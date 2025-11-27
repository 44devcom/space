# Create UI Testing Agent

## Purpose

Generate a **UI test suite** for the selected UI testing tool
(Playwright, Puppeteer, or Selenium), based on:

- project stack (`laravel`, `express`, `fastapi`, etc.)
- `ui-testing.rules.json` (tool selection, docker images, service names)
- feature descriptions (from `/create feature`)

This agent focuses on **test code and configuration**, not Docker.

---

## Inputs

- `project`:
  - `id`, `title`, `stack`
- `uiTestingTool`: one of `playwright`, `puppeteer`, `selenium`
- `baseUrl`: e.g. `http://localhost:8080` or `http://api:80`
- `features`: optional list of user flows / features to cover
  - Each feature may have:
    - name
    - path
    - scenario descriptions
- `testDir` (default: `tests/ui`)

---

## Outputs

Depending on `uiTestingTool`:

### Playwright

- `playwright.config.ts` (or `.js`):
  - `use.baseURL = BASE_URL`
  - `use.headless = true` in CI
  - testDir = `tests/ui`
- Example tests:
  - `tests/ui/smoke.spec.ts`
  - `tests/ui/<feature-slug>.spec.ts` for given features

### Puppeteer

- `tests/ui/puppeteer.config.js` (optional)
- Example tests:
  - `tests/ui/smoke.puppeteer.test.js`
  - `tests/ui/<feature-slug>.puppeteer.test.js`

### Selenium

- Example tests (Node by default):
  - `tests/ui/example-selenium.test.js`
  - `tests/ui/<feature-slug>.selenium.test.js`
- Use `SELENIUM_URL` + `BASE_URL` from env.

---

## Behavior

1. Load `.cursor/rules/ui-testing.rules.json`.
2. Determine `uiTestingTool` if not provided:
   - If project stack matches `toolSelection`, use mapped tool.
   - Else use `defaultTool`.
3. Create folder structure:
   - `tests/ui`
   - `reports/ui` (for screenshots/videos)
4. For each feature:
   - Generate at least one UI scenario:
     - happy-path
     - basic validation
5. Tag UI tests for BDD/TDD integration:
   - use `@ui` or `@e2e` tags where tool supports it.

This agent is **idempotent**:
- it should update or append tests without destroying hand-written ones.
