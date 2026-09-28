# Base interface for Triage providers
from typing import Protocol

from pydantic import BaseModel, Field

from app.models import CategoryEnum, PriorityEnum


class TriageResult(BaseModel):
    category: CategoryEnum
    priority: PriorityEnum
    summary: str = Field(max_length=140)
    confidence: float = Field(ge=0.0, le=1.0)
    triaged_by: str = ""


class TriageProvider(Protocol):
    name: str

    def triage(self, text: str, location: str) -> TriageResult: ...
