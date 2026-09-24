from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models import CategoryEnum, PriorityEnum, StatusEnum

class ComplaintCreate(BaseModel):
    text: str = Field(..., min_length=10, max_length=2000)
    location: str = Field(..., min_length=3, max_length=200)
    reporter_contact: Optional[str] = None

class ComplaintResponse(BaseModel):
    id: UUID
    text: str
    location: str
    reporter_contact: Optional[str]
    category: CategoryEnum
    priority: PriorityEnum
    status: StatusEnum
    ai_summary: Optional[str]
    triaged_by: Optional[str]
    triage_latency_ms: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

class ComplaintListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ComplaintResponse]
