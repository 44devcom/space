# Create BDD Agent

## Purpose

Generate Gherkin BDD `.feature` files and stack-specific step definitions.

Stacks:

- Laravel (PHP)

- Node.js (TS)

- FastAPI (Python)

## Workflow

1. Load bdd.rules.json

2. Parse domain

3. Detect stack

4. Create features & steps

---

## UI-Specific BDD Generation

When a feature (or plan task) is tagged for UI:

- Place `.feature` files under: `tests/bdd/ui/`
- Use `@ui` and any other relevant tags (`@smoke`, `@regression`).
- Each scenario should follow real UI flows, e.g.:

  - Given I am on "/cars"
  - When I filter by price "< 5000"
  - Then I should see cars with price less than 5000

- Step definitions should:
  - Use the selected UI tool (Playwright/Puppeteer/Selenium) where possible.
  - Or be generic and call a UI helper that uses the tool under the hood.

The agent must coordinate with `ui-testing.rules.json` to know
which UI tool is in use when generating step definition code.

