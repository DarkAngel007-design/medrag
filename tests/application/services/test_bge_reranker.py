from __future__ import annotations

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from medrag.domain.entities.chunk import Chunk
from medrag.domain.value_objects.retrieved_chunk import RetrievedChunk
from medrag.domain.value_objects.search_query import SearchQuery
from medrag.infrastructure.reranking import BGEReranker
from medrag.shared.config.retrieval import RetrievalSettings


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
async def test_returns_empty_for_empty_input() -> None:
    settings = RetrievalSettings()

    with patch(
        "medrag.infrastructure.reranking.bge_reranker.CrossEncoder"
    ) as mock_reranker:
        reranker = BGEReranker(settings)

        results = await reranker.rerank(
            SearchQuery(query="cancer"),
            [],
        )

        assert results == []

        mock_reranker.return_value.predict.assert_not_called()


@pytest.mark.asyncio
async def test_reranks_results_by_score() -> None:
    settings = RetrievalSettings(
        rerank_top_k=3,
    )

    with patch(
        "medrag.infrastructure.reranking.bge_reranker.CrossEncoder"
    ) as mock_reranker:
        model = MagicMock()
        model.predict.return_value = [
            0.2,
            0.9,
            0.5,
        ]

        mock_reranker.return_value = model

        reranker = BGEReranker(settings)

        chunks = [
            make_result("A", 1),
            make_result("B", 2),
            make_result("C", 3),
        ]

        results = await reranker.rerank(
            SearchQuery(query="biology"),
            chunks,
        )

        assert [r.chunk.text for r in results] == [
            "B",
            "C",
            "A",
        ]


@pytest.mark.asyncio
async def test_returns_top_k_results() -> None:
    settings = RetrievalSettings(
        rerank_top_k=2,
    )

    with patch(
        "medrag.infrastructure.reranking.bge_reranker.CrossEncoder"
    ) as mock_reranker:
        model = MagicMock()

        model.predict.return_value = [
            0.1,
            0.8,
            0.9,
        ]

        mock_reranker.return_value = model

        reranker = BGEReranker(settings)

        chunks = [
            make_result("A", 1),
            make_result("B", 2),
            make_result("C", 3),
        ]

        results = await reranker.rerank(
            SearchQuery(query="biology"),
            chunks,
        )

        assert len(results) == 2

        assert [r.chunk.text for r in results] == [
            "C",
            "B",
        ]


@pytest.mark.asyncio
async def test_builds_query_chunk_pairs() -> None:
    settings = RetrievalSettings()

    with patch(
        "medrag.infrastructure.reranking.bge_reranker.CrossEncoder"
    ) as mock_reranker:
        model = MagicMock()

        model.predict.return_value = [
            0.5,
            0.4,
        ]

        mock_reranker.return_value = model

        reranker = BGEReranker(settings)

        chunks = [
            make_result("Cancer treatment", 1),
            make_result("Heart disease", 2),
        ]

        query = SearchQuery(
            query="cancer",
        )

        await reranker.rerank(
            query,
            chunks,
        )

        model.predict.assert_called_once_with(
            [
                [
                    "cancer",
                    "Cancer treatment",
                ],
                [
                    "cancer",
                    "Heart disease",
                ],
            ]
        )
