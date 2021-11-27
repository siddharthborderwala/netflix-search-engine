from flask.app import Flask
from flask.templating import render_template
from flask import request

from lib.query import get_results, get_show_data

app = Flask(__name__)


@app.get("/")
def root():
    return render_template("home.html")


@app.post("/query")
@app.errorhandler(400)
def make_query():
    try:
        query = request.form["query"]
    except KeyError:
        return "Invalid Query", 400
    res = get_results(query)
    res['query'] = query
    return render_template("results.html", results=res)


@app.get("/show/<show_id>")
def render_show(show_id=None):
    show = get_show_data(show_id)
    show['num_actors'] = len(show['actors'])
    show['num_directors'] = len(show['directors'])
    return render_template("show.html", show=show)
