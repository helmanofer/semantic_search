from abc import ABC, abstractmethod
from typing import List


Sentences = List[str]
Vector = List[float]
Vectors = List[Vector]


class Embeddings(ABC):
    def __init__(self, dim: int) -> None:
        self.dim = dim

    @abstractmethod
    def infer(self, sentences: Sentences) -> Vectors:
        pass


class DummyEmbeddings(Embeddings):
    def __init__(self) -> None:
        super().__init__(768)

    def infer(self, sentences: Sentences) -> Vectors:
        return []
