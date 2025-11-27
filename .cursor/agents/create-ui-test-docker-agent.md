# Create UI Test Docker Agent

## Purpose

Generate Docker infrastructure for running UI tests using the chosen tool:

- Build Dockerfile(s) for UI test runner
- Add/merge docker-compose services for UI tests
- Wire them into the test pipeline

This agent uses `.cursor/rules/docker-playwright.mdc`,
`docker-puppeteer.mdc`, `docker-selenium.mdc` as templates.

---

## Inputs

- `project.stack`
- `uiTestingTool` (`playwright` / `puppeteer` / `selenium`)
- `dockerRoot` (default: `docker/`)
- `composeFile` (default: `docker-compose.yml` or extra test compose)
- `baseUrl` (inside Docker, e.g. `http://api:80`)

---

## Outputs

- Dockerfiles:
  - `docker/ui/playwright/Dockerfile`
  - or `docker/ui/puppeteer/Dockerfile`
  - or `docker/ui/selenium/runner.Dockerfile`
- Compose snippet or file:
  - `ui-tests-playwright` / `ui-tests-puppeteer` / `ui-tests-selenium`
  - `selenium` service for Selenium mode
- Ensures:
  - `tests/ui` is mounted
  - `reports/ui` is mounted
  - `BASE_URL` env is set
- A short README snippet in `docker/AGENTS.md` describing how to run UI tests.

---

## Behavior

1. Read `.cursor/rules/ui-testing.rules.json`:
   - use `dockerImages` & `composeServiceNames`.
2. Read the matching `.mdc`:
   - `docker-playwright.mdc` / `docker-puppeteer.mdc` / `docker-selenium.mdc`.
3. Generate or update Dockerfiles and compose services.
4. Ensure `docker-compose.test.yml` (or equivalent) includes UI test services.
5. Preserve existing non-UI services.
