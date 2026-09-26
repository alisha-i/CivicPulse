# 🏛️ CivicPulse - AI-Powered Citizen Grievance System

Welcome to **CivicPulse**! This project was developed as part of the CS4032 — Software Construction and Design assignment. It is an intelligent platform designed to help citizens report local issues (like broken roads, water leaks, or power outages) and uses Artificial Intelligence to automatically categorize and prioritize them.

## 🚀 Key Features

* **AI Triage Layer:** Uses the Factory Pattern to automatically route complaints. It falls back gracefully between local AI models (Ollama) and cloud APIs (Groq/Llama3).
* **Modern Web Interface:** A sleek, responsive frontend built with Next.js and Tailwind CSS for easy complaint submission and status tracking.
* **Robust Backend API:** Developed using FastAPI (Python) with a strict layered architecture (Routes -> Services -> Repositories -> Providers).
* **Rate Limiting & Caching:** Redis is implemented to protect endpoints from spam (HTTP 429) and to cache heavy database queries.
* **Database Migrations:** SQLAlchemy and Alembic are used to manage the PostgreSQL database schema safely.
* **High Code Quality:** Strict linting (Ruff) and automated tests (Pytest) with EXACTLY 80% code coverage.
* **Containerization & Orchestration:** Fully containerized using multi-stage Dockerfiles, Docker Compose, and orchestrated locally using Kubernetes (Minikube) with Horizontal Pod Autoscaling (HPA).
* **Continuous Integration (CI):** GitHub Actions automatically run linting and tests on every pull request.

## 🛠️ Technology Stack

* **Frontend:** Next.js 14, React, Tailwind CSS, TypeScript
* **Backend:** FastAPI, Python, SQLAlchemy, Alembic, Structlog
* **Databases:** PostgreSQL 16 (Primary), Redis 7 (Caching & Rate Limiting)
* **AI Providers:** Ollama (Local), Groq (Cloud LLM)
* **Infrastructure:** Docker, Docker Compose, Kubernetes, GitHub Actions

## 👥 Collaborators
* **[Alisha Iqbal]**
* **[Musfirah Hamid]**

> *"Building smarter cities through intelligent software design."*
