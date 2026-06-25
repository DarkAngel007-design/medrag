from abc import ABC, abstractmethod

from medrag.application.dto.generation import (
    GenerationConfig,
    GenerationResponse,
)


class LLMProvider(ABC):
    """Interface for LLM providers."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        config: GenerationConfig,
    ) -> GenerationResponse:
        """Generate a response from the supplied prompt."""
