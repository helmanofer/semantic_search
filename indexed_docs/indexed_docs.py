from typing import List

from utils.model import IndexedDoc


class IndexedDocs:
    def __init__(self) -> None:
        self._doc_iter = None
        self.indexed_docs: list = []
        self.bulk_size: int = 100
        self._force: bool = False

    def add_doc(self, doc: IndexedDoc):
        self.indexed_docs.append(doc)

    def get_bulk(self) -> List[IndexedDoc]:
        if not self.force and len(self.indexed_docs) < self.bulk_size:
            yield []
        else:
            for doc in self.indexed_docs:
                yield doc
            self.indexed_docs = []

    @property
    def force(self):
        yield self._force
        self._force = False

    @force.setter
    def force(self, force: bool):
        self._force = force
