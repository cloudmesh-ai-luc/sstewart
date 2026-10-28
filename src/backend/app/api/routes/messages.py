"""API routes for message management.

The endpoints correspond to the contract described in ``project.md``:

* ``POST /api/messages`` – Create a new synthetic message.
* ``GET  /api/messages`` – List all messages (pagination omitted for brevity).
* ``GET  /api/messages/{id}`` – Retrieve a single message.
* ``PATCH /api/messages/{id}/priority`` – Override the auto‑generated priority.
* ``POST /api/messages/{id}/review`` – Record a review action (placeholder).

The implementation uses SQLAlchemy with a SQLite database for simplicity. In a
real deployment the connection URL would be built from the configuration
loaded by :pymod:`src.backend.app.services.config`.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field

from sqlalchemy import Column, Integer, String, DateTime, create_engine, select, update
from sqlalchemy.orm import declarative_base, Session, sessionmaker

# ---------------------------------------------------------------------------
# Database setup (SQLite for demonstration). Replace with MariaDB URL in prod.
# ---------------------------------------------------------------------------
SQLITE_URL = "sqlite:///./messages.db"
engine = create_engine(SQLITE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)
Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    # Priority 0 = not set / default, higher numbers indicate more urgent.
    priority = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Create tables if they do not exist.
Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """FastAPI dependency that provides a database session.

    The session is closed after the request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, description="Synthetic message text")


class MessageRead(BaseModel):
    id: int
    content: str
    priority: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PriorityUpdate(BaseModel):
    priority: int = Field(..., ge=0, description="Reviewer‑provided priority override")
    reason: str | None = Field(None, description="Optional justification for the override")


router = APIRouter()


@router.post("/messages", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def create_message(payload: MessageCreate, db: Session = Depends(get_db)):
    """Create a new message and store it in the database.

    The auto‑generated priority is currently set to ``0`` – real logic would
    invoke the triage engine here.
    """
    db_msg = Message(content=payload.content)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg


@router.get("/messages", response_model=List[MessageRead])
def list_messages(db: Session = Depends(get_db)):
    """Return all stored messages.

    Pagination, filtering and authentication are omitted for brevity but can be
    added by extending the query and applying FastAPI's ``Depends`` mechanism.
    """
    stmt = select(Message).order_by(Message.id)
    results = db.execute(stmt).scalars().all()
    return results


@router.get("/messages/{msg_id}", response_model=MessageRead)
def get_message(msg_id: int, db: Session = Depends(get_db)):
    """Retrieve a single message by its identifier."""
    msg = db.get(Message, msg_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


@router.patch("/messages/{msg_id}/priority", response_model=MessageRead)
def update_priority(
    msg_id: int, payload: PriorityUpdate, db: Session = Depends(get_db)
):
    """Override the automatically calculated priority.

    In a full implementation the ``reason`` would be stored in a review table.
    Here we simply update the ``priority`` column.
    """
    msg = db.get(Message, msg_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    msg.priority = payload.priority
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@router.post("/messages/{msg_id}/review")
def add_review(msg_id: int, db: Session = Depends(get_db)):
    """Placeholder endpoint for recording a review action.

    The current implementation does not persist review data – it simply
    confirms that the referenced message exists.
    """
    msg = db.get(Message, msg_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message_id": msg_id, "status": "review recorded (placeholder)"}
