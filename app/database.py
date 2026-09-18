"""Database configuration for the DealerOps application."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Store the SQLite database in a file named dealerops.db.
# Later, this address can be replaced with an AWS RDS database address.
DATABASE_URL = "sqlite:///./dealerops.db"

# Create the connection between SQLAlchemy and SQLite.
# SQLite requires check_same_thread=False when used with FastAPI.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create database sessions used to read and save information.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Database models will inherit from this base class.
Base = declarative_base()


def get_database():
    """Provide a database session and close it after each request."""

    database = SessionLocal()

    try:
        yield database
    finally:
        database.close()
