from abc import ABC, abstractmethod
from typing import Generator, Iterable, Tuple
from utils.common import get_project_root, lambda_x_x
import plyvel
from tqdm import tqdm


class TextStore(ABC):
    @abstractmethod
    def put(self, key, val):
        pass

    @abstractmethod
    def put_bulk(self, iter: Iterable[Tuple[str, str]]):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def iter(self):
        pass


class LevelTextStore(TextStore):
    def __init__(self, name: str, val_serializer=None,
                 val_deserializer=None) -> None:
        self.name = name
        p = get_project_root()
        p = p.joinpath("data").joinpath(f"{self.name}.leveldb")
        self.db = plyvel.DB(p.as_posix(), create_if_missing=True)
        if not val_serializer:
            val_serializer = lambda_x_x
        if not val_deserializer:
            val_deserializer = lambda_x_x
        self.val_serializer = val_serializer
        self.val_deserializer = val_deserializer

    def put(self, key, val):
        self.db.put(str(key).rjust(10, "0").encode(),
                    self.val_serializer(val).encode())

    def put_bulk(self, iter: Iterable[Tuple[str, str]]):
        with self.db.write_batch() as wb:
            for key, val in tqdm(iter):
                wb.put(
                    str(key).rjust(10, "0").encode(),
                    self.val_serializer(val).encode()
                )

    def put_bulk_gen_id(self, iter: Iterable[str]):
        with self.db.write_batch() as wb:
            for ix, val in tqdm(enumerate(iter)):
                wb.put(
                    str(ix).rjust(10, "0").encode(),
                    self.val_serializer(val).encode()
                )

    def get(self, key):
        val = self.db.get(str(key).rjust(10, "0").encode())
        return self.val_deserializer(val.decode())

    def iter(self) -> Generator[Tuple[str, str], None, None]:
        for key, val in self.db:
            yield key.decode(), self.val_deserializer(val.decode())
