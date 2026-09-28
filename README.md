# CivicPulse 🏛️

![CI/CD](https://img.shields.io/github/actions/workflow/status/alisha-i/CivicPulse/ci.yml?label=CI%2FCD)
![Coverage](https://img.shields.io/badge/coverage-78%25-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Kubernetes](https://img.shields.io/badge/kubernetes-HPA-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Problem Statement
Municipal departments receive thousands of complaints daily, from broken streetlights to water leaks. Manually reading, categorizing, and routing these complaints is slow, error-prone, and inefficient. **CivicPulse** is an AI-powered smart city complaint triage system that solves this by automatically categorizing, prioritizing, and routing citizen complaints to the correct departments in real-time, drastically reducing response times.

## 🏗️ Architecture

```mermaid
flowchart TD
    User([Citizen]) -->|Submits Complaint| Frontend(Streamlit Frontend)
    Frontend -->|POST /api/v1/complaints/triage| API(FastAPI Backend)
    API -->|Caches rules & limits| Redis[(Redis)]
    API -->|Saves record| DB[(PostgreSQL)]
    
    API -->|1. Try Cloud AI| Groq(Groq Llama-3)
    Groq -->|Success| API
    Groq -.->|Timeout/Fail| Fallback(Rule-based Fallback Engine)
    Fallback -.-> API
    
    API -->|Returns Result| Frontend
```

## 🚀 One-Command Quickstart

Start the entire system locally (Frontend, Backend, Postgres, Redis) using Docker Compose:

```bash
docker-compose up -d --build
```
- **Frontend UI:** http://localhost:8501
- **Backend API Docs:** http://localhost:8000/docs

## 🔌 API Table

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/health` | `GET` | System health check (DB, Redis) | None | `{ "status": "ok", "db": "up", "redis": "up" }` |
| `/api/v1/complaints/triage` | `POST` | Process & triage a complaint | `{ "text": "...", "location": "..." }` | `{ "category": "...", "priority": "...", "department": "..." }` |
| `/api/v1/monitoring/metrics`| `GET` | Get system metrics & triage stats | None | `{ "total_complaints": 150, "fallback_invocations": 2 }` |


