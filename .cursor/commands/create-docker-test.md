# Create Docker Test Command

## Purpose
Run the full Docker Test Master Agent to automatically generate and execute the complete Docker test environment, including auto-discovery of endpoints, models, and schemas.

## Usage
```
/create docker-test
```

## What It Does
- Generates the entire test environment under `tests/docker/`
- Auto-discovers:
  - Laravel routes
  - FastAPI endpoints
  - Laravel models
  - FastAPI Pydantic models
  - Database schema
- Runs the full Docker Test Suite:
  - Health tests
  - Connectivity tests
  - Model tests
  - Schema tests
  - Endpoint tests
  - Database tests
  - Redis tests
  - Security tests
  - Performance tests
  - **CRUD generated code tests** (tests all generated CRUD code from create-crud)
  - **Event generated code tests** (tests all generated events from create-event)
  - **Feature generated code tests** (tests all generated features from create-feature)
- Produces a PASS/FAIL test report.

## Output
The command produces:
- `tests/docker/results/report.txt`
- detailed logs
- schema snapshots
- health + connectivity test outputs
- CRUD test results (for all generated CRUD code)
- Event test results (for all generated events)
- Feature test results (for all generated features)

This command always triggers the **Docker Test Master Agent**.