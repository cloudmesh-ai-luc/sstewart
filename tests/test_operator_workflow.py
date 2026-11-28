
from sqlalchemy import select

from app.api.routes import messages as messages_routes
from app.models import EmergencyMessage, MessageEvent, MessageTriageResult
from app.services.triage import TriageResult


def test_complete_operator_workflow(client, db_session, monkeypatch):
    """Test the complete message review, AI triage, and priority workflow."""

    # Arrange: replace the external AI service with a predictable result.
    fake_triage_result = TriageResult(
        suggested_priority="HIGH",
        suggested_category="MEDICAL",
        explanation="The message describes an injured person.",
        confidence=0.95,
    )

    monkeypatch.setattr(
        messages_routes,
        "analyze_message",
        lambda message_text: fake_triage_result,
    )

    monkeypatch.setattr(
        messages_routes,
        "get_ollama_config",
        lambda: {
            "model": "test-model",
            "base_url": "http://localhost:11434",
            "timeout": 120,
        },
    )

    # 1. Operator receives a new emergency message.
    create_response = client.post(
        "/api/messages",
        json={
            "content": "There is an injured person who needs medical assistance.",
            "location_text": "123 Main Street",
        },
    )

    assert create_response.status_code == 201

    message_id = create_response.json()["id"]

    # Verify the message was persisted.
    message = db_session.get(EmergencyMessage, message_id)

    assert message is not None
    assert message.priority == "UNCLASSIFIED"

    # 2. Operator reviews the message.
    review_response = client.post(
        f"/api/messages/{message_id}/review"
    )

    assert review_response.status_code == 200
    assert review_response.json()["message_id"] == message_id

    # 3. Operator requests AI-assisted triage.
    triage_response = client.post(
        f"/api/messages/{message_id}/triage"
    )

    assert triage_response.status_code == 200

    triage_data = triage_response.json()

    assert triage_data["suggested_priority"] == "HIGH"
    assert triage_data["suggested_category"] == "MEDICAL"
    assert triage_data["confidence"] == 0.95

    # 4. Verify the AI result was saved.
    history_response = client.get(
        f"/api/messages/{message_id}/triage"
    )

    assert history_response.status_code == 200

    triage_history = history_response.json()

    assert len(triage_history) == 1
    assert triage_history[0]["model_name"] == "test-model"
    assert triage_history[0]["suggested_priority"] == "HIGH"

    saved_triage = db_session.scalars(
        select(MessageTriageResult).where(
            MessageTriageResult.message_id == message_id
        )
    ).one()

    assert saved_triage.suggested_category == "MEDICAL"

    # 5. Supervisor/Admin makes the final priority decision.
    priority_response = client.patch(
        f"/api/messages/{message_id}/priority",
        json={
            "priority": "CRITICAL",
            "reason": "Supervisor escalation after reviewing the message.",
        },
    )

    assert priority_response.status_code == 200
    assert priority_response.json()["priority"] == "CRITICAL"

    # Verify the final database state.
    db_session.refresh(message)

    assert message.priority == "CRITICAL"

    # 6. Verify the complete audit history.
    events_response = client.get(
        f"/api/messages/{message_id}/events"
    )

    assert events_response.status_code == 200

    events = events_response.json()

    event_types = [event["event_type"] for event in events]

    assert event_types == [
        "CREATED",
        "REVIEWED",
        "AI_TRIAGE_COMPLETED",
        "PRIORITY_UPDATED",
    ]

    # Verify the final priority change was recorded correctly.
    priority_event = events[-1]

    assert priority_event["old_value"] == "UNCLASSIFIED"
    assert priority_event["new_value"] == "CRITICAL"
    assert (
        priority_event["details"]
        == "Supervisor escalation after reviewing the message."
    )

    # Verify the AI recommendation was also recorded.
    ai_event = events[2]

    assert ai_event["new_value"] == "HIGH"
    assert "MEDICAL" in ai_event["details"]
