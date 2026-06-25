"""Utilities for loading prompt templates."""

from __future__ import annotations

from pathlib import Path


class PromptTemplateLoader:
    """Loads prompt templates from the templates directory."""

    _TEMPLATE_DIRECTORY = Path(__file__).parent / "templates"

    @classmethod
    def load(
        cls,
        template_name: str,
    ) -> str:
        """Load a prompt template by name."""

        template_path = cls._TEMPLATE_DIRECTORY / template_name

        return template_path.read_text(
            encoding="utf-8",
        ).strip()
