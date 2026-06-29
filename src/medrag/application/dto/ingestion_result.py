from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class IngestionResult:
    """Result of a document ingestion operation."""

    document_id: UUID
    chunk_count: int
    already_indexed: bool = False
