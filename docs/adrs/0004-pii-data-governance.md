# ADR 0004: PII and Data Governance in AI Triage

**Status:** Accepted
**Date:** 2026-09-28

## Context and Problem Statement
Citizen complaints inherently contain Personally Identifiable Information (PII) such as names, phone numbers, and addresses. Sending raw complaints to a third-party cloud LLM (Groq) for triage poses a severe privacy and data governance risk. How do we ensure citizens' data is protected?

## Decision
We decided to implement a **Data Scrubbing / Governance Middleware** prior to the AI triage step.
Before the complaint text is sent to the `LLMTriageProvider`, any PII (phone numbers, specific names, emails) must be either sanitized or masked locally. The cloud AI only receives the context needed for triage (e.g., "Water pipe broken at [REDACTED]"). The local PostgreSQL database stores the encrypted/secure original record for official city use only.

## Consequences
**Good:**
- Ensures compliance with privacy laws and protects citizens.
- Reduces the risk of data leaks via third-party AI logs.

**Bad:**
- Increases local processing time slightly.
- Over-aggressive redaction might remove context needed by the AI to accurately assign a department (e.g., redacting a street name might make location-based routing harder).
