# Create UI Tests Command

## Purpose
Generate a complete UI testing environment with Dockerized test execution, test scripts, and CI integration.

## Usage
```
/create ui-tests [playwright|puppeteer|selenium]
```

If no tool is specified, the wizard will:
1. Consult `.cursor/rules/ui-testing.rules.json`
2. Auto-detect stack from project
3. Select tool based on `toolSelection` mapping
4. Fallback to `defaultTool`

## What It Does
- Generates UI test Docker service configuration
- Creates test directory structure:
  - `tests/ui/config/` - Tool configuration files
  - `tests/ui/helpers/` - Page objects, fixtures, utilities
  - `tests/ui/tests/` - Test files
  - `tests/ui/reports/` - Test reports, videos, screenshots
- Generates example tests:
  - Login flow
  - CRUD operations
  - Screenshot and video capture
- Generates test runner script (`run-ui-tests.sh`)
- Integrates UI tests into CI workflow
- Adds `run-ui-tests` command to plan execution

## Output
The command produces:
- `tests/ui/Dockerfile`
- `tests/ui/config/<tool>.config.js`
- `tests/ui/tests/*.spec.js`
- `tests/ui/helpers/**/*.js`
- `tests/ui/run-ui-tests.sh`
- Updated `docker-compose.yml` or `docker-compose.test.yml`
- `.github/workflows/ui-tests.yml` (if CI integration requested)

## Tool Selection
- **playwright**: Modern, cross-browser testing (default for most stacks)
- **puppeteer**: Chrome/Chromium focused testing
- **selenium**: Legacy browser support, WebDriver standard

This command triggers the complete UI testing setup including all related agents.
