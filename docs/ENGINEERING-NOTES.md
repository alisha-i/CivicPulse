# Engineering Notes (Rubric §5.2)

This document answers the core engineering and architectural questions for the CivicPulse system, including specific file and line references.

### 1. How is the system designed for loose coupling?
**Answer:** The system uses the Strategy pattern for AI triage to ensure the backend logic is not tightly coupled to a single vendor (Groq). 
- *Reference:* `backend/app/providers/triage/factory.py` (Lines 10-25) where `TriageFactory` abstracts the provider instantiation.

### 2. How is system resiliency and fallback handled?
**Answer:** If the primary cloud AI provider fails or times out, the system automatically degrades gracefully by catching the exception and returning a result from the local rule-based engine.
- *Reference:* `backend/app/routes/complaints.py` (Lines 35-45) where the fallback mechanism is wrapped in a `try-except` block.

### 3. How is state and data persistence managed?
**Answer:** Relational data (complaints, statuses) is persisted in PostgreSQL via SQLAlchemy ORM, while transient state/caching (rate limits, triage rules) is handled by Redis to keep the FastAPI backend stateless.
- *Reference:* `backend/app/database.py` (Lines 15-30) for DB sessions, and `backend/app/redis_client.py` (Lines 10-20) for caching layer.

### 4. How is autoscaling triggered and managed under load?
**Answer:** The system relies on Kubernetes Horizontal Pod Autoscaler (HPA). Scaling is triggered based on CPU utilization crossing the 50% threshold.
- *Reference:* `k8s/hpa.yaml` (Lines 15-20) defines the `targetCPUUtilizationPercentage: 50`.

### 5. How are secrets and configurations separated from code?
**Answer:** Configurations are injected via environment variables at runtime. In Kubernetes, this is done using ConfigMaps for non-sensitive data and Secrets for API keys, rather than hardcoding them.
- *Reference:* `k8s/configmap.yaml` (Lines 5-10) and `backend/app/config.py` (Lines 10-15) using Pydantic BaseSettings.

### 6. How is continuous integration and testing enforced?
**Answer:** GitHub Actions runs a CI workflow on every pull request to `main`. It enforces Ruff linting and pytest coverage thresholds (must be >=75%).
- *Reference:* `.github/workflows/ci.yml` (Lines 25-35).

### 7. How are deployments versioned and tracked?
**Answer:** We use a Deploy-by-SHA methodology. The CD pipeline builds Docker images tagged with the unique Git SHA, updating the Kubernetes manifests via text replacement before applying.
- *Reference:* `.github/workflows/cd.yml` (Lines 60-70) where `sed` is used to patch the deployment images.

### 8. How is the frontend runtime configuration handled?
**Answer:** The Streamlit frontend does not have the backend URL hardcoded at build time. It reads `BACKEND_URL` dynamically from the OS environment, allowing the same Docker image to be deployed anywhere.
- *Reference:* `frontend/app.py` (Lines 8-12) where `os.getenv("BACKEND_URL")` is fetched.
