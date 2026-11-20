
"""API routes for synthetic emergency message management.

Endpoints:
    POST  /api/messages
    GET   /api/messages
    GET   /api/messages/{msg_id}
    PATCH /api/messages/{msg_id}/priority
    POST  /api/messages/{msg_id}/review
"""

from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...database import get_db
from ...models import EmergencyMessage, MessageEvent


# ---------------------------------------------------------------------------
# Constants and types
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

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


class PriorityUpdate(BaseModel):
    priority: OverridePriority
    reason: str | None = Field(
        default=None,
        max_length=500,
        description="Optional justification for the priority override",
    )


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

router = APIRouter()


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/messages",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    payload: MessageCreate,
    db: Session = Depends(get_db),
):
    """Create a new synthetic emergency message."""

    message = EmergencyMessage(
    message_text=payload.content,
    location_text=payload.location_text,
)

    db.add(message)

    try:
        db.flush()

        event = MessageEvent(
            message_id=message.id,
            actor_id=None,
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


@router.get(
    "/messages",
    response_model=list[MessageRead],
)
def list_messages(
    db: Session = Depends(get_db),
):
    """Return all stored messages."""

    stmt = select(EmergencyMessage).order_by(
        EmergencyMessage.id
    )

    return db.execute(stmt).scalars().all()


@router.get(
    "/messages/{msg_id}",
    response_model=MessageRead,
)
def get_message(
    msg_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve a message by its identifier."""

    message = db.get(EmergencyMessage, msg_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    return message


@router.patch(
    "/messages/{msg_id}/priority",
    response_model=MessageRead,
)
def update_priority(
    msg_id: int,
    payload: PriorityUpdate,
    db: Session = Depends(get_db),
):
    """Override a message's automatically assigned priority."""

    message = db.get(EmergencyMessage, msg_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    old_priority = message.priority

    message.priority = payload.priority

    event = MessageEvent(
        message_id=message.id,
        actor_id=None,
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
    db: Session = Depends(get_db),
):
    """Record that a message has been reviewed."""

    message = db.get(EmergencyMessage, msg_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    event = MessageEvent(
        message_id=message.id,
        actor_id=None,
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
