from flask import Flask, render_template, redirect, url_for
from jinja_markdown2 import MarkdownExtension
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader(['static/doc'])
])

@app.route("/")
def index():
    return render_template('index.html')
    #return render_template('base.html')

@app.route("/bachelors-thesis")
def bachelors_thesis():
    return redirect(url_for('static', filename='doc/bachelors-thesis.pdf'))

import mastermind_server

if __name__ == '__main__':
    app.run(debug=True)
