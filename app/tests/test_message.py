import pytest
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_add_message(async_client, db_session):
    """
    Test adding a message to a chat session.
    """
    create_response = await async_client.post(
        "/chat/sessions",
        json={"user_id": "test_user"},
        headers={"X-API-Key": "test_api_key"}
    )
    assert create_response.status_code == 200, f"Create session failed: {create_response.text}"
    session_id = create_response.json()["id"]

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
    """
    create_response = await async_client.post(
        "/chat/sessions",
        json={"user_id": "test_user"},
        headers={"X-API-Key": "test_api_key"}
    )
    assert create_response.status_code == 200, f"Create session failed: {create_response.text}"
    session_id = create_response.json()["id"]

    await async_client.post(
        f"/chat/sessions/{session_id}/messages",
        json={"sender": "user", "content": "Test message", "context": {}},
        headers={"X-API-Key": "test_api_key"}
    )

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