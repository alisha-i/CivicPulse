import os
from .base import TriageProvider, TriageResult
from app.models import CategoryEnum, PriorityEnum

class SimulatedTriage:
    name = "simulated"

    def triage(self, text: str, location: str) -> TriageResult:
        if os.getenv("SIMULATE_FAILURE") == "true":
            raise Exception("Simulated failure")
            
        return TriageResult(
            category=CategoryEnum.water,
            priority=PriorityEnum.high,
            summary="Simulated AI summary",
            confidence=0.9,
            triaged_by=self.name
        )
