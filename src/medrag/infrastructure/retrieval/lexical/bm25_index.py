from __future__ import annotations

from rank_bm25 import BM25Okapi  # type: ignore[import-untyped]

from medrag.domain.entities.chunk import Chunk

from .tokenizer import BM25Tokenizer


class BM25Index:
    """In-memory BM25 index."""

    def __init__(
        self,
        tokenizer: BM25Tokenizer,
    ) -> None:
        self._tokenizer = tokenizer
        self._chunks: list[Chunk] = []
        self._tokenized_corpus: list[list[str]] = []
        self._bm25: BM25Okapi | None = None

    def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        """Index chunks for lexical retrieval."""

        if not chunks:
            return

        self._chunks.extend(chunks)

        self._tokenized_corpus.extend(
            self._tokenizer.tokenize(chunk.text) for chunk in chunks
        )

        self._rebuild_index()

    def _rebuild_index(
        self,
    ) -> None:
        """Rebuild the BM25 index from the current corpus."""

        self._bm25 = BM25Okapi(
            self._tokenized_corpus,
        )

    def search(
        self,
        query: str,
        limit: int,
    ) -> list[tuple[Chunk, float]]:
        """Search the BM25 index."""

        if self._bm25 is None:
            return []

        query_tokens = self._tokenizer.tokenize(query)

        if not query_tokens:
            return []

        scores = self._bm25.get_scores(query_tokens)

        ranked = sorted(
            zip(
                self._chunks,
                scores,
                strict=True,
            ),
            key=lambda item: item[1],
            reverse=True,
        )

        return [(chunk, float(score)) for chunk, score in ranked if score > 0][:limit]
