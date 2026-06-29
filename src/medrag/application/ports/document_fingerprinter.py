from __future__ import annotations

from abc import ABC, abstractmethod

from medrag.domain.value_objects import (
    DocumentFingerprint,
)


class DocumentFingerprinter(ABC):
    """Generates stable document fingerprints."""

    @abstractmethod
    async def fingerprint(
        self,
        content: bytes,
    ) -> DocumentFingerprint:
        """Generate a fingerprint for document contents."""
