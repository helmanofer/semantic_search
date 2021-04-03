from random import random

from starlette.testclient import TestClient

from app import app
from embeddings import embedding

client = TestClient(app)


def test_index():
    s = {
        "text": "hello i am a robot",
        "chunks": [
            {
                "text": "hello i am",
                "embeddings": [random() for _ in range(embedding.dim)]
            },
            {
                "text": "am a robot",
                "embeddings": [random() for _ in range(embedding.dim)]
            }
        ]
    }
    r = client.post("/index", json=s)
    assert r.ok
    print(r.text)
    r = client.post("/commit")
    assert r.ok
    print(r.text)
    r = client.get("/get")
    print(r.text)
