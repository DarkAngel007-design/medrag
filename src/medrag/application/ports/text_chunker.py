from __future__ import annotations

from abc import ABC, abstractmethod

from medrag.domain.entities.chunk import Chunk
from medrag.domain.entities.document import Document


class TextChunker(ABC):
    """Split documents into retrievable chunks."""

    @abstractmethod
    async def chunk(
        self,
        document: Document,
    ) -> list[Chunk]:
        """Split a document into chunks."""
