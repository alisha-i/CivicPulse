# ADR 0003: Deploy-by-SHA for Kubernetes

**Status:** Accepted
**Date:** 2026-09-28

## Context and Problem Statement
When deploying our backend and frontend applications to Kubernetes, we need a reliable way to tag Docker images and update deployments. Using the `latest` tag is an anti-pattern because Kubernetes may not detect a change if the tag name (`latest`) remains the same, preventing new rollouts. It also makes rollbacks difficult.

## Decision
We decided to adopt a **Deploy-by-SHA** strategy. 
In our GitHub Actions CI/CD pipeline (`cd.yml`), Docker images are tagged with the specific Git commit SHA (`${{ github.sha }}`). The CD pipeline then uses `sed` (or Kustomize) to patch the Kubernetes deployment YAMLs with this exact SHA before running `kubectl apply`.

## Consequences
**Good:**
- **Traceability:** Every pod running in Kubernetes can be perfectly mapped back to the exact Git commit that produced it.
- **Reliable Rollouts:** Changing the image tag forces Kubernetes to perform a rolling update.
- **Instant Rollbacks:** If a deployment fails, we can easily roll back to the previous known-good SHA tag.

**Bad:**
- Container registries (GHCR) can fill up quickly with many uniquely tagged images, requiring lifecycle management/cleanup policies.
