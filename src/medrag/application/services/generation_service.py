"""Application service for orchestrating answer generation."""

from __future__ import annotations

from medrag.application.dto.generation import (
    Citation,
    GenerationRequest,
    GenerationResponse,
)
from medrag.application.ports.llm_provider import LLMProvider
from medrag.application.ports.prompt_builder import PromptBuilder


class GenerationService:
    """Coordinates prompt construction and LLM-based answer generation."""

    def __init__(
        self,
        llm_provider: LLMProvider,
        prompt_builder: PromptBuilder,
    ) -> None:
        """Initialize the generation service."""
        if llm_provider is None:
            raise ValueError("llm_provider cannot be None")

        if prompt_builder is None:
            raise ValueError("prompt_builder cannot be None")

        self._llm_provider = llm_provider
        self._prompt_builder = prompt_builder

    async def generate_answer(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a grounded answer for the supplied request."""

        prompt: str = self._prompt_builder.build(request)

        response: GenerationResponse = await self._llm_provider.generate(
            prompt=prompt,
            config=request.config,
        )

        citations: list[Citation] = [
            Citation(
                source_index=source_index,
                document_id=context.document_id,
                chunk_id=context.chunk_id,
            )
            for source_index, context in enumerate(
                request.contexts,
                start=1,
            )
        ]

        return response.model_copy(
            update={
                "citations": citations,
            }
        )
