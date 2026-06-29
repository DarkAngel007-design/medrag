from __future__ import annotations

import hashlib

from medrag.application.ports import (
    DocumentFingerprinter,
)
from medrag.domain.value_objects import (
    DocumentFingerprint,
)


class SHA256DocumentFingerprinter(
    DocumentFingerprinter,
):
    """SHA-256 implementation of the document fingerprinter."""

    async def fingerprint(
        self,
        content: bytes,
    ) -> DocumentFingerprint:
        return DocumentFingerprint(
            hashlib.sha256(content).hexdigest(),
        )
