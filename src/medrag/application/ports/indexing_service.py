from __future__ import annotations

from abc import ABC, abstractmethod

from medrag.domain.entities.chunk import Chunk


class IndexingService(ABC):
    """Makes chunks searchable."""

    @abstractmethod
    async def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        """Index chunks for retrieval."""
