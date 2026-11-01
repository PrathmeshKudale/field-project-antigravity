import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import String, Text, Integer, DateTime, Enum, func, ForeignKey, Boolean
from app.db.compat import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class QAEvent(Base):
    __tablename__ = "qa_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    question_scrubbed: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    intent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    verdict: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    claims: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    explanation: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    next_questions: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    corpus_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    review_flag: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    llm_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    feedbacks: Mapped[list["Feedback"]] = relationship("Feedback", back_populates="qa_event")
    report_items: Mapped[list["ReportItem"]] = relationship("ReportItem", back_populates="qa_event")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    qa_event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("qa_events.id", ondelete="CASCADE"), nullable=False)
    issue: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    qa_event: Mapped["QAEvent"] = relationship("QAEvent", back_populates="feedbacks")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False, default="Family Report")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    corpus_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="reports")
    items: Mapped[list["ReportItem"]] = relationship("ReportItem", back_populates="report", cascade="all, delete-orphan")


class ReportItem(Base):
    __tablename__ = "report_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    qa_event_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("qa_events.id", ondelete="SET NULL"), nullable=True)
    section: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    report: Mapped["Report"] = relationship("Report", back_populates="items")
    qa_event: Mapped["QAEvent | None"] = relationship("QAEvent", back_populates="report_items")
