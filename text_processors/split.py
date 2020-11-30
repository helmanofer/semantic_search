from abc import ABC, abstractmethod
from typing import List, Iterator


class Split(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(self, text: List[str]) -> Iterator[List[str]]:
        pass


class WhiteSpaceSplite(Split):
    def __init__(self, chunk_length: int, overlap: int) -> None:
        self.overlap = overlap
        self.chunk_length = chunk_length

    def __call__(self, text: str) -> List[str]:
        return text.split()
