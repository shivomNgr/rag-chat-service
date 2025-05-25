import logging
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status
from typing import TypeVar, Generic, Type, Dict
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Type variables for generic repository
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    """
    A generic base repository class for CRUD operations on SQLAlchemy models.
    This class provides methods to create, read, update, and delete records in the database.
    It also handles UUID conversion for fields that require it.
    Attributes:
        model (Type[ModelType]): The SQLAlchemy model class to operate on.
        db (AsyncSession): The database session to use for operations.
        response_schema (Type[ResponseSchemaType]): The Pydantic schema for the response.
    """

    def __init__(self, model: Type[ModelType], db: AsyncSession, response_schema: Type[ResponseSchemaType]):
        """
        Initializes the repository with the model, database session, and response schema.
        Args:
            model (Type[ModelType]): The SQLAlchemy model class to operate on.
            db (AsyncSession): The database session to use for operations.
            response_schema (Type[ResponseSchemaType]): The Pydantic schema for the response.
        """
        self.model = model
        self.db = db
        self.response_schema = response_schema

    def _prepare_data(self, data: Dict) -> Dict:
        """
        Prepares the data dictionary by converting UUID fields to strings.
        This is necessary for compatibility with Pydantic models and JSON serialization.
        Args:
            data (Dict): The data dictionary to prepare.
        Returns:
            Dict: The prepared data dictionary with UUIDs converted to strings.
        """
        logger.debug(f"Preparing data for {self.model.__name__}: {data}")
        # Convert UUID fields to strings
        prepared_data = data.copy()
        for key, value in prepared_data.items():
            if isinstance(value, uuid.UUID):
                logger.debug(f"Converting {key} to string: {value}")
                prepared_data[key] = str(value)
        logger.debug(f"Prepared data: {prepared_data}")
        return prepared_data

    async def create(self, data: CreateSchemaType) -> ResponseSchemaType:
        """
        Creates a new record in the database using the provided data.
        Args:
            data (CreateSchemaType): The data to create a new record.
        Returns:
            ResponseSchemaType: The response schema instance containing the created record.
        Raises:
            HTTPException: If an error occurs during creation, a 500 Internal Server Error is raised.
        """
        try:
            # Convert Pydantic model to dict and create SQLAlchemy model instance
            db_instance = self.model(**data.model_dump())
            self.db.add(db_instance)
            await self.db.flush()  # Ensure ID is assigned
            await self.db.commit()
            await self.db.refresh(db_instance)
            logger.info(f"Created {self.model.__name__} with ID {getattr(db_instance, 'id', 'unknown')}")
            return self.response_schema.model_validate(self._prepare_data(db_instance.__dict__))
        except Exception as e:
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create {self.model.__name__.lower()}")

    async def update(self, id: str, data: UpdateSchemaType) -> ResponseSchemaType:
        """
        Updates an existing record in the database with the provided ID and data.
        Args:
            id (str): The ID of the record to update.
            data (UpdateSchemaType): The data to update the record with.
        Returns:
            ResponseSchemaType: The response schema instance containing the updated record.
        Raises:
            HTTPException: If the record is not found, a 404 Not Found error is raised.
            HTTPException: If an error occurs during update, a 500 Internal Server Error is raised.
        """
        try:
            # Convert ID to UUID if applicable
            id_value = uuid.UUID(id) if hasattr(self.model, 'id') and self.model.__table__.c.id.type.python_type == uuid.UUID else id
            result = await self.db.execute(
                select(self.model).filter(self.model.id == id_value)
            )
            db_instance = result.scalar_one_or_none()
            if not db_instance:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found")
            
            update_data = data.model_dump(exclude_unset=True)
            await self.db.execute(
                update(self.model)
                .where(self.model.id == id_value)
                .values(**update_data)
            )
            await self.db.commit()
            await self.db.refresh(db_instance)
            logger.info(f"Updated {self.model.__name__} with ID {id}")
            return self.response_schema.model_validate(self._prepare_data(db_instance.__dict__))
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating {self.model.__name__}: {str(e)}")
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update {self.model.__name__.lower()}")

    async def delete(self, id: str) -> dict:
        """
        Deletes an existing record in the database with the provided ID.
        Args:
            id (str): The ID of the record to delete.
        Returns:
            dict: A dictionary containing a success message.
        Raises:
            HTTPException: If the record is not found, a 404 Not Found error is raised.
            HTTPException: If an error occurs during deletion, a 500 Internal Server Error is raised.
        """
        try:
            # Convert ID to UUID if applicable
            id_value = uuid.UUID(id) if hasattr(self.model, 'id') and self.model.__table__.c.id.type.python_type == uuid.UUID else id
            result = await self.db.execute(
                select(self.model).filter(self.model.id == id_value)
            )
            db_instance = result.scalar_one_or_none()
            if not db_instance:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found")
            
            await self.db.delete(db_instance)
            await self.db.commit()
            logger.info(f"Deleted {self.model.__name__} with ID {id}")
            return {"message": f"{self.model.__name__} deleted successfully"}
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting {self.model.__name__}: {str(e)}")
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete {self.model.__name__.lower()}")

    async def get(self, id: str) -> ResponseSchemaType:
        """
        Retrieves a record from the database by its ID.
        Args:
            id (str): The ID of the record to retrieve.
        Returns:
            ResponseSchemaType: The response schema instance containing the retrieved record.
        Raises:
            HTTPException: If the record is not found, a 404 Not Found error is raised.
            HTTPException: If an error occurs during retrieval, a 500 Internal Server Error is raised.
        """
        try:
            # Convert ID to UUID if applicable
            id_value = uuid.UUID(id) if hasattr(self.model, 'id') and self.model.__table__.c.id.type.python_type == uuid.UUID else id
            result = await self.db.execute(
                select(self.model).filter(self.model.id == id_value)
            )
            db_instance = result.scalar_one_or_none()
            if not db_instance:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found")
            return self.response_schema.model_validate(self._prepare_data(db_instance.__dict__))
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving {self.model.__name__}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve {self.model.__name__.lower()}")