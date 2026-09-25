import os

from .base import TriageProvider
from .llm import LLMTriage
from .ollama import OllamaTriage
from .rules import RuleBasedTriage
from .simulated import SimulatedTriage


def get_triage_provider() -> TriageProvider:
    provider_name = os.getenv("TRIAGE_PROVIDER", "simulated").lower()

    if provider_name == "llm":
        return LLMTriage()
    elif provider_name == "ollama":
        return OllamaTriage()
    elif provider_name == "rules":
        return RuleBasedTriage()
    else:
        return SimulatedTriage()
