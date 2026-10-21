from pydantic import BaseModel
from typing import Literal

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source_type: Literal[
        "research_paper",
        "documentation",
        "blog",
        "forum",
        "other"
    ] = "other"

class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]