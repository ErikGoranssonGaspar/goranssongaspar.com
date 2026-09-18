"""Server-side arXiv RSS filter.

Fetches the upstream arXiv RSS feed for a fixed set of categories and drops
every item whose announce type is not "new" or "cross", i.e. it removes
revisions of previously announced preprints. The filtered document is a
verbatim subtree of the upstream RSS 2.0 feed, so all arXiv-specific metadata
(dc:creator, arxiv:DOI, category, ...) is preserved.

Caching follows stale-while-revalidate: a cached feed is always served
immediately, and at most one thread refreshes it at a time. Network I/O never
happens while the lock is held, so a slow or unreachable upstream cannot make
requests queue behind one another. After a failed refresh the next attempt is
deferred for RETRY_AFTER seconds rather than retried once per request.
"""

from __future__ import annotations

import gzip
import threading
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

CATEGORIES = ["math.PR", "math.OC", "stat", "q-fin", "econ"]
KEEP_TYPES = frozenset({"new", "cross"})

UPSTREAM = "https://rss.arxiv.org/rss/" + "+".join(CATEGORIES)
CACHE_TTL = 1800  # serve without revalidating, seconds
RETRY_AFTER = 120  # back off this long after a failed refresh, seconds
FETCH_TIMEOUT = 20  # socket timeout for one upstream fetch, seconds
USER_AGENT = "goranssongaspar.com feed filter (+https://goranssongaspar.com/)"

ARXIV_NS = "http://arxiv.org/schemas/atom"
NAMESPACES = {
    "arxiv": ARXIV_NS,
    "dc": "http://purl.org/dc/elements/1.1/",
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
}

for _prefix, _uri in NAMESPACES.items():
    ET.register_namespace(_prefix, _uri)

# _lock guards the mutable state below. It is never held across network I/O.
_lock = threading.Lock()
_body: bytes | None = None
_etag: str | None = None
_fetched_at = 0.0  # time of last successful refresh
_next_attempt = 0.0  # earliest time a refresh may be attempted again
_refreshing = False  # True while some thread is fetching upstream


def _announce_type(item: ET.Element) -> str:
    """Return an item's announce type, falling back to the description text."""
    node = item.find(f"{{{ARXIV_NS}}}announce_type")
    if node is not None and node.text:
        return node.text.strip().lower()
    # Older feeds expose the type only inside the description.
    description = item.findtext("description") or ""
    marker = "Announce Type:"
    if marker in description:
        tail = description.split(marker, 1)[1].strip()
        return tail.split(None, 1)[0].strip().lower()
    return ""


def filter_feed(raw: bytes) -> bytes:
    """Drop items whose announce type is not in KEEP_TYPES."""
    root = ET.fromstring(raw)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("upstream feed has no <channel> element")

    for item in list(channel.findall("item")):
        if _announce_type(item) not in KEEP_TYPES:
            channel.remove(item)

    # Upstream's rel="self" advertises arXiv's own URL, which is wrong here.
    link = channel.find("atom:link", NAMESPACES)
    if link is not None:
        channel.remove(link)

    return ET.tostring(root, encoding="UTF-8", xml_declaration=True)


def _read(response) -> bytes:
    payload = response.read()
    if response.headers.get("Content-Encoding") == "gzip":
        payload = gzip.decompress(payload)
    return payload


def _fetch(etag: str | None) -> tuple[bytes | None, str | None]:
    """Fetch upstream. Returns (body, etag); body is None on HTTP 304."""
    request = urllib.request.Request(
        UPSTREAM,
        headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"},
    )
    if etag:
        request.add_header("If-None-Match", etag)

    try:
        with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
            return _read(response), response.headers.get("ETag")
    except urllib.error.HTTPError as error:
        if error.code == 304:
            return None, etag
        raise


def _revalidate(etag: str | None) -> None:
    """Refresh the cache from upstream. Must be called without holding _lock."""
    global _body, _etag, _fetched_at, _next_attempt, _refreshing
    try:
        raw, new_etag = _fetch(etag)
        filtered = filter_feed(raw) if raw is not None else None
    except Exception:
        with _lock:
            _next_attempt = time.time() + RETRY_AFTER
            _refreshing = False
        raise

    with _lock:
        if filtered is not None:  # None means HTTP 304, cached copy still valid
            _body = filtered
            _etag = new_etag
        _fetched_at = time.time()
        _next_attempt = 0.0
        _refreshing = False


def get_feed() -> tuple[bytes, bool]:
    """Return (feed_bytes, is_stale).

    Raises only when the cache is empty and upstream cannot be reached.
    """
    global _refreshing
    now = time.time()

    with _lock:
        body = _body
        # Only revalidate conditionally when we have a body to fall back on;
        # otherwise a 304 would leave us with nothing to serve.
        etag = _etag if body is not None else None
        if body is not None and now - _fetched_at < CACHE_TTL:
            return body, False
        # Claim the refresh unless another thread holds it or we are backing off.
        claimed = not _refreshing and now >= _next_attempt
        if claimed:
            _refreshing = True

    if not claimed:
        if body is not None:
            return body, True  # serve stale instead of queueing on upstream
        raise RuntimeError("no cached arXiv feed available")

    try:
        _revalidate(etag)
    except Exception:
        if body is not None:
            return body, True
        raise

    with _lock:
        return _body, False
