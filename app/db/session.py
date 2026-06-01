from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, echo=settings.debug)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Yield a database session for dependency injection.

    Yields
    ------
    Session
        A SQLAlchemy database session.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
