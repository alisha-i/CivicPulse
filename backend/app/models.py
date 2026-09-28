# SQLAlchemy database models
import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class CategoryEnum(str, enum.Enum):
    water = "water"
    electricity = "electricity"
    sanitation = "sanitation"
    roads = "roads"
    streetlights = "streetlights"
    other = "other"


class PriorityEnum(str, enum.Enum):
    high = "high"
    normal = "normal"
    low = "low"


class StatusEnum(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    rejected = "rejected"


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String(2000), nullable=False)
    location = Column(String(200), nullable=False)
    reporter_contact = Column(String, nullable=True)
    category = Column(Enum(CategoryEnum), nullable=False)
    priority = Column(Enum(PriorityEnum), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.open)
    ai_summary = Column(String(140), nullable=True)
    triaged_by = Column(String, nullable=True)
    triage_latency_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Required indexes
Index("ix_complaints_status_priority", Complaint.status, Complaint.priority)
Index("ix_complaints_created_at", Complaint.created_at)
