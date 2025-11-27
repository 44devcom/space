# Docker Build Agents

This document describes the automated agents responsible for generating,
testing, linting, and optimizing Docker configurations.

---

## 1. Docker Build Agent
- Validates Dockerfiles
- Ensures minimal image sizes
- Enforces multi-stage build rules
- Runs hadolint + custom rules

## 2. Docker Compose Agent
- Ensures best practices:
  - Healthchecks mandatory
  - Secrets instead of env vars where possible
  - No bind-mounts in production

## 3. Security Agent
- Scans images with:
  - Trivy
  - Grype
- Fails on critical vulnerabilities

## 4. Documentation Agent
- Auto-generates `.mdc` service documentation
- Ensures consistent formatting and naming

---

These agents integrate into CI/CD pipelines and guarantee production-grade infrastructure.