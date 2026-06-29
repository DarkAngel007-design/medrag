from collections import defaultdict
from uuid import UUID

from medrag.application.ports import FusionStrategy
from medrag.domain.value_objects.retrieved_chunk import RetrievedChunk


class RRFFusion(FusionStrategy):
    """Reciprocal Rank Fusion implementation."""

    def __init__(self, k: int = 60) -> None:
        self._k = k

    async def fuse(
        self,
        dense_results: list[RetrievedChunk],
        lexical_results: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        """Fuse dense and lexical retrieval results using Reciprocal Rank Fusion."""

        scores: dict[UUID, float] = defaultdict(float)
        chunks: dict[UUID, RetrievedChunk] = {}

        for retrieved_chunk in dense_results:
            chunk_id = retrieved_chunk.chunk.id
            scores[chunk_id] += 1.0 / (self._k + retrieved_chunk.rank)
            chunks[chunk_id] = retrieved_chunk

        for retrieved_chunk in lexical_results:
            chunk_id = retrieved_chunk.chunk.id
            scores[chunk_id] += 1.0 / (self._k + retrieved_chunk.rank)
            chunks[chunk_id] = retrieved_chunk

        ranked_ids = sorted(
            scores,
            key=lambda chunk_id: scores[chunk_id],
            reverse=True,
        )

        return [chunks[chunk_id] for chunk_id in ranked_ids]
