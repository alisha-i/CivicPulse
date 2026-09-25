from app.schemas import ComplaintCreate
from app.providers.triage.factory import get_triage_provider
from app.logger import logger

def perform_triage(complaint: ComplaintCreate) -> dict:
    provider = get_triage_provider()
    
    logger.info("triage_started", provider=provider.name)
    result = provider.triage(complaint.text, complaint.location)
    
    return {
        "category": result.category,
        "priority": result.priority,
        "summary": result.summary,
        "triaged_by": result.triaged_by,
        "triage_latency_ms": getattr(result, "triage_latency_ms", 100) # LLM handles its own latency logging usually, but we pass what we have
    }
