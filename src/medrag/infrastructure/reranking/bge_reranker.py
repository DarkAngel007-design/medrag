from __future__ import annotations

import asyncio

import torch
from sentence_transformers import CrossEncoder

from medrag.application.ports import Reranker
from medrag.domain.value_objects.retrieved_chunk import RetrievedChunk
from medrag.domain.value_objects.search_query import SearchQuery
from medrag.shared.config.retrieval import RetrievalSettings


class BGEReranker(Reranker):
    """BGE cross-encoder reranker."""

    def __init__(
        self,
        settings: RetrievalSettings,
    ) -> None:
        self._model = CrossEncoder(
            settings.reranker_model,
            device="cuda" if torch.cuda.is_available() else "cpu",
        )

        self._top_k = settings.rerank_top_k

    async def rerank(
        self,
        query: SearchQuery,
        retrieved_chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        """Rerank retrieved chunks using the BGE cross-encoder."""

        if not retrieved_chunks:
            return []

        sentence_pairs = [
            [
                query.query,
                retrieved.chunk.text,
            ]
            for retrieved in retrieved_chunks
        ]

        scores = await asyncio.to_thread(
            self._model.predict,
            sentence_pairs,
        )

        ranked = sorted(
            zip(
                retrieved_chunks,
                scores,
                strict=True,
            ),
            key=lambda item: item[1],
            reverse=True,
        )

        return [chunk for chunk, _ in ranked[: self._top_k]]
