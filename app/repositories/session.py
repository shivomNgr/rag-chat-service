from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import ChatSession
from app.models.session import ChatSessionCreate, ChatSessionUpdate, ChatSessionResponse
from app.repositories.base import BaseRepository


class ChatSessionRepository(BaseRepository[ChatSession, ChatSessionCreate, ChatSessionUpdate, ChatSessionResponse]):
    """Repository for managing chat sessions.
    Inherits from BaseRepository to provide CRUD operations for ChatSession model.
    Attributes:
        db (AsyncSession): The database session to use for operations.
    """
    
    def __init__(self, db: AsyncSession):
        """Initializes the ChatSessionRepository with the database session.
        Args:
            db (AsyncSession): The database session to use for operations.
        """
        super().__init__(ChatSession, db, ChatSessionResponse)