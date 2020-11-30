from text_processors.chunk import Chunk
from text_processors.split import Split
from indexed_docs.indexed_doc import IndexedDoc
from typing import Iterable, Type, Union


class IndexedDocs:
    def __init__(self,
                 indexed_doc: Type[IndexedDoc],
                 split: Union[Split, None],
                 chunk: Union[Chunk, None]
                 ) -> None:
        self._doc_iter = None
        self.indexed_doc = indexed_doc
        self.split = split
        self.chunk = chunk

    @property
    def iter(self):
        return self._doc_iter

    @iter.setter
    def iter(self, iter: Iterable):
        self._doc_iter = iter

    def __iter__(self):
        for doc in self._doc_iter:
            yield self.indexed_doc(doc, self.split, self.chunk)
