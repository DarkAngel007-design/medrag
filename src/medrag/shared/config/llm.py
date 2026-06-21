from pydantic import Field, SecretStr

from .base import BaseConfig


class LLMSettings(BaseConfig):
    """
    LLM configuration.
    """

    provider: str = Field(default="openai")

    api_key: SecretStr | None = None

    model_name: str = Field(default="gpt-4.1")

    temperature: float = Field(
        default=0.0,
        ge=0,
        le=2,
    )
