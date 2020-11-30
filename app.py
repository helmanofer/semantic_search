from logging import INFO
from utils.conf_util import conf_to_env, read_app_yaml
from search_engine.elk_search_engine import ElkSearch
from search_engine.annoy_level_search_engine import AnnoyLevelSearch
from search_engine.search_engine import SearchEngine
from utils.types import SearchResults
# from search_engine.elk import ElkSearch
from flask import Flask, render_template, jsonify
import logging

conf_to_env()

logging.basicConfig(level=INFO)
conf = read_app_yaml()
se: SearchEngine = ElkSearch(conf['name'])
# se2: SearchEngine = AnnoyLevelSearch()

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


# @app.route("/search")
# @app.route("/search/<query>")
# def search(query=None):
#     if not query:
#         return render_template("search.html", data=[], columns=columns)

#     items: SearchResults = se.search(query)
#     app.logger.info(f"got data {items}")
#     return jsonify(items)


@app.route("/search")
@app.route("/search/<query>")
def search2(query=None):
    if not query:
        return render_template("search.html", data=[], columns=columns)
    app.logger.info(f"got query: {query}")
    items: SearchResults = se.search(query)
    app.logger.info(f"got data {items}")
    return jsonify(items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
