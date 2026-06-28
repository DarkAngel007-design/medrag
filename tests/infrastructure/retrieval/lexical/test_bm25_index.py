from __future__ import annotations

from uuid import uuid4

import pytest

from medrag.domain.entities.chunk import Chunk
from medrag.infrastructure.retrieval.lexical.bm25_index import (
    BM25Index,
)
from medrag.infrastructure.retrieval.lexical.tokenizer import (
    BM25Tokenizer,
)


@pytest.fixture
def tokenizer() -> BM25Tokenizer:
    return BM25Tokenizer()


@pytest.fixture
def index(
    tokenizer: BM25Tokenizer,
) -> BM25Index:
    return BM25Index(tokenizer)


@pytest.fixture
def chunks() -> list[Chunk]:
    return [
        Chunk(
            id=uuid4(),
            document_id=uuid4(),
            text="Breast cancer is one of the most common cancers.",
            chunk_index=0,
            metadata={},
        ),
        Chunk(
            id=uuid4(),
            document_id=uuid4(),
            text="Diabetes mellitus affects glucose metabolism.",
            chunk_index=1,
            metadata={},
        ),
        Chunk(
            id=uuid4(),
            document_id=uuid4(),
            text="The heart pumps blood throughout the body.",
            chunk_index=2,
            metadata={},
        ),
    ]


def test_build_index(
    index: BM25Index,
    chunks: list[Chunk],
) -> None:
    """Building the index should not raise."""

    index.index(chunks)

    @property
    def is_built(self) -> bool:
        assert index._bm25 is not None


def test_search_returns_relevant_chunk(
    index: BM25Index,
    chunks: list[Chunk],
) -> None:
    """Relevant chunks should rank highest."""

    index.index(chunks)

    results = index.search(
        "breast cancer",
        limit=2,
    )

    assert len(results) == 1

    assert "cancer" in results[0][0].text.lower()


def test_limit_respected(
    index: BM25Index,
    chunks: list[Chunk],
) -> None:
    """Search should respect requested limit."""

    index.index(chunks)

    results = index.search(
        "the",
        limit=1,
    )

    assert len(results) <= 1


def test_search_before_build(
    index: BM25Index,
) -> None:
    """Searching an empty index should return no results."""

    results = index.search(
        "cancer",
        limit=5,
    )

    assert results == []


def test_search_no_match(
    index: BM25Index,
    chunks: list[Chunk],
) -> None:
    """Unknown terms should return no results."""

    index.index(chunks)

    results = index.search(
        "quantum entanglement",
        limit=5,
    )

    assert results == []


def test_scores_sorted_descending(
    index: BM25Index,
    chunks: list[Chunk],
) -> None:
    """Results should be ordered by descending BM25 score."""

    index.index(chunks)

    results = index.search(
        "blood body heart",
        limit=5,
    )

    scores = [score for _, score in results]

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_incremental_indexing(
    index: BM25Index,
) -> None:
    """New chunks should be added without removing existing ones."""

    cancer_chunk = Chunk(
        id=uuid4(),
        document_id=uuid4(),
        text="Breast cancer treatment.",
        chunk_index=0,
        metadata={},
    )

    diabetes_chunk = Chunk(
        id=uuid4(),
        document_id=uuid4(),
        text="Diabetes mellitus treatment.",
        chunk_index=1,
        metadata={},
    )

    heart_chunk = Chunk(
        id=uuid4(),
        document_id=uuid4(),
        text="Heart disease affects millions.",
        chunk_index=2,
        metadata={},
    )

    index.index([cancer_chunk])
    index.index([diabetes_chunk])
    index.index([heart_chunk])

    cancer_results = index.search(
        "breast cancer",
        limit=5,
    )

    diabetes_results = index.search(
        "diabetes",
        limit=5,
    )

    assert any("cancer" in chunk.text.lower() for chunk, _ in cancer_results)

    assert any("diabetes" in chunk.text.lower() for chunk, _ in diabetes_results)
