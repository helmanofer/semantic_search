from abc import ABC
from dataclasses import dataclass
from typing import List
from embedding.embbeding import Vector
import json
from text_processors.chunk import Chunk
from text_processors.split import Split


class IndexedDoc(ABC):
    def __init__(self, data, split: Split = None, chunk: Chunk = None) -> None:
        self.id: int
        self.text: str
        self.chunks: List[IndexedChunk] = []


@dataclass
class IndexedChunk():
    def __init__(self) -> None:
        self.text: str
        self.parent_id: int
        self.id: int
        self.vector: Vector


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
