from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all database models.
    This class inherits from DeclarativeBase to provide a common base for all models.
    It can be extended to include common attributes or methods for all models in the application.
    """
    pass