"""Default implementation of the prompt builder."""

from __future__ import annotations

from medrag.application.dto.generation import GenerationRequest
from medrag.application.ports.prompt_builder import PromptBuilder
from medrag.infrastructure.prompts.loader import PromptTemplateLoader


class DefaultPromptBuilder(PromptBuilder):
    """Build prompts for grounded biomedical question answering."""

    _CONTEXT_HEADER = "Context"
    _QUESTION_HEADER = "Question"
    _ANSWER_HEADER = "Answer"

    _SECTION_SEPARATOR = "=" * 80
    _SOURCE_SEPARATOR = "-" * 40

    def __init__(
        self,
        template_name: str = "system_prompt.txt",
    ) -> None:
        """Initialize the prompt builder."""

        self._system_prompt = PromptTemplateLoader.load(
            template_name,
        )

    def build(
        self,
        request: GenerationRequest,
    ) -> str:
        """Build a prompt for grounded answer generation."""

        context: str = self._format_contexts(request)
        question: str = self._format_question(request)

        return (
            f"{self._system_prompt}\n\n"
            f"{self._CONTEXT_HEADER}\n"
            f"{self._SECTION_SEPARATOR}\n"
            f"{context}\n\n"
            f"{self._QUESTION_HEADER}\n"
            f"{self._SECTION_SEPARATOR}\n"
            f"{question}\n\n"
            f"{self._ANSWER_HEADER}\n"
        )

    def _format_contexts(
        self,
        request: GenerationRequest,
    ) -> str:
        """Format retrieved contexts into numbered source blocks."""

        formatted_contexts: list[str] = []

        for index, context in enumerate(
            request.contexts,
            start=1,
        ):
            formatted_contexts.append(
                f"Source [{index}]\n" f"{self._SOURCE_SEPARATOR}\n" f"{context.content}"
            )

        return "\n\n".join(formatted_contexts)

    @staticmethod
    def _format_question(
        request: GenerationRequest,
    ) -> str:
        """Format the user question."""

        return request.question.strip()
