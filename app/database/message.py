# app/database/models/message.py
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
import uuid
from app.database.base import Base
from app.utils.helper import utcnow_naive

class Message(Base):
    """
        Model representing a chat message in a session.
        This model stores the details of a message sent in a chat session, including the sender,
        content, context, and timestamp.
    """
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False
    )
    sender = Column(String, nullable=False)
    content = Column(String, nullable=False)
    context = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=utcnow_naive)