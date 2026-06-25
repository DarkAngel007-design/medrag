"""DTOs for the generation pipeline."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TokenUsage(BaseModel):
    """Token usage statistics for an LLM generation."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


class RetrievedContext(BaseModel):
    """Represents a retrieved context chunk."""

    chunk_id: UUID
    document_id: UUID
    content: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


class Citation(BaseModel):
    """Represents a citation used in the generated answer."""

    source_index: int
    document_id: UUID
    chunk_id: UUID

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


class GenerationConfig(BaseModel):
    """Configuration parameters controlling LLM answer generation."""

    model: str | None = None
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, gt=0)
    top_p: float = Field(default=1.0, gt=0.0, le=1.0)
    stream: bool = False

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


class GenerationRequest(BaseModel):
    """Request containing the question, retrieved context, and generation settings."""

    question: str
    contexts: list[RetrievedContext]
    config: GenerationConfig = Field(default_factory=GenerationConfig)

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


class GenerationResponse(BaseModel):
    """Response returned by the generation service."""

    answer: str
    citations: list[Citation]
    model: str
    usage: TokenUsage | None = None

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )
