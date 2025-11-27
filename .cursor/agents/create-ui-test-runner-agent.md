# Create UI Test Runner Agent

## Purpose

Generate **local + CI-friendly runner scripts** for UI tests.

---

## Inputs

- `uiTestingTool`
- `composeServiceName`
- Location of scripts (default: `scripts/`)

---

## Outputs

- Shell script for local / CI usage:
  - `scripts/run-ui-tests-playwright.sh`
  - or `scripts/run-ui-tests-puppeteer.sh`
  - or `scripts/run-ui-tests-selenium.sh`

---

## Run Strategy

### Playwright / Puppeteer

- `docker compose run --rm <service-name> <extra args>`

### Selenium

- Bring up selenium, run tests, then stop selenium:

```bash
docker compose up -d selenium
docker compose run --rm ui-tests-selenium "$@"
docker compose stop selenium
```

The agent must ensure scripts are:

- executable (chmod +x)
- safe (set -euo pipefail)
- parameter-forwarding ("$@").
