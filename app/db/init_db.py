from app.db.base import Base
from app.db.session import engine


def init_database() -> None:
    """
    Create all database tables defined by SQLAlchemy models.

    """
    Base.metadata.create_all(bind=engine)
