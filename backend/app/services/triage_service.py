from app.schemas import ComplaintCreate
from app.models import CategoryEnum, PriorityEnum
from app.logger import logger

def perform_triage(complaint: ComplaintCreate) -> dict:
    # Phase 6 will implement full TriageProvider
    logger.info("triage_performed", provider="simulated", detail="Simulated dummy triage for now")
    return {
        "category": CategoryEnum.other,
        "priority": PriorityEnum.normal,
        "summary": "Simulated AI summary",
        "triaged_by": "simulated",
        "triage_latency_ms": 100
    }
