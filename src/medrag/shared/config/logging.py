from typing import Literal

from pydantic import Field

from .base import BaseConfig


class LoggingSettings(BaseConfig):
    """
    Logging configuration.
    """

    level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = Field(default="INFO")

    json_logs: bool = Field(default=True)

    log_file: str = Field(default="logs/medrag.log")
