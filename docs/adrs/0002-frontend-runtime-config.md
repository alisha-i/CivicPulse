# ADR 0002: Frontend Runtime Configuration

**Status:** Accepted
**Date:** 2026-09-28

## Context and Problem Statement
Our Streamlit frontend needs to know the URL of the FastAPI backend to make HTTP requests. If we hardcode this URL at build time (e.g., inside the Dockerfile), we cannot promote the same Docker image across different environments (local, dev, production). How do we supply environment-specific config to the frontend at runtime?

## Decision
We decided to use **Runtime Environment Variables** loaded on container startup, rather than build-time arguments (`ARG`). 
The `BACKEND_URL` is read by Streamlit at runtime using `os.getenv("BACKEND_URL", "http://backend:8000")`. In Kubernetes, this is injected via a ConfigMap (`frontend-deployment.yaml`).

## Consequences
**Good:**
- **Build Once, Deploy Anywhere:** We can build a single `civicpulse-frontend` image and deploy it across Local, Staging, and Production environments just by changing the ConfigMap.
- No sensitive configuration is baked into the image.

**Bad:**
- Requires Kubernetes or docker-compose to strictly define the environment variable, otherwise the frontend will crash or fail to connect.
