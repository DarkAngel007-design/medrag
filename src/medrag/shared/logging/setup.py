import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from medrag.shared.config.settings import settings

from .formatter import MedRAGFormatter


def configure_logging() -> None:
    """
    Configure application logging.

    This function should be called exactly once during
    application startup.
    """

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    formatter = MedRAGFormatter()

    # -----------------------------
    # Console Handler
    # -----------------------------
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # -----------------------------
    # File Handler
    # -----------------------------
    log_path = Path(settings.logging.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    root_logger.setLevel(settings.logging.level)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
