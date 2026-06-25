from __future__ import annotations

import fitz  # type: ignore[import-untyped]

from medrag.application.ports.document_parser import (
    DocumentParser,
)


class PyMuPDFDocumentParser(DocumentParser):
    """Extract text from PDF documents using PyMuPDF."""

    async def parse(
        self,
        content: bytes,
    ) -> str:
        """Extract text from PDF bytes."""

        with fitz.open(
            stream=content,
            filetype="pdf",
        ) as document:

            pages: list[str] = []

            for page in document:
                pages.append(page.get_text())

        return "\n".join(pages)
