from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional, List, Dict

class Message(BaseModel):
    """Model representing a chat message in a session.
    Attributes:
        id (str): Unique identifier for the message.
        session_id (str): Identifier for the chat session.
        sender (str): Identifier for the sender of the message.
        content (str): Content of the message.
        context (Optional[Dict]): Additional context or metadata for the message.
        timestamp (datetime): Timestamp when the message was created.
    """
    sender: str
    content: str
    context: Optional[Dict] = None
    timestamp: datetime = datetime.now(timezone.utc)
    session_id: Optional[str] = None  # Added to accept session_id

class MessageResponse(BaseModel):
    """Response model for a chat message.
    Attributes:
        id (str): Unique identifier for the message.
        session_id (str): Identifier for the chat session.
        sender (str): Identifier for the sender of the message.
        content (str): Content of the message.
        context (Optional[Dict]): Additional context or metadata for the message.
        timestamp (datetime): Timestamp when the message was created.
    """
    id: str
    session_id: str
    sender: str
    content: str
    context: Optional[Dict]
    timestamp: datetime
