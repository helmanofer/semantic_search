from abc import ABC, abstractmethod
from typing import Iterator, List


Tokens = List[str]


class Chunk(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(self, tokens: Tokens) -> Iterator[Tokens]:
        pass


class OverlappingFixedSizeChunk(Chunk):
    def __init__(self, chunk_length: int, overlap: int) -> None:
        super().__init__()
        self.overlap = overlap
        self.chunk_length = chunk_length

    def __call__(self, tokens: Tokens) -> Iterator[Tokens]:
        for i in range(0, len(tokens), self.chunk_length - self.overlap):
            yield tokens[i: i + self.chunk_length]