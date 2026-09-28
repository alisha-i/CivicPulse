# Pydantic validation schemas
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models import CategoryEnum, PriorityEnum, StatusEnum


class ComplaintCreate(BaseModel):
    text: str = Field(..., min_length=10, max_length=2000)
    location: str = Field(..., min_length=3, max_length=200)
    reporter_contact: str | None = None


class ComplaintStatusUpdate(BaseModel):
    status: StatusEnum


class ComplaintResponse(BaseModel):
    id: UUID
    text: str
    location: str
    reporter_contact: str | None
    category: CategoryEnum
    priority: PriorityEnum
    status: StatusEnum
    ai_summary: str | None
    triaged_by: str | None
    triage_latency_ms: int | None
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ComplaintListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[ComplaintResponse]

# Strict validation enabled for all incoming payloads
