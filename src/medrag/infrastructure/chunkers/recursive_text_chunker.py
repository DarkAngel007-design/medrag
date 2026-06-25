from __future__ import annotations

from uuid import uuid4

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from medrag.application.ports.text_chunker import (
    TextChunker,
)
from medrag.domain.entities.chunk import Chunk
from medrag.domain.entities.document import Document


class RecursiveTextChunker(TextChunker):
    """Chunk documents using recursive character splitting."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    async def chunk(
        self,
        document: Document,
    ) -> list[Chunk]:
        """Split a document into retrievable chunks."""

        texts = self._splitter.split_text(
            document.content,
        )

        chunks: list[Chunk] = []

        for index, text in enumerate(texts):
            chunks.append(
                Chunk(
                    id=uuid4(),
                    document_id=document.id,
                    text=text,
                    chunk_index=index,
                    metadata=dict(document.metadata),
                )
            )

        return chunks
