from typing import List, TypedDict


class SearchResult(TypedDict):
    id: str
    text: str


SearchResults = List[SearchResult]
