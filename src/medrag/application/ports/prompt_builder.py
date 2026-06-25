from abc import ABC, abstractmethod

from medrag.application.dto.generation import GenerationRequest


class PromptBuilder(ABC):
    """Interface for prompt construction."""

    @abstractmethod
    def build(
        self,
        request: GenerationRequest,
    ) -> str:
        """Build a prompt for answer generation."""
