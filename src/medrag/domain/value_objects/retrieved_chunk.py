from __future__ import annotations

from dataclasses import dataclass

from medrag.domain.entities.chunk import Chunk
from medrag.domain.exceptions import DomainError


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    """Represents a chunk returned by a retrieval operation."""

    chunk: Chunk
    score: float
    rank: int

    def __post_init__(self) -> None:
        """Validate retrieval result."""

        if self.rank < 1:
            raise DomainError("Rank must be greater than or equal to 1.")
