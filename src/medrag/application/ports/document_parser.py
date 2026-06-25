from __future__ import annotations

from abc import ABC, abstractmethod


class DocumentParser(ABC):
    """Extract text from a document."""

    @abstractmethod
    async def parse(
        self,
        content: bytes,
    ) -> str:
        """Extract text from document bytes."""
