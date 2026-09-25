
from fastapi import APIRouter

router = APIRouter(prefix="/api/meta", tags=["Metadata"])

# Dummy in-memory list for now; Phase 6 will update this real-time
recent_outcomes: list[dict] = []


@router.get("/providers")
def get_providers_meta():
    """
    Which triage provider is active, and the last 20 triage outcomes
    (provider, latency ms, fallback y/n).
    """
    # Active provider will eventually come from TRIAGE_PROVIDER env variable.
    # We will simulate it for Phase 3.
    import os

    active_provider = os.getenv("TRIAGE_PROVIDER", "simulated")

    return {
        "active_provider": active_provider,
        "recent_outcomes": recent_outcomes[-20:],
    }
