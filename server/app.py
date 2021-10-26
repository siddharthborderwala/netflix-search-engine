from flask.app import Flask
from flask.templating import render_template
from flask import request

from lib.query import get_results

app = Flask(__name__)


@app.get("/")
def root():
    return render_template("home.html")


@app.post("/query")
@app.errorhandler(400)
@app.errorhandler(404)
def make_query():
    try:
        query = request.form['query']
    except KeyError:
        return "Invalid Query", 400
    results = get_results(query)
    return render_template("results.html", results=results)
