from __future__ import annotations

from typing import cast

from sentence_transformers import SentenceTransformer

from medrag.application.ports.embedding_provider import (
    EmbeddingProvider,
)


class BGEM3EmbeddingProvider(
    EmbeddingProvider,
):
    """Embedding provider backed by BGE-M3."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
    ) -> None:
        if not model_name.strip():
            raise ValueError(
                "model_name cannot be empty.",
            )

        self._model = SentenceTransformer(
            model_name,
        )

    @property
    def dimension(
        self,
    ) -> int:
        """Embedding vector dimension."""

        dimension = cast(int | None, self._model.get_embedding_dimension())

        if dimension is None:
            raise ValueError(
                "Unable to determine embedding dimension.",
            )

        return dimension

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings."""

        if not texts:
            return []

        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True,
        )

        return cast(
            list[list[float]],
            embeddings.tolist(),
        )
