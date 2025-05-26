import logging
import uuid
from fastapi import APIRouter, Depends, Request, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.session import ChatSessionCreate, ChatSessionUpdate, ChatSessionResponse
from app.utils.auth import verify_api_key
from app.repositories.session import ChatSessionRepository

router = APIRouter()
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

@router.post("/sessions", response_model=ChatSessionResponse)
@limiter.limit("10/minute")
async def create_session(
    session_data: ChatSessionCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    ### Create a new chat session

    **Parameters:**
    - `session_data` (ChatSessionCreate): The data for the new chat session.
    - `request` (Request): The FastAPI request object.
    - `db` (AsyncSession): The database session dependency.
    - `api_key` (str): The API key for authentication.

    **Returns:**
    - `ChatSessionResponse`: The response model containing the created session.

    **Raises:**
    - `HTTPException`: If an error occurs during session creation.
    """

    repo = ChatSessionRepository(db)
    try:
        return await repo.create(session_data)
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create session")

@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
@limiter.limit("10/minute")
async def get_session(
    session_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    ### Retrieve a chat session by its ID

    **Parameters:**
    - `session_id` (str): The UUID of the session to retrieve.
    - `request` (Request): The FastAPI request object.
    - `db` (AsyncSession): The database session dependency.
    - `api_key` (str): The API key for authentication.

    **Returns:**
    - `ChatSessionResponse`: The response model containing the retrieved session.

    **Raises:**
    - `HTTPException`: If the session ID is invalid or if an error occurs during retrieval.
    """
    try:
        session_id_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session ID")
    repo = ChatSessionRepository(db)
    try:
        return await repo.get(session_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve session")

@router.put("/sessions/{session_id}", response_model=ChatSessionResponse)
@limiter.limit("10/minute")
async def update_session(
    session_id: str,
    session_data: ChatSessionUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    ### Update an existing chat session

    **Parameters:**
    - `session_id` (str): The UUID of the session to update.
    - `session_data` (ChatSessionUpdate): The updated data for the chat session.
    - `request` (Request): The FastAPI request object.
    - `db` (AsyncSession): The database session dependency.
    - `api_key` (str): The API key for authentication.

    **Returns:**
    - `ChatSessionResponse`: The response model containing the updated session.

    **Raises:**
    - `HTTPException`: If the session ID is invalid or if an error occurs during update.
    """

    try:
        session_id_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session ID")
    repo = ChatSessionRepository(db)
    try:
        return await repo.update(session_id, session_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating session: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update session")

@router.delete("/sessions/{session_id}")
@limiter.limit("10/minute")
async def delete_session(
    session_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    ### Delete a chat session by its ID

    **Parameters:**
    - `session_id` (str): The UUID of the session to delete.
    - `request` (Request): The FastAPI request object.
    - `db` (AsyncSession): The database session dependency.
    - `api_key` (str): The API key for authentication.

    **Returns:**
    - `dict`: A dictionary containing a success message.

    **Raises:**
    - `HTTPException`: If the session ID is invalid or if an error occurs during deletion.
    """

    try:
        session_id_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session ID")
    repo = ChatSessionRepository(db)
    try:
        return await repo.delete(session_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete session")