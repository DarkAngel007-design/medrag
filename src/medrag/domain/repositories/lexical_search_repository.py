from __future__ import annotations

from abc import ABC, abstractmethod

from medrag.domain.entities.chunk import Chunk
from medrag.domain.value_objects.retrieved_chunk import RetrievedChunk
from medrag.domain.value_objects.search_query import SearchQuery


class LexicalSearchRepository(ABC):
    """Repository interface for lexical document retrieval."""

    @abstractmethod
    async def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        """Index chunks for lexical retrieval."""

    @abstractmethod
    async def search(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """Retrieve relevant chunks using lexical search."""
