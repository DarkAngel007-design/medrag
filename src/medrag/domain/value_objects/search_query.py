from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from medrag.domain.exceptions import InvalidSearchQueryError


@dataclass(frozen=True, slots=True)
class SearchQuery:
    """Represents a retrieval request."""

    query: str
    top_k: int = 10
    filters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate domain invariants."""

        query = self.query.strip()

        if not query:
            raise InvalidSearchQueryError("Search query cannot be empty.")

        if self.top_k <= 0:
            raise InvalidSearchQueryError("top_k must be greater than zero.")

        object.__setattr__(self, "query", query)
