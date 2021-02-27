import logging
import numpy as np
from embeddings import embedding
from indexed_docs.indexed_docs import IndexedDocs
import json
from searcher.searcher import Searcher
from utils.types import SearchResults
from store.vector_store import AnnoyVectorStore
from store.text_store import LevelTextStore


logger = logging.getLogger(__name__)


class AnnoyLevelSearch(Searcher):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.conf = self.conf['annoy']
        self.chunked_store = LevelTextStore(f"{name}_chunks",
                                            val_serializer=json.dumps,
                                            val_deserializer=json.loads)
        self.text_store = LevelTextStore(name)
        self.vec_store = AnnoyVectorStore(name, embedding.dim,
                                          self.conf['metric'])
        self.bhem = embedding

    def search(self, text: str) -> SearchResults:
        vec = self.bhem.infer([text])[0]
        logger.info(f"search vec {vec}")
        ret = self.vec_store.knn(np.array(vec), 20)

        items = []
        for ix, score in zip(*ret):
            t = self.chunked_store.get(ix)
            items.append(dict(id=ix, text=f" ... {t['text']} ... "))
            t["text"] = t["text"][::-1]
            logger.info(f"{ix}, {score}, {t}")

        return items

    def index(self, index_docs: IndexedDocs):
        try:
            for doc in index_docs:
                self.text_store.put(doc.id, doc.text)
                for chunk in doc.chunks:
                    d = {"text": chunk.text, "id": chunk.parent_id}
                    self.chunked_store.put(chunk.id, d)
                    arr = np.array(chunk.vector, dtype=np.float)
                    self.vec_store.put(chunk.id, arr)
        except Exception as e:
            print(e)
