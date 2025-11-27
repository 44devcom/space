# Worktree Resolver Agent

## Purpose

Provide a unified service for all agents to:

- Resolve paths using `.cursor/worktrees.json`
- Detect current stack (Laravel / Express / FastAPI / Generic)
- Resolve nested paths (e.g. `tests.bdd`, `api.controllers`)
- Auto-create missing directories
- Expand `$ROOT_WORKTREE_PATH`
- Execute `setup-worktree` commands for the stack
- Validate path safety (prevent accidental writes)
- Provide a canonical project file routing system

This agent becomes the **path router** for:

- DDD generation
- CRUD generation
- ORM mapping
- Event generation
- API generation (GraphQL / OpenAPI / REST)
- Docker generation
- BDD/TDD test generation
- Wizard + Plan execution

---

## API

### resolveStack(input)

Determine stack based on:

- plan.stack
- agent prompt (user mentions: Laravel, Express, FastAPI)
- fallback: `generic`

Outputs:

- `laravel` | `express` | `fastapi` | `generic`

---

### resolvePath(stack, key)

Example keys:

- `entities`
- `api.controllers`
- `tests.bdd`
- `docker.services`

Reads from `.cursor/worktrees.json` and resolves path.

Returns:

- relative path string

---

### resolveAll(stack)

Returns entire worktree object for the given stack.

---

### mkdirIfMissing(path)

Ensures the resolved target directory exists.

---

### expandRootVars(path)

Replaces:

- `$ROOT_WORKTREE_PATH`
- `$STACK`
- `$LANG`

with dynamic values.

---

### runSetup(stack)

Executes all commands in:

```yaml
worktrees[stack]["setup-worktree"]
```

Supports:

- virtualenv
- pip install
- composer install
- npm/yarn install
- cp .env logic

Runs each command in a subprocess-like safe print mode (instructions to user, not execution by Cursor directly).

---

### resolveFile(stack, category, filename)

Utility for agents that need final file paths.

Examples:

- Models (entities)
- Repositories
- GraphQL schema files
- OpenAPI spec files
- ORM models
- Feature tests

---

## Behavior

### 1. Load `.cursor/worktrees.json`

If malformed → throw user-friendly error.

### 2. Resolve stack

Infer from:

- plan
- agent prompt
- input filename or route
- language hints

### 3. Create missing directories

Before returning final path:

```bash
mkdir -p <targetDir>
```

### 4. Print all resolved directories (debug-friendly)

Useful for downstream agents.

---

## Example Call

An agent calling:

```makefile
resolvePath("laravel", "entities")
```

Returns:

```yaml
app/Domain/Entities
```

Then automatically ensures:

```bash
mkdir -p app/Domain/Entities
```

---

## Used By

- create-ddd-agent
- create-crud-agent
- create-orm-agent
- create-openapi-schema-agent
- create-graphql-schema-agent
- create-event-agent
- create-feature-agent
- create-docker-agent
- create-docker-test-agent
- create-bdd-agent
- create-tdd-agent
- create-wizard-agent
- run-plan-agent

This is now **the canonical path resolution layer** for your entire system.
