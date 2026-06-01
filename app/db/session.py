from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

_engine = None
_SessionLocal = None


def _get_engine():
    """
    Return the SQLAlchemy engine, creating it on first call.

    Returns
    -------
    Engine
        The SQLAlchemy engine instance.

    """
    global _engine
    if _engine is None:
        settings = get_settings()
        connect_args = (
            {"check_same_thread": False}
            if settings.db_driver == "sqlite"
            else {}
        )
        _engine = create_engine(
            settings.database_url,
            connect_args=connect_args,
            echo=settings.debug,
        )
    return _engine


def _get_session_local():
    """
    Return the session maker, creating it on first call.

    Returns
    -------
    sessionmaker
        The SQLAlchemy session maker.

    """
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=_get_engine()
        )
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Yield a database session for dependency injection.

    Yields
    ------
    Session
        A SQLAlchemy database session.

    """
    db = _get_session_local()()
    try:
        yield db
    finally:
        db.close()
