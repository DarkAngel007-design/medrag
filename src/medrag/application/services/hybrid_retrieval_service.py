from __future__ import annotations

import asyncio

from medrag.application.ports.fusion_strategy import FusionStrategy
from medrag.application.ports.reranker import Reranker
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
        fusion_strategy: FusionStrategy,
        reranker: Reranker,
    ) -> None:
        self._dense = dense_search_repository
        self._lexical = lexical_search_repository
        self._fusion_strategy = fusion_strategy
        self._reranker = reranker

    async def retrieve(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """Retrieve results from all backends."""

        dense_results, lexical_results = await asyncio.gather(
            self._dense.search(query),
            self._lexical.search(query),
        )

        fused_results = await self._fusion_strategy.fuse(
            dense_results,
            lexical_results,
        )

        return await self._reranker.rerank(
            query,
            fused_results,
        )
