from data.tapuz import read_tapuz_data_with_vec
import os
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth
from utils.indexer import Indexer
from utils.conf_util import conf_to_env

from elasticsearch import Elasticsearch


conf_to_env()


def index():
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

    indexer.index(read_tapuz_data_with_vec())


def search():
    q = {
        "stored_fields": [],
        "query": {
            "nested": {
                "path": "paragraphs",
                "query": {
                    "match": {
                        "paragraphs.lsh": {
                            "query": "0_0101 1_0111 2_0100 3_1101 4_0100 5_0001 6_0001 7_1011 8_0101 9_1001 10_0111 11_0010 12_1111 13_1111 14_0011 15_1001 16_1001 17_1010 18_0010 19_1011 20_1000 21_1110 22_1111 23_1100 24_1100 25_1111 26_1010 27_0000 28_0110 29_0110 30_1011 31_1110 32_0101 33_0011 34_0000 35_1110 36_1000 37_1011 38_0001 39_0111",
                            "minimum_should_match": "40%",
                        }
                    }
                },
                "score_mode": "avg",
            }
        },
        "highlight": {
            "highlight_query": {"match": {"text": "כמה עולה ליישר את ההגה"}},
            "fields": {"text": {"type": "unified"}},
        },
    }
    res = requests.get(
        url="http://127.0.0.1:9200/tapuz/_search",
        json=q,
        auth=HTTPBasicAuth("admin", "admin"),
        verify=False,
    )
    pprint(res.json())


index()
