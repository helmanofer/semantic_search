from abc import ABC, abstractmethod
from utils.types import SearchResults


class SearchEngine(ABC):
    @abstractmethod
    def search(self, text: str) -> SearchResults:
        pass
