from pydantic import BaseModel, ConfigDict

from .api import APISettings
from .database import DatabaseSettings
from .llm import LLMSettings
from .logging import LoggingSettings
from .prompts import PromptSettings
from .retrieval import RetrievalSettings
from .vector_db import VectorDBSettings


class Settings(BaseModel):
    """
    Root application settings.
    """

    model_config = ConfigDict(frozen=True)

    api: APISettings = APISettings()
    database: DatabaseSettings = DatabaseSettings()
    llm: LLMSettings = LLMSettings()
    logging: LoggingSettings = LoggingSettings()
    retrieval: RetrievalSettings = RetrievalSettings()
    vector_db: VectorDBSettings = VectorDBSettings()
    prompts: PromptSettings = PromptSettings()


settings = Settings()
