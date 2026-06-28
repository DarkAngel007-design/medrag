from __future__ import annotations

from typing import cast

from blingfire import text_to_words  # type: ignore[import-untyped]


class BM25Tokenizer:
    """Tokenizer for lexical retrieval."""

    def tokenize(
        self,
        text: str,
    ) -> list[str]:
        """
        Tokenize text into normalized word tokens.

        BlingFire performs Unicode-aware tokenization and
        punctuation handling suitable for BM25 indexing.
        """

        normalized = text.lower().strip()

        if not normalized:
            return []

        tokenized = cast(str, text_to_words(normalized))

        return [
            token
            for token in tokenized.split()
            if any(character.isalnum() for character in token)
        ]
