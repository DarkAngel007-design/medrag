from abc import ABC, abstractmethod

from medrag.domain.value_objects.retrieved_chunk import RetrievedChunk
from medrag.domain.value_objects.search_query import SearchQuery


class Reranker(ABC):
    """Ranks retrieved chunks according to query relevance."""

    @abstractmethod
    async def rerank(
        self,
        query: SearchQuery,
        retrieved_chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        """Return retrieved chunks ordered by relevance."""
