from abc import ABC, abstractmethod
from utils.conf_util import read_app_yaml
from indexed_docs.indexed_docs import IndexedDocs
from utils.model import SearchResults


class Searcher(ABC):
    def __init__(self, name) -> None:
        self.name: str = name
        self.conf = read_app_yaml()['searcher']

    @abstractmethod
    def search(self, text: str) -> SearchResults:
        pass

    @abstractmethod
    def index(self, index_docs: IndexedDocs):
        pass

    @abstractmethod
    def commit(self):
        pass
