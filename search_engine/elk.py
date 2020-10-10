

from utils.common import get_project_root
from search_engine.se import SearchEngine
from utils.types import SearchResults
from flask import json
from gensim.models.doc2vec import Doc2Vec
from lsh.random_projection import LshGaussianRandomProjection
import requests
from requests.auth import HTTPBasicAuth


class ElkSearch(SearchEngine):
    def __init__(self) -> None:
        p = get_project_root()
        p = p.joinpath("models").joinpath("dbow_w3_EP15_yes_remove_stp")
        self.model = Doc2Vec.load(p.as_posix())
        self.lsh_g = LshGaussianRandomProjection(
            vector_dimension=300, bucket_size=4, num_of_buckets=40, seed=4
        )
        self.lsh_g.fit()

    def infer(self, text: str):
        q_vec = self.model.infer_vector(text.split())
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

        print(json.dumps(q, indent=" "))
        res = requests.get(
            url="http://127.0.0.1:9200/tapuz/_search",
            json=q,
            auth=HTTPBasicAuth("admin", "admin"),
            verify=False,
        )

        items = []
        jres = res.json()
        for r in jres["hits"]["hits"]:
            items.append(
                dict(
                    id=r["_id"],
                    text=" ... ".join(r.get("highlight", {}).get("text", [])),
                )
            )

        return items
