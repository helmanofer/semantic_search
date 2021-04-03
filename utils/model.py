from typing import List, Optional, Any

from pydantic import BaseModel

from text_processors.chunk import OverlappingFixedSizeChunk
from text_processors.split import WhiteSpaceSplit

Sentences = List[str]
Vector = List[float]
Vectors = List[Vector]


class Chunk(BaseModel):
    text: str
    parent_id: Optional[int]
    id: Optional[int]
    embeddings: Optional[Vector]


class Doc(BaseModel):
    id: Optional[int]
    text: str
    chunks: Optional[list[Chunk]]


class SearchResult(Doc):
    pass


SearchResults = List[SearchResult]


class IndexedDoc(Doc):
    def __init__(self, **data: Any):
        super().__init__(**data)
        self._do_chunk()

    def _do_chunk(self):
        if not self.chunks:
            wss = WhiteSpaceSplit()
            ofsc = OverlappingFixedSizeChunk(10, 2)
            for chunked_tokens in ofsc(wss(self.text)):
                ic = Chunk(text=" ".join(chunked_tokens),
                           parent_id=self.id)
                self.chunks.append(ic)

        for chunk in self.chunks:
            if not chunk.embeddings:
                from embeddings import embedding
                chunk.embeddings = embedding.infer([chunk.text])
