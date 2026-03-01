from flask import Flask, render_template, redirect, url_for, request
from jinja_markdown2 import MarkdownExtension
from jinja2 import ChoiceLoader, FileSystemLoader
from datetime import datetime

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)
app.jinja_loader = ChoiceLoader([app.jinja_loader, FileSystemLoader(["static/doc"])])

POSTS = [
    {
        "title": "A Poisson Model of Timing Prediction Markets",
        "slug": "OU-timing",
        "description": "Prediction markets of the type \"Will Kahmeini be ousted before 2025?\" don't try to forecast the outcome of an event, but its timing. I present the first model of such prediction market prices, based on methods developed for defaultable corporate bonds.",
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


@app.route("/feed")
def rss_feed():
    return (
        render_template("rss.xml", posts=POSTS),
        200,
        {"Content-Type": "application/rss+xml"},
    )


import mastermind_server

if __name__ == "__main__":
    app.run(debug=True)
