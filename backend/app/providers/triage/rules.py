from .base import TriageProvider, TriageResult
from app.models import CategoryEnum, PriorityEnum

class RuleBasedTriage:
    name = "rules"

    def triage(self, text: str, location: str) -> TriageResult:
        lower_text = text.lower()
        category = CategoryEnum.other
        priority = PriorityEnum.normal
        
        if "water" in lower_text or "paani" in lower_text or "pipe" in lower_text:
            category = CategoryEnum.water
        elif "light" in lower_text or "bijli" in lower_text or "electricity" in lower_text:
            category = CategoryEnum.electricity
        elif "road" in lower_text or "sarak" in lower_text:
            category = CategoryEnum.roads
        elif "garbage" in lower_text or "kachra" in lower_text:
            category = CategoryEnum.sanitation
        elif "streetlight" in lower_text or "pole" in lower_text:
            category = CategoryEnum.streetlights

        if "emergency" in lower_text or "fajr" in lower_text or "blast" in lower_text or "urgent" in lower_text:
            priority = PriorityEnum.high
            
        return TriageResult(
            category=category,
            priority=priority,
            summary="Rule-based classification fallback.",
            confidence=0.5,
            triaged_by=self.name
        )
