
from sqlalchemy import select

from app.models import EmergencyMessage, MessageEvent
import pytest


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
    assert response.json()["detail"] == "Message not found."



def test_update_message_priority(client, db_session):
    """Updating priority should update the message and create an audit event."""

    # Arrange: create a message.
    create_response = client.post(
        "/api/messages",
        json={
            "content": "There is an injured person.",
            "location_text": "123 Main Street",
        },
    )

    assert create_response.status_code == 201

    message_id = create_response.json()["id"]

    # Act: change the priority.
    response = client.patch(
        f"/api/messages/{message_id}/priority",
        json={
            "priority": "HIGH",
            "reason": "Person requires immediate medical attention.",
        },
    )

    # Assert: verify the API response.
    assert response.status_code == 200
    assert response.json()["priority"] == "HIGH"

    # Assert: verify the message was updated in MariaDB.
    message = db_session.get(EmergencyMessage, message_id)

    assert message is not None
    assert message.priority == "HIGH"

    # Assert: verify the audit event.
    events = db_session.scalars(
        select(MessageEvent).where(
            MessageEvent.message_id == message_id,
            MessageEvent.event_type == "PRIORITY_UPDATED",
        )
    ).all()

    assert len(events) == 1

    event = events[0]

    assert event.old_value == "UNCLASSIFIED"
    assert event.new_value == "HIGH"



def test_update_message_priority_invalid_value(client, db_session):
    """Invalid priorities should be rejected without changing the message."""

    # Arrange: create a message.
    create_response = client.post(
        "/api/messages",
        json={
            "content": "There is an emergency.",
            "location_text": "123 Main Street",
        },
    )

    message_id = create_response.json()["id"]

    # Act: attempt to assign an invalid priority.
    response = client.patch(
        f"/api/messages/{message_id}/priority",
        json={
            "priority": "URGENT",
            "reason": "Testing invalid priority.",
        },
    )

    # Assert: the API rejects the request.
    assert response.status_code == 422

    # Assert: the original priority remains unchanged.
    message = db_session.get(EmergencyMessage, message_id)

    assert message is not None
    assert message.priority == "UNCLASSIFIED"

    # Assert: no priority-update event was created.
    events = db_session.scalars(
        select(MessageEvent).where(
            MessageEvent.message_id == message_id,
            MessageEvent.event_type == "PRIORITY_UPDATED",
        )
    ).all()

    assert len(events) == 0


def test_review_message(client, db_session):
    """Reviewing a message should create a REVIEWED audit event."""

    # Arrange: create a message.
    create_response = client.post(
        "/api/messages",
        json={
            "content": "There is a suspicious vehicle.",
            "location_text": "456 Oak Street",
        },
    )

    message_id = create_response.json()["id"]

    # Act: review the message.
    response = client.post(f"/api/messages/{message_id}/review")

    # Assert: verify the response.
    assert response.status_code == 200
    assert response.json()["message_id"] == message_id
    assert response.json()["status"] == "review recorded"

    # Assert: verify the audit event.
    events = db_session.scalars(
        select(MessageEvent).where(
            MessageEvent.message_id == message_id,
            MessageEvent.event_type == "REVIEWED",
        )
    ).all()

    assert len(events) == 1


def test_create_message_empty_content(client, db_session):
    """The API should reject messages with empty content."""

    response = client.post(
        "/api/messages",
        json={
            "content": "",
            "location_text": "123 Main Street",
        },
    )

    # Assert: validation rejects the request.
    assert response.status_code == 422

    # Assert: no message was created.
    messages = db_session.scalars(
        select(EmergencyMessage)
    ).all()

    assert len(messages) == 0


