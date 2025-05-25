import logging
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

from app.database.message import Message as SQLAlchemyMessage
from app.models.message import Message, MessageResponse
from app.models.pagination import PaginatedMessages
from app.repositories.base import BaseRepository

logger = logging.getLogger(__name__)

class MessageRepository(BaseRepository[SQLAlchemyMessage, Message, Message, MessageResponse]):
    """
    A repository for managing messages in the database.
    This class provides methods to create, retrieve, and paginate messages associated with a session.
    Attributes:
        db (AsyncSession): The database session to use for operations.
    """
    def __init__(self, db: AsyncSession):
        """
        Initializes the MessageRepository with the database session.
        Args:
            db (AsyncSession): The database session to use for operations.
        """
        super().__init__(SQLAlchemyMessage, db, MessageResponse)


    async def get_by_session_id(self, session_id: str, page: int = 1, page_size: int = 10) -> PaginatedMessages:
        """
        Retrieves messages associated with a specific session ID, with pagination support.
        Args:
            session_id (str): The UUID of the session to retrieve messages for.
            page (int): The page number to retrieve (default is 1).
            page_size (int): The number of messages per page (default is 10).
        Returns:
            PaginatedMessages: A paginated response containing messages and metadata.
        Raises:
            HTTPException: If the session ID is invalid or if an error occurs during retrieval.
        """
        logger.debug(f"Retrieving messages for session ID: {session_id}, page: {page}, page_size: {page_size}")
        try:
            session_id_value = uuid.UUID(session_id)
            # Count total messages
            count_result = await self.db.execute(
                select(func.count()).select_from(self.model).filter(self.model.session_id == session_id_value)
            )
            total = count_result.scalar_one()

            # Fetch paginated messages
            result = await self.db.execute(
                select(self.model)
                .filter(self.model.session_id == session_id_value)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            messages = result.scalars().all()
            return PaginatedMessages(
                messages=[self.response_schema.model_validate(self._prepare_data(msg.__dict__)) for msg in messages],
                total=total,
                page=page,
                page_size=page_size
            )
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session ID")
        except Exception as e:
            logger.error(f"Error retrieving messages: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve messages")