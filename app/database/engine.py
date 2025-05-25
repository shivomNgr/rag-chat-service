# app/database/engine.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL not set in environment variables")
    raise ValueError("DATABASE_URL not set")

try:
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={"server_settings": {"application_name": "rag_chat_service"}}
    )
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db():
    """
    Dependency that provides a database session for FastAPI routes.
    This function creates a new database session for each request and ensures it is properly closed after use.
    Yields:
        AsyncSession: A database session for the request.
    Raises:
        Exception: If an error occurs during session creation or rollback.
    """
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        await session.close()
        