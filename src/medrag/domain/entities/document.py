from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from medrag.domain.exceptions import InvalidDocumentError


@dataclass(slots=True)
class Document:
    """Represents a source document in the MedRAG domain."""

    id: UUID
    source: str
    content: str
    created_at: datetime
    updated_at: datetime
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def _validate_non_empty(value: str, field_name: str) -> str:
        """Validate and normalize a required string field."""

        value = value.strip()

        if not value:
            raise InvalidDocumentError(f"Document {field_name} cannot be empty.")

        return value

    def __post_init__(self) -> None:
        """Validate domain invariants after initialization."""

        self.source = self._validate_non_empty(self.source, "source")
        self.content = self._validate_non_empty(self.content, "content")
