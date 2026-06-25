from __future__ import annotations

from uuid import UUID

from medrag.domain.entities.document import Document
from medrag.domain.exceptions import DocumentNotFoundError
from medrag.domain.repositories.document_repository import (
    DocumentRepository,
)


class InMemoryDocumentRepository(DocumentRepository):
    """In-memory implementation of DocumentRepository."""

    def __init__(self) -> None:
        self._documents: dict[UUID, Document] = {}

    async def save(
        self,
        document: Document,
    ) -> None:
        self._documents[document.id] = document

    async def get_by_id(
        self,
        document_id: UUID,
    ) -> Document:
        try:
            return self._documents[document_id]

        except KeyError as exc:
            raise DocumentNotFoundError(f"Document '{document_id}' not found.") from exc

    async def delete(
        self,
        document_id: UUID,
    ) -> None:
        self._documents.pop(
            document_id,
            None,
        )

    async def exists(
        self,
        document_id: UUID,
    ) -> bool:
        return document_id in self._documents
