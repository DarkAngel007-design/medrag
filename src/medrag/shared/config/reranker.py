from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RerankerSettings(BaseSettings):
    """Configuration for the reranker model."""

    model_config = SettingsConfigDict(
        env_prefix="RERANKER__",
        frozen=True,
    )

    model_name: str = Field(
        default="BAAI/bge-reranker-v2-m3",
    )

    use_fp16: bool = Field(
        default=True,
    )
