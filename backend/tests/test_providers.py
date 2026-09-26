import os

from app.models import CategoryEnum, PriorityEnum
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import SimulatedTriage


def test_rules_triage():
    provider = RuleBasedTriage()

    res = provider.triage("Water is leaking from pipe", "Sector 1")
    assert res.category == CategoryEnum.water

    res = provider.triage("No electricity in my area", "Sector 2")
    assert res.category == CategoryEnum.electricity

    res = provider.triage("Road is broken", "Sector 3")
    assert res.category == CategoryEnum.roads

    res = provider.triage("Garbage everywhere", "Sector 4")
    assert res.category == CategoryEnum.sanitation

    res = provider.triage("Streetlight is broken", "Sector 5")
    assert res.category == CategoryEnum.streetlights

    res = provider.triage("A blast happened emergency!", "Sector 6")
    assert res.priority == PriorityEnum.high


def test_simulated_triage():
    provider = SimulatedTriage()
    res = provider.triage("Anything", "Anywhere")
    assert res.category == CategoryEnum.water
    assert res.priority == PriorityEnum.high

    os.environ["SIMULATE_FAILURE"] = "true"
    try:
        provider.triage("Anything", "Anywhere")
    except Exception as e:
        assert str(e) == "Simulated failure"
    os.environ["SIMULATE_FAILURE"] = "false"
