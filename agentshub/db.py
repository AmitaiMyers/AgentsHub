"""Database engine, session factory and transaction scope."""
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


def utcnow() -> datetime:
    """Naive UTC timestamp; every stored datetime uses this convention."""
    return datetime.now(UTC).replace(tzinfo=None)


class Database:
    def __init__(self, url: str):
        connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
        self.engine = create_engine(url, connect_args=connect_args)
        self._session_factory = sessionmaker(self.engine, expire_on_commit=False)

    def create_schema(self) -> None:
        from agentshub import models  # noqa: F401  (registers tables on Base.metadata)

        Base.metadata.create_all(self.engine)

    @contextmanager
    def transaction(self) -> Iterator[Session]:
        """Commit on success, roll back when an exception leaves the block."""
        with self._session_factory.begin() as session:
            yield session
