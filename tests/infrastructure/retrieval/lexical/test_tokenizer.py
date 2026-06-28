from __future__ import annotations

import pytest

from medrag.infrastructure.retrieval.lexical.tokenizer import (
    BM25Tokenizer,
)


@pytest.fixture
def tokenizer() -> BM25Tokenizer:
    """Create a BM25 tokenizer instance."""
    return BM25Tokenizer()


def test_tokenize_simple_sentence(
    tokenizer: BM25Tokenizer,
) -> None:
    """Tokenize a simple English sentence."""

    tokens = tokenizer.tokenize("Cancer is a disease.")

    assert tokens == [
        "cancer",
        "is",
        "a",
        "disease",
    ]


def test_tokenize_empty_string(
    tokenizer: BM25Tokenizer,
) -> None:
    """Tokenizing an empty string should return no tokens."""

    assert tokenizer.tokenize("") == []


def test_tokenize_whitespace(
    tokenizer: BM25Tokenizer,
) -> None:
    """Whitespace-only input should return no tokens."""

    assert tokenizer.tokenize("     ") == []


def test_tokenize_normalizes_case(
    tokenizer: BM25Tokenizer,
) -> None:
    """Tokenizer should normalize tokens to lowercase."""

    tokens = tokenizer.tokenize("Cancer CANCER cancer")

    assert tokens == [
        "cancer",
        "cancer",
        "cancer",
    ]


def test_tokenize_biomedical_text(
    tokenizer: BM25Tokenizer,
) -> None:
    """Tokenizer should preserve important biomedical terms."""

    tokens = tokenizer.tokenize("BRCA1 mutations increase breast cancer risk.")

    assert "brca1" in tokens
    assert "mutations" in tokens
    assert "breast" in tokens
    assert "cancer" in tokens
    assert "risk" in tokens


def test_tokenize_handles_punctuation(
    tokenizer: BM25Tokenizer,
) -> None:
    """Tokenizer should ignore punctuation."""

    tokens = tokenizer.tokenize("COVID-19, influenza; and RSV.")

    assert "covid" in tokens or "covid-19" in tokens
    assert "influenza" in tokens
    assert "rsv" in tokens
