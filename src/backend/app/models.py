
from __future__ import annotations

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Use MariaDB-compatible unsigned BIGINT identifiers.
ID_TYPE = BIGINT(unsigned=True)


class Operator(Base):
    __tablename__ = "operators"

    __table_args__ = (
        CheckConstraint(
            "role IN ('OPERATOR', 'SUPERVISOR', 'ADMIN')",
            name="chk_operators_role",
        ),
    )

    id = Column(ID_TYPE, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    role = Column(
        String(30),
        nullable=False,
        server_default=text("'OPERATOR'"),
    )

    is_active = Column(
        Boolean,
        nullable=False,
        server_default=text("1"),
    )

    created_at = Column(
        DATETIME(fsp=6),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP(6)"),
    )

    updated_at = Column(
        DATETIME(fsp=6),
        nullable=False,
        server_default=text(
            "CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"
        ),
    )

    events = relationship("MessageEvent", back_populates="actor")

    def __repr__(self):
        return f"<Operator id={self.id} email={self.email!r} role={self.role}>"


class EmergencyMessage(Base):
    __tablename__ = "emergency_messages"

    __table_args__ = (
        CheckConstraint(
            "status IN ('NEW', 'IN_REVIEW', 'IN_PROGRESS', 'RESOLVED', 'CLOSED')",
            name="chk_messages_status",
        ),
        CheckConstraint(
            "priority IN ('UNCLASSIFIED', 'LOW', 'MODERATE', 'HIGH', 'CRITICAL')",
            name="chk_messages_priority",
        ),
        Index("idx_messages_status_created", "status", "created_at"),
        Index("idx_messages_priority_created", "priority", "created_at"),
        Index("idx_messages_created", "created_at"),
    )

    id = Column(ID_TYPE, primary_key=True, autoincrement=True)

    message_text = Column(Text, nullable=False)
    location_text = Column(String(500), nullable=True)

    status = Column(
        String(30),
        nullable=False,
        server_default=text("'NEW'"),
    )

    priority = Column(
        String(30),
        nullable=False,
        server_default=text("'UNCLASSIFIED'"),
    )

    category = Column(String(100), nullable=True)

    created_at = Column(
        DATETIME(fsp=6),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP(6)"),
    )

    updated_at = Column(
        DATETIME(fsp=6),
        nullable=False,
        server_default=text(
            "CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"
        ),
    )

    events = relationship("MessageEvent", back_populates="message")

    @property
    def content(self) -> str:
        return self.message_text

    @content.setter
    def content(self, value: str) -> None:
        self.message_text = value

    def __repr__(self):
        return (
            f"<EmergencyMessage id={self.id} "
            f"priority={self.priority} status={self.status}>"
        )


class MessageEvent(Base):
    __tablename__ = "message_events"

    __table_args__ = (
        Index("idx_events_message_created", "message_id", "created_at"),
        Index("idx_events_actor_created", "actor_id", "created_at"),
    )

    id = Column(ID_TYPE, primary_key=True, autoincrement=True)

    message_id = Column(
        ID_TYPE,
        ForeignKey("emergency_messages.id", ondelete="RESTRICT"),
        nullable=False,
    )

    actor_id = Column(
        ID_TYPE,
        ForeignKey("operators.id", ondelete="SET NULL"),
        nullable=True,
    )

    event_type = Column(String(50), nullable=False)
    old_value = Column(String(500), nullable=True)
    new_value = Column(String(500), nullable=True)
    details = Column(Text, nullable=True)

    created_at = Column(
        DATETIME(fsp=6),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP(6)"),
    )

    message = relationship("EmergencyMessage", back_populates="events")
    actor = relationship("Operator", back_populates="events")

    def __repr__(self):
        return (
            f"<MessageEvent id={self.id} "
            f"type={self.event_type} message_id={self.message_id}>"
        )
