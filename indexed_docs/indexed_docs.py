from indexed_docs.indexed_doc import IndexedDoc
from text_processors.chunk import Chunk
from text_processors.split import Split
from typing import Iterable, Type, Union, List, Optional


class IndexedDocs:
    def __init__(self) -> None:
        self._doc_iter = None
        self.indexed_docs: list = []
        self.bulk_size: int = 100

    def add_doc(self, doc: IndexedDoc):
        self.indexed_docs.append(doc)

    def get_bulk(self) -> List[IndexedDoc]:
        if len(self.indexed_docs) < self.bulk_size:
            yield []
        else:
            yield self.indexed_docs
            self.indexed_docs = []
