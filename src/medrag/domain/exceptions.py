"""Domain-specific exceptions for the MedRAG domain."""


class DomainError(Exception):
    """Base class for all domain exceptions."""


class InvalidDocumentError(DomainError):
    """Raised when a document violates domain invariants."""


class InvalidChunkError(DomainError):
    """Raised when a chunk violates domain invariants."""


class InvalidSearchQueryError(DomainError):
    """Raised when a search query violates domain invariants."""


class InvalidRetrievedChunkError(DomainError):
    """Raised when a retrieved chunk violates domain invariants."""


class DocumentNotFoundError(DomainError):
    """Raised when a requested document does not exist."""


class DuplicateDocumentError(DomainError):
    """Raised when attempting to create a duplicate document."""


class RetrievalError(DomainError):
    """Raised when a retrieval operation cannot be completed."""
