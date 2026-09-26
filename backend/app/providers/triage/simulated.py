import os

from app.models import CategoryEnum, PriorityEnum

from .base import TriageResult


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
            triaged_by=self.name,
        )
