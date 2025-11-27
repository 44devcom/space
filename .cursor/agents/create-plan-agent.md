# Create Plan Agent (GitHub-style)

## Purpose

Convert a natural language project request into a **GitHub-style project plan**.

The structure:

- Project
- Milestones
- Issues
- Tasks
- Subtasks

Saved into:

```text
.cursor/plans/<project-id>.plan.json
```

Then executable via `run-plan-agent`.

---

## Inputs

A description such as:

- "Car Market Monitor in Laravel with DDD, MVC, API, ORM, Docker, BDD & TDD"
- "FastAPI microservice with CRUD and OpenAPI"

The agent must infer:

- project id, title, description
- domain name
- stack (laravel/node/fastapi/generic)

---

## Stack Detection

- Contains "laravel", "php" → stack = "laravel"
- Contains "node", "express", "ts" → stack = "node"
- Contains "fastapi", "python" → stack = "fastapi"
- Else → stack = "generic"

---

## Default Milestones

1. Domain (DDD / schema / events)
2. MVC (models / views / controllers)
3. API (OpenAPI / GraphQL)
4. Persistence (ORM / CRUD)
5. Infrastructure: Docker & SSL (docker compose, Nginx, HTTPS with Let's Encrypt)
6. Quality (BDD / TDD / test runners)
7. UI Testing (Dockerized UI test environment)
8. GUI Applications (Desktop PySide6, Mobile Kotlin, Web Next.js)
9. SSL & HTTPS Setup (Nginx SSL, Let's Encrypt, Certbot)

---

## Task Types

Each task receives a `type`:

- ddd
- schema
- event
- mvc-model
- mvc-controller
- mvc-view
- openapi
- graphql
- orm
- crud
- docker
- docker-test
- bdd
- tdd
- tests
- ui-docker
- ui-tests
- ui-runner
- ui-ci
- gui
- gui-desktop-pyside6
- gui-mobile-kotlin
- gui-web-next
- ssl
- nginx
- certbot
- custom

---

## Workflow

1. Analyze text → extract title/domain/stack.
2. Build full milestone → issue → task → subtask hierarchy.
3. Validate against `plan.schema.json`.
4. Save plan to `.cursor/plans/<project-id>.plan.json`.
5. Print milestone/task overview.

---

## GUI Milestone Injection

If the project description includes:
- "desktop"
- "mobile"
- "gui"
- "web app"
- "ui"
- "dashboard"
- "interface"

THEN the plan MUST include `milestone-gui`.

If not included explicitly, Wizard will still add it by default unless user opts-out by adding:
`--no-gui`.

The GUI milestone contains:
- Issue: "Generate Multiple GUI Clients"
  - Task: "Generate PySide6 desktop GUI" (type: `gui-desktop-pyside6`, priority: 1)
  - Task: "Generate Android Kotlin GUI" (type: `gui-mobile-kotlin`, priority: 2)
  - Task: "Generate Web GUI with Next.js" (type: `gui-web-next`, priority: 3)

---

## SSL Milestone Injection

If the project description includes:
- "domain"
- "email"
- "https"
- "ssl"
- "certificate"
- "letsencrypt"
- "certbot"
- "production"

THEN the plan MUST include `milestone-ssl`.

The SSL milestone contains:
- Issue: "Configure Nginx SSL"
  - Task: "Generate SSL Nginx config" (type: `nginx`, priority: 1)
  - Task: "Generate Diffie-Hellman parameters script" (type: `ssl`, priority: 2)
  - Task: "Generate certbot initialization script" (type: `certbot`, priority: 3)
  - Task: "Add certbot service to docker-compose" (type: `docker`, priority: 4)
  - Task: "Generate SSL renewal script" (type: `ssl`, priority: 5)

SSL tasks must run sequentially (not parallel-safe).

---

## Infrastructure Milestone Structure

The Infrastructure milestone (`milestone-infrastructure`) contains:

### Issue: Base Docker Compose Setup
- Task: "Generate base docker-compose.yml" (type: `docker`, priority: 1)
  - Subtasks:
    - "Add API service"
    - "Add database service"
    - "Add Redis service"
    - "Add Nginx reverse proxy"

### Issue: Nginx SSL & HTTPS
- Depends on: "Base Docker Compose Setup"
- Task: "Generate Nginx SSL configuration" (type: `docker`, priority: 2)
  - Subtasks:
    - "Redirect HTTP→HTTPS"
    - "Serve /.well-known/acme-challenge from letsencrypt root"
    - "Configure ssl_certificate and ssl_certificate_key"
    - "Configure ssl_dhparam"
- Task: "Generate SSL scripts (dhparam, certbot, renew)" (type: `docker`, priority: 3)
  - Depends on: "Generate Nginx SSL configuration"
  - Subtasks:
    - "Create scripts/generate-dhparam.sh"
    - "Create scripts/enable-ssl.sh (certbot init)"
    - "Create scripts/renew-ssl.sh and cron example"
- Task: "Add certbot service to docker-compose" (type: `docker`, priority: 4)
  - Depends on: "Generate Nginx SSL configuration"
  - Subtasks:
    - "Mount letsencrypt and ACME webroot volumes"
    - "Configure certonly --webroot command"

### Issue: Nginx SSL Config Editor Integration (Optional)
- Depends on: "Nginx SSL & HTTPS"
- Task: "Add /api/ssl/nginx-config endpoints" (type: `feature`, priority: 5)
- Task: "Add NginxConfigEditor to Next.js GUI" (type: `gui-web-next`, priority: 6)
- Task: "Add Nginx SSL config editor to PySide6 GUI" (type: `gui-desktop-pyside6`, priority: 7)
