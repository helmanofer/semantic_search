from logging import INFO

import uvicorn
from fastapi import FastAPI
from starlette.templating import Jinja2Templates

from indexed_docs.indexed_doc import IndexedDoc
from indexed_docs.indexed_docs import IndexedDocs
from searcher import searcher
from searcher.searcher import Searcher
from utils.types import SearchResults
import logging


logging.basicConfig(level=INFO)
logger = logging.getLogger()

se: Searcher = searcher

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

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/search")
@app.get("/search/{query}")
def search(query: str = None):
    if not query:
        return templates.TemplateResponse("search.html", dict(data=[], columns=columns))
        # return render_template("search.html", )
    logger.info(f"got query: {query}")
    items: SearchResults = se.search(query)
    logger.info(f"got data {items}")
    return items


docs = IndexedDocs()


@app.post("/index/")
def index(doc: IndexedDoc):
    logger.info(f"got doc: {doc}")
    docs.add_doc(doc)
    searcher.index(docs)


if __name__ == "__main__":
    uvicorn.run(app)
