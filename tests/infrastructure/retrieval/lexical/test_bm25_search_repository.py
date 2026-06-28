from __future__ import annotations

from uuid import uuid4

import pytest

from medrag.domain.entities.chunk import Chunk
from medrag.domain.value_objects.search_query import SearchQuery
from medrag.infrastructure.retrieval.lexical.bm25_index import (
    BM25Index,
)
from medrag.infrastructure.retrieval.lexical.bm25_search_repository import (
    BM25SearchRepository,
)
from medrag.infrastructure.retrieval.lexical.tokenizer import (
    BM25Tokenizer,
)


@pytest.fixture
def repository() -> BM25SearchRepository:
    tokenizer = BM25Tokenizer()
    index = BM25Index(tokenizer)

    return BM25SearchRepository(index)


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


@pytest.mark.asyncio
async def test_index_and_search(
    repository: BM25SearchRepository,
    chunks: list[Chunk],
) -> None:
    """Repository should return retrieved chunks."""

    await repository.index(chunks)

    query = SearchQuery(
        query="breast cancer",
        top_k=5,
    )

    results = await repository.search(query)

    assert len(results) == 1

    assert "cancer" in results[0].chunk.text.lower()

    assert results[0].rank == 1

    assert results[0].score > 0


@pytest.mark.asyncio
async def test_search_before_indexing(
    repository: BM25SearchRepository,
) -> None:
    """Searching before indexing should return an empty list."""

    query = SearchQuery(
        query="cancer",
        top_k=5,
    )

    results = await repository.search(query)

    assert results == []


@pytest.mark.asyncio
async def test_top_k_respected(
    repository: BM25SearchRepository,
    chunks: list[Chunk],
) -> None:
    """Repository should respect top_k."""

    await repository.index(chunks)

    query = SearchQuery(
        query="cancer diabetes",
        top_k=1,
    )

    results = await repository.search(query)

    assert len(results) <= 1
