import pytest
import uuid
from sqlalchemy import select
from app.database import Message

@pytest.mark.asyncio
async def test_health_check(client):
    """
    Test the health check endpoint to ensure the service is running.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_create_session(async_client, db_session):
    """
    Test the creation of a chat session.
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
    """
    create_response = await async_client.post(
        "/chat/sessions",
        json={"user_id": "test_user", "name": "Test Session"},
        headers={"X-API-Key": "test_api_key"}
    )
    assert create_response.status_code == 200, f"Create session failed: {create_response.text}"
    session_id = create_response.json()["id"]

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