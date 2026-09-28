# ADR 0001: Provider Interface for AI Triage

**Status:** Accepted
**Date:** 2026-09-28

## Context and Problem Statement
We need to process unstructured citizen complaints to extract category, priority, and department. Relying on a single external LLM provider (like Groq or OpenAI) introduces a single point of failure. How can we design the system to abstract the AI triage provider and seamlessly switch to a local fallback when the primary fails?

## Decision
We decided to implement the **Strategy Pattern** via a common `ProviderInterface` (`BaseTriageProvider`). 
All AI providers (e.g., `LLMTriageProvider` for Groq) and the local fallback (`RuleBasedTriageProvider`) must implement this interface. A `TriageFactory` will manage the lifecycle and routing.

## Consequences
**Good:**
- High resiliency: If the cloud API goes down, the `TriageFactory` instantly catches the exception and routes the request to the `RuleBasedTriageProvider` without the caller knowing.
- Extensibility: Adding a new LLM provider (e.g., Claude or OpenAI) only requires adding a new class implementing the interface.

**Bad:**
- Increases code complexity by requiring a factory and interface layer rather than making direct API calls.
