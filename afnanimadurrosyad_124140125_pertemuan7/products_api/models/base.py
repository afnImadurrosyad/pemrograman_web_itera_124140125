from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer

from .meta import Base


def utc_now():
    return datetime.now(timezone.utc)


class BaseModel(Base):
    """Base model class for all models."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(DateTime, default=utc_now)

    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
