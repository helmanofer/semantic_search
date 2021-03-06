import json
from typing import Optional, Any

from pydantic import BaseModel

from embeddings.embeddings import Vector
from text_processors.chunk import OverlappingFixedSizeChunk
from text_processors.split import WhiteSpaceSplit


class IndexedChunk(BaseModel):
    text: str
    parent_id: Optional[int]
    id: Optional[int]
    embeddings: Optional[Vector]


class IndexedDoc(BaseModel):
    id: Optional[int]
    text: str
    chunks: Optional[list[IndexedChunk]]

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._do_chunk()

    def _do_chunk(self):
        if not self.chunks:
            wss = WhiteSpaceSplit()
            ofsc = OverlappingFixedSizeChunk(10, 2)
            for chunked_tokens in ofsc(wss(self.text)):
                ic = IndexedChunk(text=" ".join(chunked_tokens),
                                  parent_id=self.id)
                self.chunks.append(ic)

        for chunk in self.chunks:
            if not chunk.embeddings:
                from embeddings import embedding
                chunk.embeddings = embedding.infer([chunk.text])



class IndexedDocJsonWithEmbedding(IndexedDoc):
    def __init__(self, data: str, *args, **kwargs) -> None:
        super().__init__(data)
        jdata = json.loads(data)
        self.id = jdata["id"]
        self.text = jdata["text"]
        for chunk_json in jdata['chunks']:
            chunk = IndexedChunk()
            chunk.id = chunk_json["id"]
            chunk.parent_id = self.id
            chunk.text = chunk_json["text"]
            chunk.vector = chunk_json["vector"]
            self.chunks.append(chunk)


if __name__ == "__main__":
    pass