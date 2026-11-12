from flask import Flask, render_template, redirect, url_for, request, Response
from jinja_markdown2 import MarkdownExtension
from jinja2 import ChoiceLoader, FileSystemLoader
from datetime import datetime

import arxiv_filter

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)
app.jinja_loader = ChoiceLoader([app.jinja_loader, FileSystemLoader(["static/doc"])])

POSTS = [
    {
        "title": "Final Words on Timing Prediction Markets",
        "slug": "masters-thesis",
        "description": '''Timing prediction markets are based on questions like "Will Event A occur before time T?"; they're especially interesting in geopolitics. I have spent the last six months elaborating a reduced-form model of these timing markets. More sophisticated techniques are able to achieve reasonable calibration across the entire predictive distribution.''',
        "date": "2026-07-13",
    },
    {
        "title": "A Poisson Model of Timing Prediction Markets",
        "slug": "OU-timing",
        "description": "Prediction markets of the type \"Will Khamenei be ousted before 2025?\" don't try to forecast the outcome of an event, but its timing. I present the first model of such prediction market prices, based on methods developed for defaultable corporate bonds.",
        "date": "2026-03-01",
    },
    {
        "title": "Modeling Binary Prediction Markets",
        "slug": "binary-AI09",
        "description": "Who will win the next election? Prediction markets turn such questions into tradable contracts, whose market prices reveal collective beliefs about uncertain events. I evaluate the state-of-the-art model of such markets, which models these contracts as derivatives on latent processes. Turns out it's not great!",
        "date": "2025-10-02",
    },
    {
        "title": "Optimal Mastermind",
        "slug": "mastermind",
        "description": "Remember the game Mastermind, where you have to guess a secret color combination? I explain how we can use information theory to play it optimally. Play around with the interactive game!",
        "date": "2025-06-11",
    },
]


@app.template_filter("rfc822")
def rfc822_filter(date_str):
    """Convert ISO date string to RFC 822 format for RSS."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%a, %d %b %Y 00:00:00 GMT")


@app.template_filter("pretty_date")
def pretty_date_filter(date_str):
    """Convert ISO date string to a human-readable date, e.g. '13 July 2026'."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{dt.day} {dt:%B %Y}"


@app.route("/")
def index():
    return render_template("index.html", posts=POSTS)


@app.route("/bachelors-thesis")
def bachelors_thesis():
    return redirect(url_for("static", filename="doc/bachelors-thesis.pdf"))


@app.route("/binary-AI09")
def binary_AI09():
    return render_template("binary-AI09.html")


@app.route("/OU-timing")
def ou_cox_timing_pm():
    return render_template("ou_cox_timing_pm.html")


@app.route("/masters-thesis")
def masters_thesis():
    return render_template("masters_thesis.html")


@app.route("/feed")
def rss_feed():
    return (
        render_template("rss.xml", posts=POSTS),
        200,
        {"Content-Type": "application/rss+xml"},
    )


@app.route("/arxiv-feed")
def arxiv_feed():
    """Upstream arXiv feed with revisions removed (new and cross only)."""
    try:
        body, stale = arxiv_filter.get_feed()
    except Exception:
        return Response(
            "upstream arXiv feed unavailable",
            status=502,
            mimetype="text/plain",
        )
    return Response(
        body,
        mimetype="application/rss+xml",
        headers={
            "Cache-Control": f"max-age={arxiv_filter.CACHE_TTL}",
            "X-Upstream-Stale": "1" if stale else "0",
        },
    )


import mastermind_server

if __name__ == "__main__":
    app.run(debug=True)
