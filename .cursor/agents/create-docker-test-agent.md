# Docker Test Master Agent

## Overview
This agent is responsible for generating, orchestrating, and executing a **complete, isolated Docker Test Environment** for validating all services, schemas, models, endpoints, controllers, Dockerfiles, and infrastructure components.

It ensures all generated Docker services are:
- syntactically correct
- buildable
- startable
- healthy
- connected
- contract-compliant
- schema-valid
- secure
- production-ready

This agent combines the functionality of:
- create-docker
- create-docker-test
- deep schema testers
- endpoint testers
- database and redis validators
- security scanners

---

# Responsibilities

## 1. Generate Test Environment Structure
When invoked, the agent must create:

```
tests/docker/
├── docker-compose.test.yml
├── results/
│   ├── report.txt
│   ├── logs/
│   ├── health/
│   ├── connectivity/
│   ├── schema/
│   └── errors.log
└── scripts/
    ├── health.sh
    ├── connectivity.sh
    ├── endpoints.sh
    ├── model-tests-laravel.sh
    ├── model-tests-fastapi.py
    ├── database-tests.sh
    ├── redis-tests.sh
    ├── schema-openapi.sh
    ├── schema-json.sh
    ├── security.sh
    ├── performance.sh
    ├── crud-generated-tests.sh
    ├── event-generated-tests.sh
    ├── feature-generated-tests.sh
    └── test-runner.sh
```

Each script must be:
- auto-generated
- executable
- self-contained

---

# Test Categories The Agent Must Generate

## A) Health Tests
Validate that containers run correctly:
- Laravel: `php -v`
- FastAPI: `python --version`
- MySQL: `mysqladmin ping`
- Redis: `redis-cli ping`
- Nginx: `nginx -t`
- Mailpit: API status

## B) Connectivity Tests
Validate real network connectivity:
- HTTP 200 responses
- API JSON validity
- Redis GET/SET
- MySQL SELECT queries
- Mailpit message injection and retrieval

## C) Endpoint Tests
Generated based on introspection:
- Laravel route:list → test every route
- FastAPI openapi.json → test every endpoint
- Check expected methods (GET/POST/etc.)
- Validate response codes
- Validate JSON structure

## D) Model Tests
### Laravel:
- factory creation
- relationship resolution
- casts & guarded fields
- DB writes/reads

### FastAPI:
- Pydantic model instantiation
- schema validation
- enum handling

## E) Schema Tests
### FastAPI OpenAPI:
- Download `/openapi.json`
- Validate with jsonschema

### Laravel JSON:
- Validate output schema consistency
- Compare with stored schemas

## F) Database Tests
- Table existence
- Field existence
- Index presence
- Foreign keys
- Migrations validity

## G) Redis Tests
- PING
- SET/GET
- TTL tests
- Memory policy

## H) Security Tests
- nginx security headers
- Laravel security:check
- CORS validation
- Header validation
- Trivy scan (optional)

## I) SSL/HTTPS Tests
If SSL is configured:
- Test HTTP → HTTPS redirect:
  ```bash
  curl -I http://localhost --fail
  curl -I http://localhost --fail | grep -q "301\|302" || exit 1
  ```
