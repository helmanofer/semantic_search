import gzip
import json
from search_engine.se import SearchEngine
from utils.types import SearchResults
from utils.bert_embeddings_model import BertHebEmbeddingModel
from utils.common import read_all_files, split_list_to_lists_w_overlapping

from tqdm.std import tqdm
from store.vector_store import AnnoyVectorStore
from store.text_store import LevelTextStore
import logging


logger = logging.getLogger(__name__)


class AnnoyLevelSearch(SearchEngine):
    def __init__(self) -> None:
        self.chunked_store = LevelTextStore("haaretz_chunks",
                                            val_serializer=json.dumps,
                                            val_deserializer=json.loads)
        self.text_store = LevelTextStore("haaretz")
        self.vec_store = AnnoyVectorStore("haaretz", 768)
        self.bhem = BertHebEmbeddingModel()

    def search(self, text: str) -> SearchResults:
        vec = self.bhem.infer([text])[0]
        logger.info(f"search vec {vec}")
        ret = self.vec_store.knn(vec, 20)

        items = []
        for ix, score in zip(*ret):
            t = self.chunked_store.get(ix)
            items.append(dict(id=ix, text=f" ... {t['text']} ... "))
            t["text"] = t["text"][::-1]
            logger.info(f"{ix}, {score}, {t}")

        return items

    def index(self):
        all_files = read_all_files(
            "/mnt/c/SourceCode/sematic_search/data/haaretz_txt/*", "txt"
        )

        ix_ch = 0
        ix = 0
        for f in tqdm(all_files):
            text = open(f).read()
            tokenized = text.split()
            texts = split_list_to_lists_w_overlapping(tokenized, 32, 4)

            self.text_store.put(ix, text)
            texts = [" ".join(text) for text in texts]
            vectors = self.bhem.infer(texts)
            for text, vector in zip(texts, vectors):
                self.chunked_store.put(ix_ch, {"text": text, "id": ix})
                self.vec_store.put(ix_ch, vector)
                ix_ch += 1
            ix += 1

        self.vec_store.save()

    def index_from_file(self):
        fn = "/mnt/c/SourceCode/sematic_search/data/haarez.jsonl.gz"
        with gzip.open(fn, "rb") as rw:
            try:
                for line in tqdm(rw):
                    j = json.loads(line.decode())
                    self.text_store.put(j["id"], j["text"])
                    for chunk in j['chunks']:
                        d = {"text": chunk["text"], "id": j["id"]}
                        self.chunked_store.put(chunk["id"], d)
                        self.vec_store.put(chunk["id"], chunk["vector"])
            except Exception as e:
                print(e)
        self.vec_store.save()


