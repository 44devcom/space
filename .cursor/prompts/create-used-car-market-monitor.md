This service monitors used car listings across multiple websites, parses data from multiple sources, maintains historical changes, and sends alerts based on filters.
The system must include full Dockerized infrastructure, FastAPI backend, MVC-style structure, workers, API, SSL, GUI, ORM, DDD, CRUD, GraphQL, DB, email service, cache/queue, healthchecks, UI tests, and test environments.

## 1. Domain Model

The system must manage the following domain entities:

### Entities

- Car (canonical record)
- CarListing (per-website listing)
- CarWebsite (listing website metadata)
- CarFieldMapping (mapping external → internal fields)
- Filter (user rules)
- Alert (Filter + Email)
- ChangeEvent (history of changes)
- FilterMatch (filter match log)

### Relationships

- A Car has many CarListings
- A CarWebsite has many CarListings
- A CarListing has many ChangeEvents
- A CarListing has many FilterMatches
- A Filter has many FilterMatches
- An Alert belongs to a Filter

All domain models must include:

- created_at
- updated_at
- deleted_at (soft delete)

### 🏗️ Domain-Driven Design (DDD) Requirements

Use Domain-Driven Design principles:

- **Entities**: Car, CarListing, CarWebsite, Filter, Alert (with unique identity)
- **Value Objects**: Price, Mileage, Location, FilterRule (immutable, no identity)
- **Domain Services**: FilterEvaluationService, ChangeDetectionService, AlertTriggerService
- **Aggregates**: Car (root aggregate), Filter (root aggregate)
- **Domain Events**: CarListingCreated, CarListingUpdated, FilterMatched, AlertTriggered

Define models, schemas, relations, and domain logic.

Provide OpenAPI, GraphQL, and JSON Schema models.

Include filters, mapping, event history, soft delete, etc.

## 2. CRUD + API Requirements

Must provide CRUD endpoints for:

- Car
- CarListing
- CarWebsite
- Filter
- Alert
- CarFieldMapping

Each entity must have:

- REST CRUD endpoints
- GraphQL type & resolvers
- OpenAPI schema definitions

### 🖥️ API Backend Structure

Generate backend structure for one of:

- Laravel, or
- Express.js (Node), or
- FastAPI (Python)

With:

- Controllers
- Repositories
- ORM mappings
- CRUD endpoints
- Validation rules
- Pagination
- BDD & TDD tests
- Modular folder structure

## 3. Email Service

The email system must:

- Run in a dedicated Docker service (Mailpit / SMTP)
- Support HTML + text templates
- Support batching
- Support async sending from worker

Alerts must integrate with this service.

## 3.5 Database & ORM

Generate:

- Migrations
- Seeders
- ORM entity classes
- Relations
- History tracking
- Soft delete fields

Ensure compatibility with:

- Laravel Eloquent
- TypeORM / Prisma (Node)
- SQLAlchemy (Python)

## 4. Filter Service

Evaluate filter rules using:

- Operators (>, <, =, contains, range, keyword)
- Nested conditions (AND/OR)

Must support bulk evaluation

Must support asynchronous evaluation inside worker queues

## 5. Alert Service

An alert is: Filter + Email target.

Alerts must trigger when:

- New car listing matches a filter
- Any listing field changes
- ChangeEvent is created

Alert pipeline must be event-driven and async.

## 6. Logging & Event Store

Must store:

**item_changes table:**

- field
- from
- now
- at (timestamp)

**filter_matches table:**

- filter_id
- item_id
- matched_at

All change logs must be preserved (append-only).

## 7. Time-Based Browsing

The system must support:

- Show state of all items at a given historical date
- List items created in a date range
- List items updated in a date range
- List items deleted in a date range

This requires:

- ChangeEvent reconstruction
- Soft delete support
- Historical snapshot queries

## 8. Massive Asynchronous Processing

A fully asynchronous, horizontally scalable pipeline must process:

**(a) Mass insert/update/delete items**

- Run in dedicated worker containers
- Must produce ChangeEvents
- Must evaluate filters
- Must trigger alerts

**(b) Sitemap parsing**

- ~ 40,000 items per file
- ~ 3 files per run

**(c) Listing file parsing**

- ~ 100 items per file
- ~ 1,000 files per run

**(d) HTML file parsing**

- ~ 100,000 items per run

Each pipeline must:

- Run asynchronously
- Log errors + partial failures
- Write change events
- Write filter matches
- Queue follow-up tasks
- Be idempotent

## 9. Performance Requirements

Must support high throughput: 100k+ items < 10 minutes

Must support:

- Multiple worker containers
- Parallel parsing
- Queue-based scaling

Must use:

- Minimal locking
- Bulk operations
- Efficient diff-based change detection

## 🔥 10. Infrastructure, Docker, Runtime & Environment Requirements

- THIS ensures Docker appears in your plan.
- UI Testing: Playwright in a dedicated Docker service

### 10.1 Full Dockerized Architecture (required)

The entire system must run in Docker:

**Mandatory Docker services:**

- api → main backend (Laravel/Express/FastAPI/etc.)
- worker → async pipeline worker(s)
- queue → Redis
- db → MySQL
- cache → Redis
- mail → Mailpit (SMTP + Web UI)
- scheduler → cron / queue scheduler
- docker-test → test environment
- nginx (optional) → reverse proxy

Each service must include:

- Healthchecks
- Logging
- Resource limits
- Restart policies
- Environment injection from .env

### 10.2 Docker Compose Requirements

Create:

- `docker-compose.yml`
- `docker-compose.override.yml`
- `docker-compose.test.yml`

Include:

