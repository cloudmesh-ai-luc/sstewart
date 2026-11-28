
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...api.dependencies import get_current_operator, require_roles
from ...database import get_db
from ...models import EmergencyMessage, MessageEvent, Operator, MessageTriageResult

from ...services.triage import (
    analyze_message,
    OllamaUnavailableError,
    OllamaResponseError,
    TriageResult,
)

from ...services.config import get_ollama_config


Priority = Literal[
    "UNCLASSIFIED",
    "LOW",
    "MODERATE",
    "HIGH",
    "CRITICAL",
]

OverridePriority = Literal[
    "LOW",
    "MODERATE",
    "HIGH",
    "CRITICAL",
]


class MessageCreate(BaseModel):
    content: str = Field(min_length=1)
    location_text: str | None = None


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    priority: Priority
    created_at: datetime
    updated_at: datetime


class MessageEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    message_id: int
    actor_id: int | None
    event_type: str
    old_value: str | None
    new_value: str | None
    details: str | None
    created_at: datetime


class TriageResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    message_id: int
    requested_by_operator_id: int | None
    suggested_priority: Priority
    suggested_category: str
    explanation: str
    confidence: float
    model_name: str
    created_at: datetime




class PriorityUpdate(BaseModel):
    priority: OverridePriority
    reason: str | None = Field(
        default=None,
        max_length=500,
        description="Optional explanation for the priority change.",
    )


router = APIRouter()


@router.post(
    "/messages",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    payload: MessageCreate,
    current_operator: Operator = Depends(get_current_operator),
    db: Session = Depends(get_db),
):
    message = EmergencyMessage(
        message_text=payload.content,
        location_text=payload.location_text,
    )

    db.add(message)

    try:
        db.flush()

        event = MessageEvent(
            message_id=message.id,
            actor_id=current_operator.id,
            event_type="CREATED",
            new_value="UNCLASSIFIED",
            details="Synthetic emergency message created.",
        )

        db.add(event)
        db.commit()
        db.refresh(message)

    except Exception:
        db.rollback()
        raise

    return message


@router.get("/messages", response_model=list[MessageRead])
def list_messages(
    current_operator: Operator = Depends(get_current_operator),
    db: Session = Depends(get_db),
):
    stmt = select(EmergencyMessage).order_by(EmergencyMessage.id)
    return db.execute(stmt).scalars().all()


@router.get("/messages/{msg_id}", response_model=MessageRead)
def get_message(
    msg_id: int,
    current_operator: Operator = Depends(get_current_operator),
    db: Session = Depends(get_db),
):
    message = db.get(EmergencyMessage, msg_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found.",
        )

    return message


@router.patch("/messages/{msg_id}/priority", response_model=MessageRead)
def update_priority(
    msg_id: int,
    payload: PriorityUpdate,
    current_operator: Operator = Depends(
        require_roles("SUPERVISOR", "ADMIN")
    ),
    db: Session = Depends(get_db),
):
    message = db.get(EmergencyMessage, msg_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found.",
        )

    old_priority = message.priority
    message.priority = payload.priority

    event = MessageEvent(
        message_id=message.id,
        actor_id=current_operator.id,
        event_type="PRIORITY_UPDATED",
        old_value=old_priority,
        new_value=payload.priority,
        details=payload.reason,
    )

    db.add(event)

    try:
        db.commit()
        db.refresh(message)

    except Exception:
        db.rollback()
        raise

    return message


@router.post("/messages/{msg_id}/review")
def add_review(
    msg_id: int,
    current_operator: Operator = Depends(get_current_operator),
    db: Session = Depends(get_db),
):
    message = db.get(EmergencyMessage, msg_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found.",
        )

    event = MessageEvent(
        message_id=message.id,
        actor_id=current_operator.id,
        event_type="REVIEWED",
        details="Message review recorded.",
    )

    db.add(event)

    try:
        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "message_id": message.id,
        "status": "review recorded",
    }


@router.get(
    "/messages/{msg_id}/events",
    response_model=list[MessageEventRead],
)
def get_message_events(
    msg_id: int,
    current_operator: Operator = Depends(get_current_operator),
    db: Session = Depends(get_db),
):
    # Verify that the message exists.
    message = db.get(EmergencyMessage, msg_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found.",
        )

    # Retrieve the message's audit history.
    stmt = (
        select(MessageEvent)
        .where(MessageEvent.message_id == msg_id)
        .order_by(MessageEvent.created_at, MessageEvent.id)
    )

    events = db.execute(stmt).scalars().all()

    return events

@router.post(
    "/messages/{msg_id}/triage",
    response_model=TriageResult,
)
def run_message_triage(
    msg_id: int,
    current_operator: Operator = Depends(get_current_operator),
    db: Session = Depends(get_db),
):
    message = db.get(EmergencyMessage, msg_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found.",
        )

    try:
        result = analyze_message(message.content)

    except OllamaUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI triage service is currently unavailable.",
        )

    except OllamaResponseError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI triage service returned an invalid response.",
        )

    config = get_ollama_config()

    triage_record = MessageTriageResult(
        message_id=message.id,
        requested_by_operator_id=current_operator.id,
        suggested_priority=result.suggested_priority,
        suggested_category=result.suggested_category,
        explanation=result.explanation,
        confidence=result.confidence,
        model_name=config["model"],
    )

    audit_event = MessageEvent(
        message_id=message.id,
        actor_id=current_operator.id,
        event_type="AI_TRIAGE_COMPLETED",
        new_value=result.suggested_priority,
        details=(
            f"AI model: {config['model']}; "
            f"category: {result.suggested_category}; "
            f"confidence: {result.confidence}"
        ),
    )

    db.add_all([triage_record, audit_event])

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return result


@router.get(
    "/messages/{msg_id}/triage",
    response_model=list[TriageResultRead],
)
def get_message_triage_history(
    msg_id: int,
    current_operator: Operator = Depends(get_current_operator),
    db: Session = Depends(get_db),
):
    message = db.get(EmergencyMessage, msg_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found.",
        )

    stmt = (
        select(MessageTriageResult)
        .where(MessageTriageResult.message_id == msg_id)
        .order_by(
            MessageTriageResult.created_at,
            MessageTriageResult.id,
        )
    )

    results = db.execute(stmt).scalars().all()

    return results
