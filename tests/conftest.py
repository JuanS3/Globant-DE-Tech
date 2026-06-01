import os

# Force SQLite in-memory for tests before any app imports
os.environ["DB_DRIVER"] = "sqlite"
os.environ["SQLITE_PATH"] = ":memory:"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app

# Clear cached settings so the env vars above take effect
get_settings.cache_clear()

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Create all tables before running tests and drop them after.

    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Session:
    """
    Yield a database session for testing.

    Yields
    ------
    Session
        A SQLAlchemy database session rolled back after each test.

    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session) -> TestClient:
    """
    Return a TestClient with overridden database dependency.

    Parameters
    ----------
    db_session : Session
        The database session fixture.

    Returns
    -------
    TestClient
        A FastAPI test client using the test database session.

    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
