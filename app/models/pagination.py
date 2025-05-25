from pydantic import BaseModel
from typing import List
from app.models.message import MessageResponse


class PaginatedMessages(BaseModel):
    """Model for paginated messages response
    Attributes:
        messages (List[MessageResponse]): List of messages in the current page.
        total (int): Total number of messages across all pages.
        page (int): Current page number.
        page_size (int): Number of messages per page.
    """
    messages: List[MessageResponse]
    total: int
    page: int
    page_size: int