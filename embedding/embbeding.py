from abc import ABC, abstractmethod
from typing import List


Sentences = List[str]
Vector = List[float]
Vectors = List[Vector]


class Embedding(ABC):
    def __init__(self, dim: int) -> None:
        self.dim = dim

    @abstractmethod
    def infer(self, sentences: Sentences) -> Vectors:
        pass


class DummyEmbedding(Embedding):
    def __init__(self) -> None:
        super().__init__(768)

    def infer(self, sentences: Sentences) -> Vectors:
        return []
