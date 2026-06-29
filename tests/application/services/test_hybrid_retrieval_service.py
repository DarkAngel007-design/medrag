from __future__ import annotations

from uuid import uuid4

import pytest

from medrag.application.ports import FusionStrategy, Reranker
from medrag.application.services.hybrid_retrieval_service import (
    HybridRetrievalService,
)
from medrag.domain.entities.chunk import Chunk
from medrag.domain.value_objects.retrieved_chunk import RetrievedChunk
from medrag.domain.value_objects.search_query import SearchQuery


class FakeDenseSearchRepository:
    def __init__(
        self,
        results: list[RetrievedChunk],
    ) -> None:
        self._results = results

    async def search(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        return self._results


class FakeLexicalSearchRepository:
    def __init__(
        self,
        results: list[RetrievedChunk],
    ) -> None:
        self._results = results

    async def search(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        return self._results


class FakeFusionStrategy(FusionStrategy):
    async def fuse(
        self,
        dense_results: list[RetrievedChunk],
        lexical_results: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        return dense_results + lexical_results


class FakeReranker(Reranker):
    async def rerank(
        self,
        query: SearchQuery,
        retrieved_chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        return retrieved_chunks


def make_result(
    text: str,
    rank: int,
) -> RetrievedChunk:
    chunk = Chunk(
        id=uuid4(),
        document_id=uuid4(),
        text=text,
        chunk_index=rank,
        metadata={},
    )

    return RetrievedChunk(
        chunk=chunk,
        score=1.0,
        rank=rank,
    )


@pytest.mark.asyncio
async def test_merge_dense_and_lexical_results() -> None:
    dense = [
        make_result("Cancer", 1),
        make_result("Diabetes", 2),
    ]

    lexical = [
        make_result("Heart", 1),
    ]

    service = HybridRetrievalService(
        dense_search_repository=FakeDenseSearchRepository(dense),
        lexical_search_repository=FakeLexicalSearchRepository(lexical),
        fusion_strategy=FakeFusionStrategy(),
        reranker=FakeReranker(),
    )

    results = await service.retrieve(SearchQuery(query="cancer"))

    assert len(results) == 3
    assert results == dense + lexical
