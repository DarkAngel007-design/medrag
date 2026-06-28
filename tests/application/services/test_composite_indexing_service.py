from __future__ import annotations

from uuid import uuid4

import pytest

from medrag.application.services.composite_indexing_service import (
    CompositeIndexingService,
)
from medrag.domain.entities.chunk import Chunk


class FakeDenseSearchRepository:
    def __init__(self) -> None:
        self.indexed_chunks: list[Chunk] = []

    async def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        self.indexed_chunks.extend(chunks)


class FakeLexicalSearchRepository:
    def __init__(self) -> None:
        self.indexed_chunks: list[Chunk] = []

    async def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        self.indexed_chunks.extend(chunks)


@pytest.fixture
def chunks() -> list[Chunk]:
    return [
        Chunk(
            id=uuid4(),
            document_id=uuid4(),
            text="Breast cancer treatment.",
            chunk_index=0,
            metadata={},
        ),
        Chunk(
            id=uuid4(),
            document_id=uuid4(),
            text="Diabetes mellitus treatment.",
            chunk_index=1,
            metadata={},
        ),
    ]


@pytest.mark.asyncio
async def test_indexes_into_all_backends(
    chunks: list[Chunk],
) -> None:
    dense = FakeDenseSearchRepository()
    lexical = FakeLexicalSearchRepository()

    service = CompositeIndexingService(
        dense,
        lexical,
    )

    await service.index(chunks)

    assert dense.indexed_chunks == chunks
    assert lexical.indexed_chunks == chunks


@pytest.mark.asyncio
async def test_empty_chunks() -> None:
    dense = FakeDenseSearchRepository()
    lexical = FakeLexicalSearchRepository()

    service = CompositeIndexingService(
        dense,
        lexical,
    )

    await service.index([])

    assert dense.indexed_chunks == []
    assert lexical.indexed_chunks == []
