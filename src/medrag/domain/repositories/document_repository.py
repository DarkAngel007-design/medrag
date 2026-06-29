from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from medrag.domain.entities.document import Document
from medrag.domain.value_objects import DocumentFingerprint


class DocumentRepository(ABC):
    """Repository interface for document persistence."""

    @abstractmethod
    async def save(
        self,
        document: Document,
    ) -> None:
        """Persist a document."""

    @abstractmethod
    async def get_by_id(
        self,
        document_id: UUID,
    ) -> Document:
        """Retrieve a document by its identifier."""

    @abstractmethod
    async def delete(
        self,
        document_id: UUID,
    ) -> None:
        """Delete a document."""

    @abstractmethod
    async def exists(
        self,
        document_id: UUID,
    ) -> bool:
        """Check whether a document exists."""

    @abstractmethod
    async def get_by_fingerprint(
        self,
        fingerprint: DocumentFingerprint,
    ) -> Document | None:
        """Return the document with the given fingerprint, if it exists."""
