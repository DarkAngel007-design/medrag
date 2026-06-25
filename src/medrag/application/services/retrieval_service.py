from __future__ import annotations

from medrag.domain.repositories.search_repository import (
    SearchRepository,
)
from medrag.domain.value_objects.retrieved_chunk import (
    RetrievedChunk,
)
from medrag.domain.value_objects.search_query import SearchQuery


class RetrievalService:
    """Application service responsible for retrieval."""

    def __init__(
        self,
        search_repository: SearchRepository,
    ) -> None:
        self._search_repository = search_repository

    async def retrieve(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """Retrieve relevant chunks."""

        return await self._search_repository.search(
            query,
        )
