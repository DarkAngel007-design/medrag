from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from medrag.infrastructure.database.base import Base


class DocumentModel(Base):
    """SQLAlchemy representation of a document."""

    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    fingerprint: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )

    source: Mapped[str] = mapped_column()

    title: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )
