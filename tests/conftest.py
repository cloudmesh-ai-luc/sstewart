
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

from app.database import get_db
from app.main import app
from app.models import Base, Operator
from app.services.config import get_database_config
from app.services.tokens import create_access_token

TEST_DATABASE_NAME = "911_analysis_test"


@pytest.fixture(scope="session")
def test_engine():
    """Create an engine that connects exclusively to the test database."""

    config = get_database_config()

    database_url = URL.create(
        drivername="mariadb+mariadbconnector",
        username=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
        database=TEST_DATABASE_NAME,
    )

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        echo=False,
    )

    # Safety check: never create test tables in the development database.
    assert engine.url.database == TEST_DATABASE_NAME
    assert engine.url.database.endswith("_test")

    Base.metadata.create_all(bind=engine)

    yield engine

    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    """Give each test an isolated database transaction."""

    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()



@pytest.fixture
def client(db_session):
    """Provide an authenticated FastAPI test client using the test database."""

    # Create a test administrator in the isolated test database.
    test_operator = Operator(
        email="test-admin@example.com",
        password_hash="test-password-hash",
        role="ADMIN",
        is_active=True,
    )

    db_session.add(test_operator)
    db_session.flush()

    # Generate a real JWT for the test administrator.
    access_token = create_access_token(test_operator.id)

    # Override the database dependency for all API requests.
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(
            app,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
        ) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.pop(get_db, None)
