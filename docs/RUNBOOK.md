# CivicPulse Runbook

This runbook provides operational procedures for the CivicPulse system.

## 1. How to Deploy

Deployments are fully automated via GitHub Actions (`.github/workflows/cd.yml`).
1. Merge your Pull Request into the `main` branch.
2. The CI/CD pipeline will automatically run: tests the code, builds the images, tags them with the Git SHA, pushes to GHCR, and applies the YAML files to the Kubernetes cluster.

**Manual Local Deployment:**
```bash
docker-compose up -d --build
```
*Or for K8s manually:*
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

## 2. How to Roll Back

If a bad deployment goes out, the fastest way to restore service is using Kubernetes rollout undo:

```bash
# Check deployment history
kubectl rollout history deployment/backend -n civicpulse

# Rollback to the previous version
kubectl rollout undo deployment/backend -n civicpulse

# Verify the rollout
kubectl rollout status deployment/backend -n civicpulse
```
*Note: Also revert the Git commit in GitHub to ensure the bad code is removed from `main`.*

## 3. How to Read Logs

To monitor the applications and debug issues, use `kubectl logs`.

```bash
# Get backend logs (follow live)
kubectl logs -f deployment/backend -n civicpulse

# Get frontend logs
kubectl logs -f deployment/frontend -n civicpulse

# Get logs for a specific pod
kubectl get pods -n civicpulse
kubectl logs <pod-name> -n civicpulse
```

## 4. What to Do When Triage Starts Failing

If the AI triage system is failing (e.g., Groq API is returning 500s or timeouts):

**Diagnosis:**
1. Check the backend logs: `kubectl logs -f deployment/backend -n civicpulse | grep -i error`
2. If the logs show `Groq API Error` or `Timeout`, the primary AI is down.

**Action / Mitigation:**
- **No manual action is required immediately.** CivicPulse is designed with a **Rule-Based Fallback Engine**. The system will automatically catch the exception and route complaints to the local rule-based system (`RuleBasedTriageProvider`).
- **Post-Incident:** Check the Groq status page. Once the third-party API is stable again, the system will automatically resume using it on the next request. No restart is required.
