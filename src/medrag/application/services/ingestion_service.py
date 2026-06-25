from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from medrag.application.dto.ingestion_result import IngestionResult
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
    ) -> None:
        self._document_repository = document_repository
        self._document_parser = document_parser
        self._text_chunker = text_chunker
        self._indexing_service = indexing_service

    async def ingest(
        self,
        content: bytes,
        source: str,
        title: str | None = None,
    ) -> IngestionResult:
        """Ingest a document into the system."""

        text = await self._document_parser.parse(content)

        now = datetime.now(UTC)

        document = Document(
            id=uuid4(),
            source=source,
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
        )
