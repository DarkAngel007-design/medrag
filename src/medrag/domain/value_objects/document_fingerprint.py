from __future__ import annotations

from dataclasses import dataclass

from medrag.domain.exceptions import DomainError


@dataclass(frozen=True, slots=True)
class DocumentFingerprint:
    """Stable fingerprint uniquely identifying a document's contents."""

    value: str

    def __post_init__(self) -> None:
        """Validate the fingerprint."""

        if not self.value:
            raise DomainError("Document fingerprint cannot be empty.")
