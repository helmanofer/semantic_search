from abc import ABC, abstractmethod
from typing import Tuple
from utils.common import get_project_root
import numpy as np
from annoy import AnnoyIndex


class VectorStore(ABC):
    @abstractmethod
    def put(self, key, vec):
        pass

    @abstractmethod
    def save(self):
        pass


class AnnoyVectorStore(VectorStore):
    def __init__(self, name: str, dim: int, metric: str) -> None:
        self.name = name
        p = get_project_root()
        p = p.joinpath("data").joinpath(f'{self.name}.ann')
        self.file_name = p.as_posix()
        self.db = AnnoyIndex(dim, metric)
        # with suppress(OSError):

    def put(self, key: int, vec: np.ndarray):
        self.db.add_item(key, vec)

    def save(self):
        self.db.build(10)  # 10 trees
        self.db.save(self.file_name)

    def knn(self, v: np.ndarray, n: int) -> Tuple[list, list]:
        self.db.load(self.file_name)
        return self.db.get_nns_by_vector(v, n, search_k=-1,
                                         include_distances=True)
