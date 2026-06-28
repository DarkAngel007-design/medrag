from __future__ import annotations

import asyncio
from uuid import UUID

from medrag.domain.repositories.dense_search_repository import (
    DenseSearchRepository,
)
from medrag.domain.repositories.lexical_search_repository import (
    LexicalSearchRepository,
)
from medrag.domain.value_objects.retrieved_chunk import (
    RetrievedChunk,
)
from medrag.domain.value_objects.search_query import (
    SearchQuery,
)


class HybridRetrievalService:
    """Coordinates retrieval across multiple search backends."""

    def __init__(
        self,
        dense_search_repository: DenseSearchRepository,
        lexical_search_repository: LexicalSearchRepository,
    ) -> None:
        self._dense = dense_search_repository
        self._lexical = lexical_search_repository

    async def retrieve(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """Retrieve results from all backends."""

        dense_results, lexical_results = await asyncio.gather(
            self._dense.search(query),
            self._lexical.search(query),
        )

        return self._merge_results(
            dense_results,
            lexical_results,
        )

    def _merge_results(
        self,
        dense_results: list[RetrievedChunk],
        lexical_results: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        """Merge dense and lexical results without ranking."""

        merged: list[RetrievedChunk] = []
        seen: set[UUID] = set()

        for result in [*dense_results, *lexical_results]:
            if result.chunk.id in seen:
                continue

            seen.add(result.chunk.id)
            merged.append(result)

        return merged
