from utils.conf_util import conf_to_env
import os
from typing import Callable, Iterator

from tqdm import tqdm
from elasticsearch import Elasticsearch, helpers
from jsonlines import jsonlines

# from utils.add_yaml_to_env import conf_to_env
# from utils.utils import get_project_root
# from utils.mappings import mapping
import logging

from mapping import mapping
from utils.index import read_tapuz_data


class Indexer(object):
    def __init__(
        self,
        es: Elasticsearch,
        index_name: str,
        doc_processor: Callable[[dict], dict] = lambda x: x,
        filter_function: Callable[[dict], bool] = lambda x: True,
    ):
        self.n = 20
        self.es = es
        self.process_doc = doc_processor
        self.index_name = index_name
        self.filter_function = filter_function

    def chunks(self, l):
        """Yield successive n-sized chunks from l."""
        chunk = []
        for i in l:
            chunk.append(i)
            if len(chunk) == self.n:
                yield chunk
                chunk = []
        yield chunk

    def recreate_index(self):
        print("recreating index")
        self.es.indices.delete(index=self.index_name, params=dict(ignore_unavailable="true"))
        self.es.indices.create(index=self.index_name, body=mapping)

    def index_one(self, doc):
        _id = doc.pop("_id")
        self.es.index(index=self.index_name, id=_id, body=doc)

    def index(self, iterator: Iterator):
        actions = []
        for doc in tqdm(iterator):
            _id = doc.pop("_id")
            if not _id:
                continue
            action = {"_index": self.index_name, "_id": _id, "_source": self.process_doc(doc)}
            actions.append(action)
            if len(actions) == self.n:
                helpers.bulk(self.es, actions)
                actions = []
        helpers.bulk(self.es, actions)
        self.es.indices.refresh(index=self.index_name)

    def index_from_file(self, filename):
        with jsonlines.open(filename) as docs:
            self.index(docs)

    def find_replace(self, new_name_key, new_name_value, id_key, id_value):
        query = {
            "script": {"source": f"ctx._source.{new_name_key} = '{new_name_value}'"},
            "query": {"term": {id_key: id_value}},
        }

        r = self.es.update_by_query(
            self.index_name, body=query, request_timeout=60, refresh=True, wait_for_completion=False
        )
        logging.info(r)


if __name__ == "__main__":
    conf_to_env()

    # context = create_default_context(cafile=os.environ["CA_KEY_FILE"])
    context = None
    es_ = Elasticsearch(
        os.environ["ELK_IP"],
        http_auth=(os.environ["ADMIN_USER"], os.environ["ADMIN_PASSWORD"]),
        ssl_context=context,
        scheme="http",
        port=os.environ["ELK_PORT"],
    )

    index_name_ = os.environ["INDEX_NAME"]
    indexer = Indexer(es_, index_name_)
    indexer.recreate_index()

    indexer.index(read_tapuz_data())
