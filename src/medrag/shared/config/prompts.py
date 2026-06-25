"""Prompt template configuration."""

from pydantic import BaseModel, ConfigDict


class PromptSettings(BaseModel):
    """Configuration for prompt templates."""

    model_config = ConfigDict(frozen=True)

    system_template: str = "system_prompt.txt"

    evaluation_template: str = "evaluation_prompt.txt"

    query_rewrite_template: str = "query_rewrite_prompt.txt"

    hyde_template: str = "hyde_prompt.txt"
