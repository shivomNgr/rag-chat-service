# app/database/utils.py
import logging
from app.database.base import Base
from .engine import engine

logger = logging.getLogger(__name__)

async def init_db():
    """Initialize the database by creating all tables.
    This function connects to the database and creates all tables defined in the Base metadata.
    It should be called during application startup to ensure the database schema is ready for use.
    Raises:
        Exception: If an error occurs during the database initialization process.
    """
    logger.info("Initializing database...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise