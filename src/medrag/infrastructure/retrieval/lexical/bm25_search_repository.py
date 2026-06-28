from __future__ import annotations

import asyncio

from medrag.domain.entities.chunk import Chunk
from medrag.domain.repositories.lexical_search_repository import (
    LexicalSearchRepository,
)
from medrag.domain.value_objects.retrieved_chunk import RetrievedChunk
from medrag.domain.value_objects.search_query import SearchQuery

from .bm25_index import BM25Index


class BM25SearchRepository(LexicalSearchRepository):
    """BM25-based implementation of lexical search."""

    def __init__(
        self,
        index: BM25Index,
    ) -> None:
        self._index = index

    async def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        """Index chunks for lexical retrieval."""

        await asyncio.to_thread(
            self._index.index,
            chunks,
        )

    async def search(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """Search the BM25 index."""

        results = await asyncio.to_thread(
            self._index.search,
            query.query,
            query.top_k,
        )

        return [
            RetrievedChunk(
                chunk=chunk,
                score=score,
                rank=rank,
            )
            for rank, (chunk, score) in enumerate(
                results,
                start=1,
            )
        ]
