"""API schemas for generation endpoints."""

from pydantic import BaseModel, ConfigDict, Field


class GenerateRequest(BaseModel):
    """Request body for the RAG generation endpoint."""

    question: str = Field(
        min_length=1,
        description="Question to answer using retrieved biomedical evidence.",
    )

    model_config = ConfigDict(
        extra="forbid",
    )
