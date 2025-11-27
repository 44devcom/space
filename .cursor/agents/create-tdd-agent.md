# Create TDD Agent

## Purpose

Generate failing TDD tests for domain logic.

Supported:

- Laravel (PHPUnit/Pest)

- Node.js (Jest)

- FastAPI (pytest)

## Workflow

1. Load tdd.rules.json  

2. Inspect domain  

3. Detect stack  

4. Generate failing tests in correct format

---

## UI-Specific TDD Test Generation

For UI-related tasks or features, `create-tdd-agent` should:

- Generate **Page Object** classes or helpers in `tests/ui/page-objects/`:
  - e.g., `CarsPage`, `AlertsPage`
- For Playwright/Puppeteer:
  - Provide reusable functions:
    - `login()`
    - `goToCarsList()`
    - `createFilter()`
- For Selenium:
  - Provide WebDriver-based page object classes.

Tests should:

- Be smaller, unit-like or component-level where applicable.
- Support being called from BDD step definitions and direct TDD tests.
- Avoid duplicating BDD flows; instead expose building-block APIs.

The agent must respect the chosen `uiTestingTool`.

