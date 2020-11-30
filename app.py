from logging import INFO
from utils.conf_util import conf_to_env, read_app_yaml
from search_engine import searcher
from search_engine.search_engine import SearchEngine
from utils.types import SearchResults
from flask import Flask, render_template, jsonify
import logging


# conf_to_env()

logging.basicConfig(level=INFO)
conf = read_app_yaml()
se: SearchEngine = searcher

columns = [
    {
        "field": "id",  # which is the field's name of data key
        "title": "id",  # display as the table header's name
        "sortable": True,
    },
    {
        "field": "text",
        "title": "text",
        "sortable": False,
    },
]

app = Flask(__name__)


@app.route("/search")
@app.route("/search/<query>")
def search(query=None):
    if not query:
        return render_template("search.html", data=[], columns=columns)
    app.logger.info(f"got query: {query}")
    items: SearchResults = se.search(query)
    app.logger.info(f"got data {items}")
    return jsonify(items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
