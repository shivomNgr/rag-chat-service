import logging
from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.message import Message, MessageResponse
from app.models.pagination import PaginatedMessages
from app.utils.auth import verify_api_key
from app.repositories.message import MessageRepository


router = APIRouter()
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
@limiter.limit("10/minute")
async def add_message(
    session_id: str,
    message_data: Message,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Add a new message to a chat session.
    Args:
        session_id (str): The UUID of the session to which the message belongs.
        message_data (Message): The message data to be added.
        request (Request): The FastAPI request object.
        db (AsyncSession): The database session dependency.
        api_key (str): The API key for authentication.
    Returns:
        MessageResponse: The response model containing the added message.
    Raises:
        HTTPException: If the session ID is invalid or if an error occurs during message creation.
    """
    repo = MessageRepository(db)
    message_data_dict = message_data.model_dump()
    message_data_dict["session_id"] = session_id
    return await repo.create(Message(**message_data_dict))

@router.get("/sessions/{session_id}/messages", response_model=PaginatedMessages)
@limiter.limit("10/minute")
async def get_messages(
    request: Request,
    session_id: str,
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Retrieve messages for a specific chat session with pagination.
    Args:
        session_id (str): The UUID of the session to retrieve messages for.
        page (int): The page number to retrieve (default is 1).
        page_size (int): The number of messages per page (default is 10).
        request (Request): The FastAPI request object.
        db (AsyncSession): The database session dependency.
        api_key (str): The API key for authentication.
    Returns:
        PaginatedMessages: A paginated response containing messages and metadata.
    Raises: 
        HTTPException: If the session ID is invalid or if an error occurs during retrieval.
    """
    repo = MessageRepository(db)
    return await repo.get_by_session_id(session_id, page, page_size)