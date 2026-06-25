from uuid import UUID

from pydantic import BaseModel


class SearchResult(BaseModel):
    """Single retrieval result."""

    chunk_id: UUID
    document_id: UUID
    text: str
    score: float
    rank: int


class SearchResponse(BaseModel):
    """Search response."""

    results: list[SearchResult]