- Test HTTPS endpoint (with insecure flag for self-signed or Let's Encrypt):
  ```bash
  curl -I https://localhost --insecure --fail
  curl -k https://example.com/health
  ```
- Test ACME challenge endpoint:
  ```bash
  curl -f http://localhost/.well-known/acme-challenge/test
  ```
- Validate SSL certificate:
  ```bash
  openssl s_client -connect localhost:443 -servername example.com < /dev/null
  ```
- Test SSL protocols (should reject TLSv1.0, TLSv1.1):
  ```bash
  openssl s_client -connect localhost:443 -tls1_2
  openssl s_client -connect localhost:443 -tls1_3
  ```

## I) Performance Tests
Light load tests:
- `ab`
- `wrk`
- response latency threshold

## J) CRUD Generated Code Tests
Tests all generated CRUD code that exists in the codebase (from `create-crud`):

### Discovery Phase:
- Auto-discover all generated CRUD code in:
  - `generated/laravel/app/Http/Controllers/*Controller.php`
  - `generated/python/routers/*_router.py`
  - `generated/python/services/*_service.py`
  - `generated/node/controllers/*.js` (if Express code exists)
  - `generated/sql/*.sql` (if SQL procedures exist)

### Laravel Generated CRUD Tests:
For each discovered Laravel controller:
- Test controller methods (index, show, store, update, destroy)
- Test request validation (StoreRequest, UpdateRequest)
- Test resource formatting (Resource classes)
- Test routes are registered and accessible
- Test database operations (create, read, update, delete)
- Validate response formats match JSON Schema
- Test error handling (404, validation errors, etc.)

### Python FastAPI Generated CRUD Tests:
For each discovered FastAPI router:
- Test all endpoints (GET list, GET by id, POST, PUT, DELETE)
- Test Pydantic DTO validation (CreateDTO, UpdateDTO, ResponseDTO)
- Test service layer methods
- Validate type hints match JSON Schema
- Test database operations through service layer
- Validate response schemas match OpenAPI spec

### Express Generated CRUD Tests (if exists):
For each discovered Express controller:
- Test controller methods
- Test service layer
- Test route handlers
- Test validators (if enabled)
- Test database operations

### SQL Generated CRUD Tests (if exists):
For each discovered stored procedure:
- Test procedure execution
- Test CRUD operations (create, read, update, delete)
- Validate table structure matches schema

### Validation Checks:
- All generated CRUD files are syntactically correct and loadable
- Controllers/routers handle all CRUD operations correctly
- Request/DTO validation rules match JSON Schema
- Routes are properly registered and accessible
- Database operations work correctly (create, read, update, delete)
- Response formats match expected schemas
- Error handling is implemented and works
- Cross-stack compatibility (if same model has CRUD in multiple stacks)

## K) Event Generated Code Tests
Tests all generated event code that exists in the codebase (from `create-event`):

### Discovery Phase:
- Auto-discover all generated event code in:
  - `schemas/events/*/*.json` (event schemas)
  - `generated/python/events/*_events.py` (Python events)
  - `generated/python/events/*_handlers.py` (Python handlers)
  - `generated/laravel/Events/*.php` (Laravel events)
  - `generated/laravel/Listeners/*.php` (Laravel listeners)
  - `generated/node/*_event_bus.js` (Node event bus)
  - `generated/node/*.js` (Node events and handlers)
  - `generated/sql/*_trigger.sql` (SQL triggers)

### Python FastAPI Generated Event Tests:
For each discovered Python event:
- Test event class instantiation (AbstractEvent inheritance)
- Test event payload validation (Pydantic models)
- Test event name property
- Test sync handler execution
- Test async handler execution
- Test event registration and dispatch
- Validate payload types match schema

### Laravel Generated Event Tests:
For each discovered Laravel event:
- Test Event class instantiation
- Test Listener class execution
- Test EventServiceProvider registration
- Test event broadcasting (if broadcast enabled in schema)
- Test event firing and handling
- Validate event payload structure

### Node Express Generated Event Tests (if exists):
For each discovered Node event:
- Test event bus functionality
- Test event class instantiation
- Test handler class execution
- Test event emission and handling
- Validate event payload structure

### SQL Generated Event Tests (if exists):
For each discovered SQL trigger:
- Test trigger creation
- Test trigger execution on table events
- Validate event table structure
- Test trigger logic

### Validation Checks:
- All generated event files are syntactically correct and loadable
- Event classes instantiate properly with correct payloads
- Handler classes execute correctly when events are dispatched
- Event registration works (EventServiceProvider, event bus, etc.)
- Payload validation matches event schema
- Broadcast events work correctly (if enabled)
- Cross-stack event compatibility (if same event exists in multiple stacks)
- Event handlers handle errors gracefully

## L) Feature Generated Code Tests
Tests all generated feature code that exists in the codebase (from `create-feature`):

### Discovery Phase:
- Auto-discover all generated features in:
  - `schemas/features/*.json` (feature schemas)
  - `features/*/laravel/` (Laravel feature code)
  - `features/*/python/` (Python FastAPI feature code)
  - `features/*/express/` (Node Express feature code)
  - `features/*/sql/` (SQL feature code)
  - `docs/*.md` (feature documentation)

### Laravel Generated Feature Tests:
For each discovered Laravel feature:
- Test Controllers (if generated)
- Test Models (if generated)
- Test Requests validation (if generated)
- Test Resources formatting (if generated)
- Test Routes registration and accessibility
- Test Migrations (run migrations, verify tables)
- Test Seeders (execute seeders, verify data)
- Test feature folder structure matches specification
- Test dependencies (imports/use statements work)

### Python FastAPI Generated Feature Tests:
For each discovered Python feature:
- Test routers (if generated)
- Test schemas/DTOs (if generated)
- Test services (if generated)
- Test models (if model provided in schema)
- Test factories (if generated)
- Test seeders (if generated)
- Test feature folder structure
- Test dependencies (imports work)

### Node Express Generated Feature Tests (if exists):
For each discovered Express feature:
- Test controllers (if generated)
- Test services (if generated)
- Test routes (if generated)
- Test validators (if generated)
- Test feature folder structure
- Test dependencies (requires work)

### SQL Generated Feature Tests (if exists):
For each discovered SQL feature:
- Test CRUD procedures (if generated)
- Test table creation schema (if generated)
- Test table structure matches schema
- Test procedures execute correctly

### Documentation Tests (if exists):
For each discovered feature documentation:
- Validate markdown file exists
- Test markdown formatting is valid
- Verify documentation completeness

### Validation Checks:
- Feature folder structure matches specification from schema
- Schema file exists and is valid JSON
- All stack-specific files are syntactically correct and loadable
- Dependencies are properly resolved (imports/use statements work)
- Endpoints work correctly (test all routes/endpoints)
- Models (if provided) are valid and work correctly
- Migrations run successfully (if Laravel feature)
- Seeders execute correctly (if provided)
- Cross-stack compatibility maintained (if feature spans multiple stacks)
- Feature integration works (features can work together if dependencies exist)

---

# Execution Workflow

The agent must:

1. **Generate all test scripts**  
2. **Generate docker-compose.test.yml**  
3. **Generate test-runner.sh**  
4. Run:
```bash
docker compose -f docker-compose.test.yml build --no-cache
docker compose -f docker-compose.test.yml up -d
```
5. **Run health tests**  
6. **Run connectivity tests**  
7. **Run schema tests**  
8. **Run endpoint tests**  
9. **Run model tests**  
10. **Run database tests**  
11. **Run redis tests**  
12. **Run security tests**  
13. **Run CRUD generated code tests** (test all generated CRUD code)
14. **Run event generated code tests** (test all generated events)
15. **Run feature generated code tests** (test all generated features)
16. **(Optional) performance tests**  
17. Save results to `/tests/docker/results`  
18. Shut environment down  
19. Produce a PASS/FAIL report  

---

# PASS / FAIL Logic

## Success Conditions
All tests must return exit code 0.

## Failure Conditions
If any of these logs contain “error”, “fatal”, “exception”, “panic”:
- docker build logs  
- container logs  
- test-runner logs  
- health logs  
- connectivity logs  
- schema validation logs  

The agent MUST output:

```
TEST SUITE FAILED
See tests/docker/results/report.txt
```

Otherwise:

```
ALL DOCKER SERVICES VALID — TEST SUITE PASSED
```

---

# Command Trigger

This agent is activated when the user runs:

```
/create docker-test
```

or requests:

```
/run docker tests
```

or:

```
validate all docker services
```

---

# Final Output (Required)

After running, the agent MUST generate:

```
tests/docker/results/report.txt
tests/docker/results/logs/docker.log
tests/docker/results/health/health.log
tests/docker/results/connectivity/connectivity.log
tests/docker/results/schema/openapi-validation.json
tests/docker/results/schema/json-validation.json
tests/docker/results/crud/crud-test-results.json
tests/docker/results/events/event-test-results.json
tests/docker/results/features/feature-test-results.json
tests/docker/results/errors.log
```

---

# Notes
- The test environment must be **isolated** from production docker-compose.
- No bind volumes from production may be used.
- All scripts must be idempotent.
- Agent must automatically retry failed HTTP tests (3 retries).
- Output must be fully deterministic.
- CRUD, Event, and Feature tests must discover and test all generated code that exists in the codebase.
- Tests should auto-discover generated code from `generated/`, `features/`, and `schemas/` directories.
- Generated code from CRUD/Event/Feature commands must be tested in the Docker environment.
- Test results must clearly indicate which generated files/components passed/failed.