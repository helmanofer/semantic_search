from flask import json
from lsh.random_projection import LshGaussianRandomProjection
import requests
from requests.models import HTTPBasicAuth
from flask import Flask, render_template, jsonify
from gensim.models.doc2vec import Doc2Vec


model = Doc2Vec.load("dbow_w3_EP15_yes_remove_stp")
lsh_g = LshGaussianRandomProjection(
    vector_dimension=300, bucket_size=4, num_of_buckets=40, seed=4
)
lsh_g.fit()

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
        
    q_vec = model.infer_vector(query.split())
    lsh = " ".join(lsh_g.indexable_transform(q_vec))
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
            "highlight_query": {"match": {"text": query}},
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
    app.logger.info(f"got data {items}")
    return jsonify(items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
