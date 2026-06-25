from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Generate vector embeddings for text."""

    @abstractmethod
    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for the supplied texts."""

    @property
    @abstractmethod
    def dimension(
        self,
    ) -> int:
        """Embedding dimension."""
