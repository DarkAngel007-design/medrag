from pydantic import Field

from .base import BaseConfig


class APISettings(BaseConfig):
    """
    API configuration.
    """

    host: str = Field(
        default="0.0.0.0",
        description="Host address",
    )

    port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Application port",
    )

    debug: bool = Field(
        default=False,
        description="Debug mode",
    )

    app_name: str = "MedRAG"

    version: str = "0.1.0"
