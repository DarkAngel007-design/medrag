from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from medrag.domain.exceptions import InvalidChunkError


@dataclass(slots=True)
class Chunk:
    """Represents the smallest retrievable unit of a document."""

    id: UUID
    document_id: UUID
    text: str
    chunk_index: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate domain invariants after initialization."""

        self.text = self._validate_non_empty(
            self.text,
            "text",
        )

        if self.chunk_index < 0:
            raise InvalidChunkError("Chunk index cannot be negative.")

    @staticmethod
    def _validate_non_empty(value: str, field_name: str) -> str:
        """Validate and normalize a required string field."""

        value = value.strip()

        if not value:
            raise InvalidChunkError(f"Chunk {field_name} cannot be empty.")

        return value
