# Create UI CI Agent

## Purpose

Generate CI configuration fragments to run Dockerized UI tests automatically.

---

## Inputs

- CI type:
  - `github-actions` (default)
  - (future: gitlab, bitbucket, etc.)
- `uiTestingTool`
- `composeFile` (default: `docker-compose.yml`)
- `runnerScript` (from `runnerScriptNames` in ui-testing.rules.json)

---

## Outputs

For GitHub Actions:

- `.github/workflows/ui-tests.yml` that:
  - checks out code
  - sets up Docker
  - builds images (if needed)
  - runs UI tests via `scripts/run-ui-tests-<tool>.sh`
  - archives reports (`reports/ui`) as artifacts

---

## Example Workflow (simplified)

```yaml
name: UI Tests

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  ui-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build images
        run: docker compose build

      - name: Run UI tests
        run: bash scripts/run-ui-tests-PLAYWRIGHT_OR_OTHER.sh

      - name: Upload UI test artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: ui-test-reports
          path: reports/ui
```

The agent adapts the script name and service based on uiTestingTool.
