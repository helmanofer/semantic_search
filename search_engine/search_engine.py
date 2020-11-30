from abc import ABC, abstractmethod
from indexed_docs.indexed_docs import IndexedDocs
from utils.types import SearchResults


class SearchEngine(ABC):
    def __init__(self, name) -> None:
        self.name: str = name

    @abstractmethod
    def search(self, text: str) -> SearchResults:
        pass


    @abstractmethod
    def index(self, index_docs: IndexedDocs):
        pass
