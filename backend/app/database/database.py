import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
from app.config import settings

# Determine database URL with fallback to SQLite for local test/dev without PostgreSQL
raw_db_url = settings.DATABASE_URL or os.getenv("DATABASE_URL", "")

if not raw_db_url:
    # Default fallback sqlite for local testing if Neon DB URL is not set
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
else:
    # Ensure correct dialect prefix for SQLAlchemy 2.0 + psycopg3
    if raw_db_url.startswith("postgres://"):
        DATABASE_URL = raw_db_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw_db_url.startswith("postgresql://") and not raw_db_url.startswith("postgresql+psycopg://"):
        DATABASE_URL = raw_db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    else:
        DATABASE_URL = raw_db_url
    
    if "sqlite" in DATABASE_URL:
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )
    else:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
