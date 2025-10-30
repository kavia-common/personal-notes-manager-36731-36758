from typing import Generator
import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Database URL - use env var if provided, else default to local SQLite file
DEFAULT_DB_PATH = os.getenv("NOTES_DB_PATH", "notes.db")
DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# For SQLite, ensure correct connect args
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

# Create SQLAlchemy/SQLModel engine
engine = create_engine(DB_URL, echo=False, connect_args=connect_args)


def init_db() -> None:
    """
    Initialize the database by creating tables if they don't exist.
    """
    # Create all tables registered with SQLModel metadata
    SQLModel.metadata.create_all(engine)


# PUBLIC_INTERFACE
def get_session() -> Generator[Session, None, None]:
    """Provide a database session for dependency injection."""
    with Session(engine) as session:
        yield session
