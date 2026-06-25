from uuid import UUID

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response returned after document ingestion."""

    document_id: UUID
    chunk_count: int
