# Create Wizard Agent (GitHub-style)

## Purpose

Top-level UX flow:

> "Idea" → Plan → Execution

This agent:

1. Reads the description.
2. Calls `create-plan-agent`.
3. Saves a GitHub-style plan.
4. Calls `run-plan-agent`.

---

## Usage

```text
/create wizard "Car Market Monitor in Laravel with DDD, MVC, API, ORM, Docker, BDD & TDD"
```

---

## Behavior

1. Parse description → detect stack & domain.
2. Call create-plan-agent → generate `.cursor/plans/<id>.plan.json`
3. Print plan overview:
   - milestones
   - issues
   - task types
4. Execute plan:
   - initial `--dry` preview
   - final run

This agent does not generate code; it orchestrates planning and execution.

---

## UI Testing Detection

The wizard MUST consult `.cursor/rules/ui-testing.rules.json` and automatically decide:

1. If user specifies a tool → use it.
2. If no tool is specified:
   - Detect frontend or backend stack from project description.
   - Match stack to `toolSelection` in `ui-testing.rules.json`.
   - Fallback to `defaultTool`.

Wizard MUST add a "UI Testing Milestone" containing tasks:
- Generate UI test Docker service (`ui-docker`)
- Generate test runner script (`ui-runner`)
- Generate example test suite (`ui-tests`)
- Integrate UI tests into CI config (`ui-ci`)
- Add `run-ui-tests` command

Wizard now automatically inserts UI testing into Plans.

---

## GUI Generation Milestone

The wizard MUST add a new milestone at the end of the plan:

- PySide6 Desktop GUI
- Kotlin Mobile GUI
- Next.js Web GUI

The wizard uses:
- `.cursor/rules/create-gui-desktop-pyside6.mdc`
- `.cursor/rules/create-gui-mobile-kotlin.mdc`
- `.cursor/rules/create-gui-web-next.mdc`

Each GUI is treated as a separate task with a dedicated agent.

The GUI milestone is added by default unless the user opts-out by including `--no-gui` in the description.

---

## SSL & HTTPS Setup Milestone

The wizard MUST add a new milestone for SSL/HTTPS setup if:
- `domain`, `email`, `https`, or `ssl` keywords are detected
- OR the project description indicates production deployment

The SSL milestone contains:
- Issue: "Configure Nginx SSL"
  - Task: "Generate SSL Nginx config" (type: `nginx`, priority: 1)
  - Task: "Generate Diffie-Hellman parameters script" (type: `ssl`, priority: 2)
  - Task: "Generate certbot initialization script" (type: `certbot`, priority: 3)
  - Task: "Add certbot service to docker-compose" (type: `docker`, priority: 4)
  - Task: "Generate SSL renewal script" (type: `ssl`, priority: 5)

SSL tasks must run sequentially (not parallel-safe).

---

## Infrastructure Milestone (Docker + SSL)

The wizard MUST add an `Infrastructure: Docker & SSL` milestone that:

- Creates a base Docker stack (API, DB, Redis, Mail, Nginx).
- Adds Nginx reverse proxy.
- Configures SSL with Let's Encrypt:
  - Nginx HTTP→HTTPS redirect
  - ACME challenge location
  - certbot service in docker-compose
  - dhparam script
  - initial certificate acquisition script
  - renewal script

This milestone generates tasks of type `docker`, which will be executed by Docker-related agents.

**Priority Boost**: If the user description includes `https`, `ssl`, `letsencrypt`, `domain`, `nginx`, the priority of this milestone is raised.

The Infrastructure milestone structure includes:
- Issue: "Base Docker Compose Setup" (docker-compose.yml generation)
- Issue: "Nginx SSL & HTTPS" (SSL configuration and scripts)
- Issue: "Nginx SSL Config Editor Integration" (optional GUI integration)
