from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for persistent backend tables."""


engine = None
SessionLocal: sessionmaker[Session]


def _connect_args(database_url: str) -> dict:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def _ensure_sqlite_parent(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return
    sqlite_path = Path(database_url.replace("sqlite:///", "", 1))
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)


def configure_database(database_url: str | None = None) -> None:
    """
    Configure the SQLAlchemy engine and session factory.

    对应需求：
    - REQ-008 后台权限、版本化知识库与数据库持久化
    """
    global engine, SessionLocal
    if engine is not None:
        engine.dispose()
    url = database_url or settings.database_url
    _ensure_sqlite_parent(url)
    engine = create_engine(url, connect_args=_connect_args(url), pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


def init_db() -> None:
    """Create all persistence tables if they do not exist."""
    from app.models import persistence  # noqa: F401

    if engine is None:
        configure_database()
    Base.metadata.create_all(bind=engine)


def reset_database(database_url: str) -> None:
    """Reset a test database. Production code should use init_db()."""
    from app.models import persistence  # noqa: F401

    configure_database(database_url)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def new_session() -> Session:
    """Create a database session bound to the currently configured engine."""
    return SessionLocal()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session."""
    db = new_session()
    try:
        yield db
    finally:
        db.close()


configure_database()
