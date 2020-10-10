from logging import INFO
from search_engine.se import SearchEngine
from utils.types import SearchResults
# from search_engine.elk import ElkSearch
from search_engine.annoy_level import AnnoyLevelSearch
from flask import Flask, render_template, jsonify
import logging


logging.basicConfig(level=INFO)

# se: SearchEngine = ElkSearch()
se2: SearchEngine = AnnoyLevelSearch()

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
    items: SearchResults = se2.search(query)
    app.logger.info(f"got data {items}")
    return jsonify(items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
