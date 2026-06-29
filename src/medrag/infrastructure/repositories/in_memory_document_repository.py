from __future__ import annotations

from uuid import UUID

from medrag.domain.entities.document import Document
from medrag.domain.exceptions import DocumentNotFoundError
from medrag.domain.repositories.document_repository import (
    DocumentRepository,
)
from medrag.domain.value_objects import DocumentFingerprint


class InMemoryDocumentRepository(DocumentRepository):
    """In-memory implementation of DocumentRepository."""

    def __init__(self) -> None:
        self._documents: dict[UUID, Document] = {}
        self._fingerprints: dict[str, UUID] = {}

    async def save(
        self,
        document: Document,
    ) -> None:
        self._documents[document.id] = document
        self._fingerprints[document.fingerprint.value] = document.id

    async def get_by_id(
        self,
        document_id: UUID,
    ) -> Document:
        try:
            return self._documents[document_id]

        except KeyError as exc:
            raise DocumentNotFoundError(
                f"Document '{document_id}' not found.",
            ) from exc

    async def delete(
        self,
        document_id: UUID,
    ) -> None:
        document = self._documents.pop(
            document_id,
            None,
        )

        if document is not None:
            self._fingerprints.pop(
                document.fingerprint.value,
                None,
            )

    async def exists(
        self,
        document_id: UUID,
    ) -> bool:
        return document_id in self._documents

    async def get_by_fingerprint(
        self,
        fingerprint: DocumentFingerprint,
    ) -> Document | None:
        """Return the document with the given fingerprint, if it exists."""

        document_id = self._fingerprints.get(
            fingerprint.value,
        )

        if document_id is None:
            return None

        return self._documents[document_id]
