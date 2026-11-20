
from sqlalchemy import select

from app.models import EmergencyMessage, MessageEvent


def test_create_message(client, db_session):
    """Creating a message should save it and its audit event."""

    # Arrange: prepare the request payload.
    payload = {
        "content": "There is a fire in the building.",
        "location_text": "123 Main Street",
    }

    # Act: send the request to the API.
    response = client.post("/api/messages", json=payload)

    # Assert: verify the API response.
    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["content"] == payload["content"]
    assert data["priority"] == "UNCLASSIFIED"
    assert data["created_at"] is not None

    # Assert: verify the message was persisted in MariaDB.
    message = db_session.get(EmergencyMessage, data["id"])

    assert message is not None
    assert message.message_text == payload["content"]
    assert message.location_text == payload["location_text"]

    # Assert: verify the creation audit event was persisted.
    events = db_session.scalars(
        select(MessageEvent).where(
            MessageEvent.message_id == data["id"]
        )
    ).all()

    assert len(events) == 1
    assert events[0].event_type == "CREATED"



def test_list_messages(client):
    """The API should return all messages."""

    # Initially, there should be no messages.
    response = client.get("/api/messages")

    assert response.status_code == 200
    assert response.json() == []

    # Create two messages.
    client.post(
        "/api/messages",
        json={
            "content": "There is a fire.",
            "location_text": "123 Main Street",
        },
    )

    client.post(
        "/api/messages",
        json={
            "content": "There is a medical emergency.",
            "location_text": "456 Oak Street",
        },
    )

    # Retrieve the messages.
    response = client.get("/api/messages")

    assert response.status_code == 200

    messages = response.json()

    assert len(messages) == 2
    assert messages[0]["content"] == "There is a fire."
    assert messages[1]["content"] == "There is a medical emergency."


def test_get_message(client):
    """The API should return one message by its ID."""

    create_response = client.post(
        "/api/messages",
        json={
            "content": "There is an accident.",
            "location_text": "789 Pine Street",
        },
    )

    message_id = create_response.json()["id"]

    response = client.get(f"/api/messages/{message_id}")

    assert response.status_code == 200

    message = response.json()

    assert message["id"] == message_id
    assert message["content"] == "There is an accident."
    assert message["priority"] == "UNCLASSIFIED"


def test_get_message_not_found(client):
    """The API should return 404 for an unknown message ID."""

    response = client.get("/api/messages/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"
