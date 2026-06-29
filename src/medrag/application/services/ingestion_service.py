from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from medrag.application.dto.ingestion_result import IngestionResult
from medrag.application.ports.document_fingerprinter import DocumentFingerprinter
from medrag.application.ports.document_parser import DocumentParser
from medrag.application.ports.indexing_service import IndexingService
from medrag.application.ports.text_chunker import TextChunker
from medrag.domain.entities.document import Document
from medrag.domain.repositories.document_repository import (
    DocumentRepository,
)


class IngestionService:
    """Application service responsible for document ingestion."""

    def __init__(
        self,
        document_repository: DocumentRepository,
        document_parser: DocumentParser,
        text_chunker: TextChunker,
        indexing_service: IndexingService,
        document_fingerprinter: DocumentFingerprinter,
    ) -> None:
        self._document_repository = document_repository
        self._document_parser = document_parser
        self._text_chunker = text_chunker
        self._indexing_service = indexing_service
        self._document_fingerprinter = document_fingerprinter

    async def ingest(
        self,
        content: bytes,
        source: str,
        title: str | None = None,
    ) -> IngestionResult:
        """Ingest a document into the system."""

        fingerprint = await self._document_fingerprinter.fingerprint(
            content,
        )

        existing_document = await self._document_repository.get_by_fingerprint(
            fingerprint,
        )

        if existing_document is not None:
            return IngestionResult(
                document_id=existing_document.id,
                chunk_count=0,
                already_indexed=True,
            )

        text = await self._document_parser.parse(content)

        now = datetime.now(UTC)

        document = Document(
            id=uuid4(),
            source=source,
            fingerprint=fingerprint,
            content=text,
            created_at=now,
            updated_at=now,
            title=title,
        )

        chunks = await self._text_chunker.chunk(document)

        await self._document_repository.save(document)

        await self._indexing_service.index(chunks)

        return IngestionResult(
            document_id=document.id,
            chunk_count=len(chunks),
            already_indexed=False,
        )
