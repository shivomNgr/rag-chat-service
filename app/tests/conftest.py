import asyncio
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.utils.auth import verify_api_key
from app.database import get_db


# Override API key dependency for testing
async def override_verify_api_key():
    """
    Override the verify_api_key dependency to return a fixed API key for testing.
    """
    return "test_api_key"

app.dependency_overrides[verify_api_key] = override_verify_api_key

@pytest.fixture
def client():
    """
    Create a TestClient for the FastAPI app.
    """
    return TestClient(app)

@pytest_asyncio.fixture
async def async_client():
    """
    Create an AsyncClient for the FastAPI app using ASGITransport.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture
async def db_session():
    """
    Create a database session for testing.
    """
    async for session in get_db():
        yield session

@pytest.fixture(scope="session")
def event_loop():
    """
    Create a new event loop for the test session.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()