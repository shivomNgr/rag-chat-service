# app/database/models/session.py
import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base
from app.utils.helper import utcnow_naive


class ChatSession(Base):
    """Model representing a chat session.
    This model stores the details of a chat session, including its name, user ID,
    favorite status, and timestamps for creation and last update.
    Attributes:
        id (UUID): Unique identifier for the chat session.
        name (str): Name of the chat session.
        user_id (str): Identifier for the user associated with the session.
        is_favorite (bool): Indicates if the session is marked as favorite.
        created_at (datetime): Timestamp when the session was created.
        updated_at (datetime): Timestamp when the session was last updated.
    """
    __tablename__ = "chat_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utcnow_naive)
    updated_at = Column(DateTime(timezone=True), default=utcnow_naive, onupdate=utcnow_naive)