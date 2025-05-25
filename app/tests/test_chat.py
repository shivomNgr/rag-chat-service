import asyncio
import pytest
import uuid
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from app.main import app
from app.utils.auth import verify_api_key
from app.database import get_db, Message


@pytest.fixture
def client():
    """
    Create a TestClient for the FastAPI app.
    This fixture can be used to make synchronous requests to the app during tests.
    """
    return TestClient(app)

# Override API key dependency for testing
async def override_verify_api_key():
    """
    Override the verify_api_key dependency to return a fixed API key for testing.
    This allows tests to bypass actual API key verification.
    """
    return "test_api_key"

app.dependency_overrides[verify_api_key] = override_verify_api_key

@pytest_asyncio.fixture
async def async_client():
    """
    Create an AsyncClient for the FastAPI app using ASGITransport.
    This fixture can be used to make asynchronous requests to the app during tests.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture
async def db_session():
    """
    Create a database session for testing.
    This fixture can be used to interact with the database during tests.
    """
    async for session in get_db():
        yield session

@pytest.fixture(scope="session")
def event_loop():
    """
    Create a new event loop for the test session.
    This fixture ensures that each test session has its own event loop.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Test Cases
@pytest.mark.asyncio
async def test_health_check(client):
    """
    Test the health check endpoint to ensure the service is running.
    This test checks that the endpoint returns a 200 status code and the expected response.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_create_session(async_client, db_session):
    """
    Test the creation of a chat session.
    This test checks that a session can be created successfully and returns the expected data.
    """
    response = await async_client.post(
        "/chat/sessions",
        json={"user_id": "test_user", "name": "Test Session"},
        headers={"X-API-Key": "test_api_key"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["name"] == "Test Session"
    assert "id" in data

@pytest.mark.asyncio
async def test_update_session(async_client, db_session):
    """
    Test updating a chat session.
    This test checks that an existing session can be updated successfully and returns the updated data.
    """
    # Create a session
    create_response = await async_client.post(
        "/chat/sessions",
        json={"user_id": "test_user", "name": "Test Session"},
        headers={"X-API-Key": "test_api_key"}
    )
    assert create_response.status_code == 200, f"Create session failed: {create_response.text}"
    session_id = create_response.json()["id"]

    # Update the session
    response = await async_client.put(
        f"/chat/sessions/{session_id}",
        json={"name": "Updated Session", "is_favorite": True},
        headers={"X-API-Key": "test_api_key"}
    )
    assert response.status_code == 200, f"Update session failed: {response.text}"
    data = response.json()
    assert data["name"] == "Updated Session"
    assert data["is_favorite"] is True
    assert data["id"] == session_id


@pytest.mark.asyncio
async def test_delete_session_cascades_messages(async_client, db_session):
    """
    Test that deleting a chat session also deletes associated messages.
    This test checks that when a session is deleted, all messages associated with that session are also removed.
    """
    response = await async_client.post(
        "/chat/sessions",
        json={"user_id": "test_user", "name": "Test Session"},
        headers={"X-API-Key": "test_api_key"},
    )
    assert response.status_code == 200
    session_id = response.json()["id"]

    response = await async_client.post(
        f"/chat/sessions/{session_id}/messages",
        json={
            "sender": "user",
            "content": "Test message",
            "context": {"rag_data": "context"},
        },
        headers={"X-API-Key": "test_api_key"},
    )
    assert response.status_code == 200

    result = await db_session.execute(
        select(Message).filter_by(session_id=uuid.UUID(session_id))
    )
    assert result.scalars().first() is not None

    response = await async_client.delete(
        f"/chat/sessions/{session_id}",
        headers={"X-API-Key": "test_api_key"},
    )
    assert response.status_code == 200

    result = await db_session.execute(
        select(Message).filter_by(session_id=uuid.UUID(session_id))
    )
    assert result.scalars().first() is None

@pytest.mark.asyncio
async def test_add_message(async_client, db_session):
    """
    Test adding a message to a chat session.
    This test checks that a message can be added to an existing session and returns the expected data.
    """
    # Create a session
    create_response = await async_client.post(
        "/chat/sessions",
        json={"user_id": "test_user"},
        headers={"X-API-Key": "test_api_key"}
    )
    assert create_response.status_code == 200, f"Create session failed: {create_response.text}"
    session_id = create_response.json()["id"]

    # Add a message
    response = await async_client.post(
        f"/chat/sessions/{session_id}/messages",
        json={
            "sender": "user",
            "content": "Hello, how are you?",
            "context": {"rag_data": "Some context"}
        },
        headers={"X-API-Key": "test_api_key"}
    )
    assert response.status_code == 200, f"Add message failed: {response.text}"
    data = response.json()
    assert data["sender"] == "user"
    assert data["content"] == "Hello, how are you?"
    assert data["context"] == {"rag_data": "Some context"}
    assert data["session_id"] == session_id

@pytest.mark.asyncio
async def test_get_messages(async_client, db_session):
    """
    Test retrieving messages from a chat session.
    This test checks that messages can be retrieved from an existing session with pagination.
    """
    # Create a session
    create_response = await async_client.post(
        "/chat/sessions",
        json={"user_id": "test_user"},
        headers={"X-API-Key": "test_api_key"}
    )
    assert create_response.status_code == 200, f"Create session failed: {create_response.text}"
    session_id = create_response.json()["id"]

    # Add a message
    await async_client.post(
        f"/chat/sessions/{session_id}/messages",
        json={"sender": "user", "content": "Test message", "context": {}},
        headers={"X-API-Key": "test_api_key"}
    )

    # Get messages
    response = await async_client.get(
        f"/chat/sessions/{session_id}/messages?page=1&page_size=10",
        headers={"X-API-Key": "test_api_key"}
    )
    assert response.status_code == 200, f"Get messages failed: {response.text}"
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total"] == 1
    assert len(data["messages"]) == 1
    assert data["messages"][0]["content"] == "Test message"