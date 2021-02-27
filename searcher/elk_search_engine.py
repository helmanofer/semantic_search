import numpy as np
from indexed_docs.indexed_docs import IndexedDocs
from searcher.searcher import Searcher
from elasticsearch import Elasticsearch, helpers
from utils.types import SearchResults
from flask import json
from lsh.random_projection import LshGaussianRandomProjection
from embeddings import embedding
from searcher.elk_mapping import mapping


class ElkSearch(Searcher):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.conf = self.conf['elk']
        self.model = embedding
        self.lsh_g = LshGaussianRandomProjection(
            vector_dimension=embedding.dim, bucket_size=4,
            num_of_buckets=40, seed=4
        )
        self.es: Elasticsearch
        self._init_es()
        self.lsh_g.fit()
        self.n = 10

    def _init_es(self):
        self.es = Elasticsearch(
            self.conf["ELK_IP"],
            http_auth=(self.conf["ADMIN_USER"],
                       self.conf["ADMIN_PASSWORD"]),
            ssl_context=self.conf["ELK_SCHEME"],
            scheme="http",
            port=self.conf["ELK_PORT"],
        )

    def recreate_index(self):
        print("recreating index")
        self.es.indices.delete(
            index=self.name, params=dict(ignore_unavailable="true")
        )
        self.es.indices.create(index=self.name, body=mapping)

    def index(self, index_docs: IndexedDocs):

        def iterarte():
            for doc in index_docs:
                action = {
                    "_index": self.name,
                    "_id": doc.id,
                    "_source": {
                        "text": doc.text,
                        "paragraphs": [
                            {
                                "par_text": p.text,
                                "par_tokens": p.text.split(),
                                # "par_vector": p.vector,
                                "lsh": " ".join(self.lsh_g.indexable_transform(
                                    np.array(p.vector, dtype=np.float))
                                    )
                            }
                            for p in doc.chunks
                        ],
                    }
                }
                yield action
        helpers.bulk(self.es, iterarte(), chunk_size=self.n)
        self.es.indices.refresh(index=self.name)

    def infer(self, text: str):
        q_vec = self.model.infer([text])[0]
        lsh = " ".join(self.lsh_g.indexable_transform(q_vec))
        return lsh

    def search(self, text: str) -> SearchResults:
        lsh = self.infer(text)

        q = {
            "stored_fields": [],
            "query": {
                "nested": {
                    "path": "paragraphs",
                    "query": {
                        "match": {
                            "paragraphs.lsh": {
                                "query": lsh,
                                "minimum_should_match": "40%",
                            }
                        }
                    },
                    "score_mode": "avg",
                }
            },
            "highlight": {
                "no_match_size": 40,
                "pre_tags": ["<mark>"],
                "post_tags": ["</mark>"],
                "highlight_query": {"match": {"text": text}},
                "fields": {"text": {"type": "unified"}},
            },
        }

        jres = self.es.search(index=self.name, body=q)

        print(json.dumps(q, indent=" "))
        # res = requests.get(
        #     url="http://127.0.0.1:9200/tapuz/_search",
        #     json=q,
        #     auth=HTTPBasicAuth("admin", "admin"),
        #     verify=False,
        # )

        items = []
        # jres = res.json()
        for r in jres["hits"]["hits"]:
            items.append(
                dict(
                    id=r["_id"],
                    text=" ... ".join(r.get("highlight", {}).get("text", [])),
                )
            )

        return items