- networks
- volumes
- environment variables
- startup ordering
- healthcheck dependencies (depends_on: condition: service_healthy)

### 10.3 Dockerfiles (multi-stage)

Each Dockerfile must:

- Use multi-stage builds (dev / prod)
- Use non-root user
- Include build caching layers
- Include composer/npm/pip install layers
- Include healthcheck commands

### 10.4 Environment Variable Requirements

Must create sample `.env.example`, including:

**Database**
```
DB_HOST=db
DB_PORT=5432
DB_DATABASE=cars
DB_USERNAME=root
DB_PASSWORD=secret
```

**Redis/Queue**
```
REDIS_HOST=queue
REDIS_PORT=6379
QUEUE_CONNECTION=redis
```

**Mail**
```
MAIL_HOST=mail
MAIL_PORT=1025
MAIL_USER=null
MAIL_PASSWORD=null
MAIL_FROM=no-reply@cars.com
```

**Application**
```
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost
```

**Worker Pipeline**
```
WORKER_CONCURRENCY=10
WORKER_BATCH_SIZE=1000
WORKER_MAX_RETRIES=3
```

### 10.5 Worker Architecture

Workers must:

- Run as separate containers
- Process:
  - Alerts
  - Filters
  - Mass parsing
  - ChangeEvent creation
  - FilterMatch creation
- Support scaling: `docker compose up --scale worker=8`
- Support task routing

### 10.6 Docker Test & UI Test Environment

The Docker test stack must support:

- Unit tests (TDD) for domain, application, infrastructure, API layers
- Feature/BDD tests (REST + GraphQL)
- API tests (FastAPI endpoints, including error cases)
- Snapshot tests for critical responses

Integration tests with:
- Queue + Mail + DB + Cache

UI tests:

- Playwright service (e.g. ui-tests-playwright in Docker)
- Test runner script (e.g. scripts/run-ui-tests-playwright.sh)
- CI integration (GitHub Actions workflow for running UI tests in Docker)
- Using a dedicated docker-tests environment.

## 🔐 11. SSL + Let's Encrypt + Nginx

Configure:

- Full HTTPS setup
- Let's Encrypt automatic certificate provisioning
- ACME challenge handling via Nginx
- Certbot init scripts
- Renewal scripts
- Cron example
- Diffie–Hellman (dhparam) generation
- Security headers
- OCSP stapling

Nginx must have:

- HTTP→HTTPS redirect
- SSL configuration
- Proxy pass to API
- Static file handling

Generate all scripts needed:

- `scripts/enable-ssl.sh`
- `scripts/generate-dhparam.sh`
- `scripts/renew-ssl.sh`

## 🧩 12. GUI Applications

### ✔ Web GUI (Next.js + ShadCN + Mermaid + Monaco)

Generate:

- Dashboard
- CRUD UI
- Parallel Plan Execution viewer
- Mermaid diagrams
- JSON editor
- Logs console
- Agent runner UI
- File tree viewer
- Nginx Config Editor
- SSL Certificate Manager (renew/enable/reload)

## 🚀 13. SSL Certificate Manager GUI

Include in all GUIs:

Certificate status:

- issuer
- validity dates
- days remaining

Button: Run certificate request

Button: Renew

Button: Reload Nginx

View certbot logs

Warnings if <30 days to expiry

## ⚙️ 14. Interactive Nginx Config Editor

All GUIs must include:

- Editor (Monaco for web)
- Load config from API
- Edit config
- Save & Test
- Save, Test, Reload
- Validation output from nginx -t
- Display of errors with line numbers

Backend must expose:

- GET /api/ssl/nginx-config
- POST /api/ssl/nginx-config
- POST /api/ssl/reload

## 📦 15. Plan → Wizard → Run-Plan Pipeline Integration

The generated plan must include:

- Infrastructure → Docker + SSL milestone
- Backend → API Controllers
- Domain → DDD models
- ORM → migrations + entities
- GUI → Web
- Nginx interactive editor milestone
- SSL manager milestone
- Tests → BDD/TDD

Plan structure:

```
Project
  └─ Milestones
       └─ Issues
            └─ Tasks
                 └─ Subtasks
```

Wizard must generate:

- Parallel-safe tasks
- Dependencies
- Execution layers
- Mermaid DAG diagrams

Run-plan must:

- Execute SSL/Docker sequentially
- Execute GUI tasks
- Execute models, schemas, etc. in parallel
- Resume with --continue

## 🧪 16. Tests (BDD + TDD)

Generate:

- BDD scenarios (Given/When/Then)
- Unit tests
- Integration tests
- GUI tests where applicable
- Docker test environment
- SSL test commands (HTTP, HTTPS, certbot dry-run)

## 📊 17. Mermaid Diagrams (auto-generate)

Include diagrams:

- Domain model
- API flow
- Docker architecture
- SSL handshake
- GUI flow
- Plan DAG
- Parallel executor timeline

## 📁 18. Final Output Format

The generator must output:

- `/api` backend
- `/gui/web/next`
- `/docker`
- `/nginx`
- `/ssl`
- `/scripts`
- `/mermaid`
- `/tests`
- `/schemas`
- `.cursor/plan.json`
- Agents + rules if needed

Everything must be runnable with:

```bash
docker compose up -d
```

And GUIs must run independently.

## 🏆 Final Message

This improved prompt:

✔ Includes all SSL features
✔ Includes GUI → SSL → Nginx integration
✔ Works with your GitHub-style Plan system
✔ Works with the Parallel Executor
✔ Covers web stack
✔ Ensures production-ready HTTPS
✔ Ensures everything is auto-generated
