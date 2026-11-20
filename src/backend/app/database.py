from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base
from app.services.config import get_database_config

db_config = get_database_config()

DATABASE_URL = URL.create(
    drivername="mariadb+mariadbconnector",
    username=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
    port=db_config["port"],
    database=db_config["database"],
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """Provide a database session for a request."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()