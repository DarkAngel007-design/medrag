from pydantic_settings import BaseSettings, SettingsConfigDict

from .api import APISettings
from .database import DatabaseSettings
from .llm import LLMSettings
from .logging import LoggingSettings
from .prompts import PromptSettings
from .reranker import RerankerSettings
from .retrieval import RetrievalSettings
from .vector_db import VectorDBSettings


class Settings(BaseSettings):
    """
    Root application settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
    )

    api: APISettings = APISettings()
    database: DatabaseSettings = DatabaseSettings()
    llm: LLMSettings = LLMSettings()
    logging: LoggingSettings = LoggingSettings()
    retrieval: RetrievalSettings = RetrievalSettings()
    vector_db: VectorDBSettings = VectorDBSettings()
    prompts: PromptSettings = PromptSettings()
    reranker: RerankerSettings = RerankerSettings()


settings = Settings()
