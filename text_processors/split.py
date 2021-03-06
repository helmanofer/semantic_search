from abc import ABC, abstractmethod
from typing import List, Iterator


class Split(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(self, text: str) -> List[str]:
        pass


class WhiteSpaceSplit(Split):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, text: str) -> List[str]:
        return text.split()
