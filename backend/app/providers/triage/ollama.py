from .base import TriageResult
from .rules import RuleBasedTriage


class OllamaTriage:
    name = "llm:ollama"

    def __init__(self):
        self.rules_fallback = RuleBasedTriage()

    def triage(self, text: str, location: str) -> TriageResult:
        # Dummy implementation for Ollama; will be implemented in Compose phase
        return self.rules_fallback.triage(text, location)
