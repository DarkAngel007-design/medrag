from __future__ import annotations

import litellm
from litellm.exceptions import APIError

from medrag.application.dto.generation import (
    GenerationConfig,
    GenerationResponse,
    TokenUsage,
)
from medrag.application.ports.llm_provider import LLMProvider
from medrag.shared.config.llm import LLMSettings


class LLMGenerationError(RuntimeError):
    """Raised when the configured LLM fails to generate a response."""


class LiteLLMProvider(LLMProvider):
    """LiteLLM implementation of the LLMProvider interface."""

    def __init__(
        self,
        settings: LLMSettings,
    ) -> None:
        self._settings = settings

    def _resolve_model(
        self,
        config: GenerationConfig,
    ) -> str:
        return config.model or self._settings.model_name

    def _resolve_temperature(
        self,
        config: GenerationConfig,
    ) -> float:
        return config.temperature

    def _resolve_max_tokens(
        self,
        config: GenerationConfig,
    ) -> int:
        return (
            config.max_tokens
            if config.max_tokens is not None
            else self._settings.max_tokens
        )

    async def generate(
        self,
        prompt: str,
        config: GenerationConfig,
    ) -> GenerationResponse:
        """Generate a response using LiteLLM."""

        try:
            response = await litellm.acompletion(
                model=self._resolve_model(config),
                api_key=(
                    self._settings.api_key.get_secret_value()
                    if self._settings.api_key
                    else None
                ),
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=self._resolve_temperature(config),
                max_tokens=self._resolve_max_tokens(config),
                top_p=config.top_p,
                timeout=self._settings.timeout,
            )

        except APIError as exc:
            raise LLMGenerationError("Failed to generate LLM response.") from exc

        usage = None

        if response.usage is not None:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )

        return GenerationResponse(
            answer=response.choices[0].message.content,
            citations=[],
            model=response.model,
            usage=usage,
        )
