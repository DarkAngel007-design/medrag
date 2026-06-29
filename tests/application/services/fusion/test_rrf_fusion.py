from __future__ import annotations

from uuid import uuid4

import pytest

from medrag.application.services.fusion.rrf_fusion import RRFFusion
from medrag.domain.entities.chunk import Chunk
from medrag.domain.value_objects.retrieved_chunk import RetrievedChunk


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
async def test_fuse_returns_empty_when_no_results() -> None:
    fusion = RRFFusion()

    results = await fusion.fuse([], [])

    assert results == []


@pytest.mark.asyncio
async def test_fuse_dense_only() -> None:
    fusion = RRFFusion()

    dense = [
        make_result("Cancer", 1),
        make_result("Diabetes", 2),
    ]

    results = await fusion.fuse(dense, [])

    assert results == dense


@pytest.mark.asyncio
async def test_fuse_lexical_only() -> None:
    fusion = RRFFusion()

    lexical = [
        make_result("Cancer", 1),
        make_result("Diabetes", 2),
    ]

    results = await fusion.fuse([], lexical)

    assert results == lexical


@pytest.mark.asyncio
async def test_duplicate_chunks_are_removed() -> None:
    fusion = RRFFusion()

    shared = make_result("Cancer", 1)

    dense = [shared]
    lexical = [shared]

    results = await fusion.fuse(
        dense,
        lexical,
    )

    assert len(results) == 1
    assert results[0] == shared


@pytest.mark.asyncio
async def test_rrf_ranks_consistently_high_results_first() -> None:
    fusion = RRFFusion()

    a = make_result("A", 1)
    b_dense = make_result("B", 2)

    b_lexical = RetrievedChunk(
        chunk=b_dense.chunk,
        score=0.9,
        rank=1,
    )

    c = make_result("C", 2)

    dense = [
        a,
        b_dense,
    ]

    lexical = [
        b_lexical,
        c,
    ]

    results = await fusion.fuse(
        dense,
        lexical,
    )

    assert results[0].chunk.text == "B"


@pytest.mark.asyncio
async def test_custom_k_parameter() -> None:
    fusion = RRFFusion(k=20)

    dense = [
        make_result("Cancer", 1),
    ]

    results = await fusion.fuse(
        dense,
        [],
    )

    assert len(results) == 1
    assert results[0].chunk.text == "Cancer"
