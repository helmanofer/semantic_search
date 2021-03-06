from indexed_docs.indexed_doc import IndexedDoc


def test_with_chunks_and_embeddings():
    s = {
        "text": "hello i am a robot",
        "chunks": [
            {
                "text": "hello i am",
                "embeddings": [1, 2, 3]
            },
            {
                "text": "am a robot",
                "embeddings": [1, 2, 3]
            }
        ]
    }

    i = IndexedDoc(**s)
    assert len(i.chunks) == 2
    assert i.chunks[0].text == "hello i am"
