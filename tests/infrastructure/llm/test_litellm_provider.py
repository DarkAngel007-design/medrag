from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from medrag.application.dto.generation import GenerationConfig
from medrag.infrastructure.llm.litellm_provider import (
    LiteLLMProvider,
    LLMGenerationError,
)
from medrag.shared.config.llm import LLMSettings


@pytest.fixture
def provider() -> LiteLLMProvider:
    settings = LLMSettings(
        model_name="gpt-5.4-mini",
        max_tokens=1024,
        temperature=0.0,
    )
    return LiteLLMProvider(settings)


@patch("litellm.acompletion", new_callable=AsyncMock)
async def test_generate_success(
    mock_completion: AsyncMock,
    provider: LiteLLMProvider,
) -> None:
    response = MagicMock(name="LiteLLMResponse")

    response.model = "gpt-5.4-mini"

    response.choices = [
        MagicMock(
            message=MagicMock(
                content="Medical answer",
            )
        )
    ]

    response.usage = MagicMock(
        prompt_tokens=100,
        completion_tokens=20,
        total_tokens=120,
    )

    mock_completion.return_value = response

    result = await provider.generate(
        prompt="What is aspirin?",
        config=GenerationConfig(),
    )

    assert result.answer == "Medical answer"
    assert result.model == "gpt-5.4-mini"

    assert result.usage is not None
    assert result.usage.prompt_tokens == 100
    assert result.usage.completion_tokens == 20
    assert result.usage.total_tokens == 120

    assert result.citations == []

    mock_completion.assert_awaited_once()


@patch("litellm.acompletion", new_callable=AsyncMock)
async def test_generate_uses_configuration(
    mock_completion: AsyncMock,
    provider: LiteLLMProvider,
) -> None:
    response = MagicMock(name="LiteLLMResponse")

    response.model = "gpt-5.4-mini"

    response.choices = [
        MagicMock(
            message=MagicMock(
                content="Answer",
            )
        )
    ]

    response.usage = None

    mock_completion.return_value = response

    config = GenerationConfig(
        model="gpt-5.4-mini",
        temperature=0.5,
        max_tokens=512,
        top_p=0.8,
    )

    await provider.generate(
        prompt="Hello",
        config=config,
    )

    kwargs = mock_completion.await_args.kwargs

    assert kwargs["model"] == "gpt-5.4-mini"
    assert kwargs["temperature"] == 0.5
    assert kwargs["max_tokens"] == 512
    assert kwargs["top_p"] == 0.8
    assert kwargs["timeout"] == provider._settings.timeout


@patch("litellm.acompletion", new_callable=AsyncMock)
async def test_generate_uses_default_settings(
    mock_completion: AsyncMock,
    provider: LiteLLMProvider,
) -> None:
    response = MagicMock(name="LiteLLMResponse")

    response.model = "gpt-5.4-mini"

    response.choices = [
        MagicMock(
            message=MagicMock(
                content="Answer",
            )
        )
    ]

    response.usage = None

    mock_completion.return_value = response

    await provider.generate(
        prompt="Hello",
        config=GenerationConfig(),
    )

    kwargs = mock_completion.await_args.kwargs

    assert kwargs["model"] == "gpt-5.4-mini"
    assert kwargs["max_tokens"] == 1024


@patch("litellm.acompletion", new_callable=AsyncMock)
async def test_generate_without_usage(
    mock_completion: AsyncMock,
    provider: LiteLLMProvider,
) -> None:
    response = MagicMock(name="LiteLLMResponse")

    response.model = "gpt-5.4-mini"

    response.choices = [
        MagicMock(
            message=MagicMock(
                content="Answer",
            )
        )
    ]

    response.usage = None

    mock_completion.return_value = response

    result = await provider.generate(
        prompt="Hello",
        config=GenerationConfig(),
    )

    assert result.usage is None


@patch("litellm.acompletion", new_callable=AsyncMock)
async def test_generate_wraps_exception(
    mock_completion: AsyncMock,
    provider: LiteLLMProvider,
) -> None:
    mock_completion.side_effect = RuntimeError("Boom")

    with pytest.raises(LLMGenerationError):
        await provider.generate(
            prompt="Hello",
            config=GenerationConfig(),
        )
