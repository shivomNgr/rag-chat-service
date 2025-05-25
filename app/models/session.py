from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional, List, Dict

class ChatSessionCreate(BaseModel):
    """Model for creating a chat session.
    Attributes:
        name (Optional[str]): Name of the chat session.
        user_id (str): Identifier for the user associated with the session.
    """
    name: Optional[str] = None
    user_id: str

class ChatSessionUpdate(BaseModel):
    """Model for updating a chat session.
    Attributes:
        name (Optional[str]): New name for the chat session.
        is_favorite (Optional[bool]): New favorite status for the session.
    """
    name: Optional[str] = None
    is_favorite: Optional[bool] = None

class ChatSessionResponse(BaseModel):
    """Response model for a chat session.
    Attributes:
        id (str): Unique identifier for the chat session.
        name (Optional[str]): Name of the chat session.
        user_id (str): Identifier for the user associated with the session.
        is_favorite (bool): Indicates if the session is marked as favorite.
        created_at (datetime): Timestamp when the session was created.
        updated_at (datetime): Timestamp when the session was last updated.
    """
    id: str
    name: Optional[str]
    user_id: str
    is_favorite: bool
    created_at: datetime
    updated_at: datetime