def test_update_nonexistent_message(client):
    """Updating a nonexistent message should return 404."""

    response = client.patch(
        "/api/messages/999999/priority",
        json={
            "priority": "HIGH",
            "reason": "Testing nonexistent message.",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found."


def test_review_nonexistent_message(client):
    """Reviewing a nonexistent message should return 404."""

    response = client.post("/api/messages/999999/review")

    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found."


def test_priority_history_preserves_changes(client, db_session):
    """Multiple priority changes should preserve their audit history."""

    create_response = client.post(
        "/api/messages",
        json={
            "content": "An emergency requiring assessment.",
            "location_text": "123 Main Street",
        },
    )

    message_id = create_response.json()["id"]

    # First priority change.
    first_response = client.patch(
        f"/api/messages/{message_id}/priority",
        json={"priority": "LOW"},
    )

    assert first_response.status_code == 200

    # Second priority change.
    second_response = client.patch(
        f"/api/messages/{message_id}/priority",
        json={"priority": "CRITICAL"},
    )

    assert second_response.status_code == 200

    # Verify the current priority.
    message = db_session.get(EmergencyMessage, message_id)

    assert message.priority == "CRITICAL"

    # Verify the complete audit history.
    events = db_session.scalars(
        select(MessageEvent)
        .where(
            MessageEvent.message_id == message_id,
            MessageEvent.event_type == "PRIORITY_UPDATED",
        )
        .order_by(MessageEvent.id)
    ).all()

    assert len(events) == 2

    assert events[0].old_value == "UNCLASSIFIED"
    assert events[0].new_value == "LOW"

    assert events[1].old_value == "LOW"
    assert events[1].new_value == "CRITICAL"


def test_create_message_without_location(client, db_session):
    """A message should be created even when location is omitted."""

    response = client.post(
        "/api/messages",
        json={
            "content": "An emergency without a reported location."
        },
    )

    assert response.status_code == 201

    message_id = response.json()["id"]

    message = db_session.get(EmergencyMessage, message_id)

    assert message is not None
    assert message.message_text == (
        "An emergency without a reported location."
    )
    assert message.location_text is None


def test_create_message_database_failure(client, db_session, monkeypatch):
    """A failed commit should roll back message creation."""

    def fail_commit():
        raise RuntimeError("Simulated commit failure")

    monkeypatch.setattr(db_session, "commit", fail_commit)

    with pytest.raises(RuntimeError, match="Simulated commit failure"):
        client.post(
            "/api/messages",
            json={
                "content": "Testing database failure.",
                "location_text": "123 Main Street",
            },
        )

    # Verify the failed operation left no records behind.
    messages = db_session.scalars(
        select(EmergencyMessage)
    ).all()

    events = db_session.scalars(
        select(MessageEvent)
    ).all()

    assert messages == []
    assert events == []



def test_update_priority_database_failure(
    client, db_session, monkeypatch
):
    """A failed priority update should restore the original priority."""

    # Create a message before simulating the failure.
    create_response = client.post(
        "/api/messages",
        json={
            "content": "Testing priority rollback.",
            "location_text": "123 Main Street",
        },
    )

    message_id = create_response.json()["id"]

    def fail_commit():
        raise RuntimeError("Simulated commit failure")

    monkeypatch.setattr(db_session, "commit", fail_commit)

    # Attempt to update the priority.
    with pytest.raises(RuntimeError, match="Simulated commit failure"):
        client.patch(
            f"/api/messages/{message_id}/priority",
            json={"priority": "CRITICAL"},
        )

    # Verify the original priority was restored.
    message = db_session.get(EmergencyMessage, message_id)

    assert message is not None
    assert message.priority == "UNCLASSIFIED"

    # Verify no priority-update event remains.
    events = db_session.scalars(
        select(MessageEvent).where(
            MessageEvent.message_id == message_id,
            MessageEvent.event_type == "PRIORITY_UPDATED",
        )
    ).all()

    assert events == []


def test_review_database_failure(client, db_session, monkeypatch):
    """A failed review commit should not leave an audit event."""

    create_response = client.post(
        "/api/messages",
        json={
            "content": "Testing review rollback.",
            "location_text": "456 Oak Street",
        },
    )

    message_id = create_response.json()["id"]

    def fail_commit():
        raise RuntimeError("Simulated commit failure")

    monkeypatch.setattr(db_session, "commit", fail_commit)

    with pytest.raises(RuntimeError, match="Simulated commit failure"):
        client.post(f"/api/messages/{message_id}/review")

    # Verify no review event remains.
    events = db_session.scalars(
        select(MessageEvent).where(
            MessageEvent.message_id == message_id,
            MessageEvent.event_type == "REVIEWED",
        )
    ).all()

    assert events == []
