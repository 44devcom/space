# Run Plan Agent (GitHub-style, Parallel Executor)

## Purpose

Execute a GitHub-style project plan stored at:

```text
.cursor/plans/<project-id>.plan.json
```

using:

Project → Milestones → Issues → Tasks → Subtasks

Dependency graph between tasks

Parallel execution where safe

## Supported Flags

```text
/run plan <project-id> [--fast] [--dry] [--continue] [--parallel]
```

- `--parallel` → enable parallel execution using `.cursor/rules/plan.rules.json`
- `--fast` → stop on first failure
- `--dry` → simulate without delegating to agents
- `--continue` → resume from `.cursor/run-state/<project-id>.json`

If `parallel.enabled` is `true` in `plan.rules.json`, the agent may also run in parallel by default (even without `--parallel`), but `--parallel` is an explicit request.

## Core Concepts

### 1. Task Dependency Graph (per milestone)

For each milestone:

1. Gather all `issues[].tasks[]`.
2. Build a DAG:
   - **express**: `task.id`
   - **edges**: `task.dependsOn[]` → `task.id`
3. Detect cycles (if any) and fail early with a clear error.
4. Compute execution layers using topological sort:
   - **Layer 0**: tasks with no dependencies
   - **Layer 1**: tasks whose dependencies are all in previous layers
   - **Layer N**: ...

Tasks in the same layer are potentially parallel.

### 2. Parallel-Safe Types

Read `.cursor/rules/plan.rules.json`:

```json
"parallel": {
  "agentSafety": {
    "schema": true,
    "event": true,
    "mvc-model": true,
    "mvc-view": true,
    "mvc-controller": true,
    "openapi": true,
    "graphql": true,
    "bdd": true,
    "tdd": true,
    "tests": true,
    "ddd": false,
    "crud": false,
    "orm": false,
    "docker": false,
    "docker-test": true,
    "ui-tests": true,
    "ui-runner": true,
    "ui-ci": true,
    "ui-docker": false,
    "gui": true,
    "gui-desktop-pyside6": true,
    "gui-mobile-kotlin": true,
    "gui-web-next": true,
    "ssl": false,
    "nginx": false,
    "certbot": false,
    "custom": false
  }
}
```

**Rule**: If `agentSafety[task.type] === true`, task may be executed in parallel. If `false` or missing → always run sequentially.

## Execution Algorithm (High-Level)

1. Load plan JSON.
2. Validate with `plan.schema.json`.
3. Resolve stack from `project.stack`.
4. Use Worktree Resolver Agent:
   - ensure worktree paths are known
   - optionally run `setup-worktree` for the stack
5. Load run-state if `--continue`.
6. For each milestone:
   - Collect all tasks across issues into a list.
   - Build DAG (expresss = task ids, edges from `dependsOn`).
   - Compute layers (L0, L1, ..., Ln).
   - For each layer L:
     - Split tasks into:
       - `parallelCandidates` (parallel-safe types, not yet completed, no unmet deps)
       - `sequentialTasks` (not parallel-safe or forced sequential)
     - Respect `maxWorkers` from rules.
     - If `--dry`:
       - Print which tasks would run in parallel and which sequentially.
     - Else:
       - Execute:
         1. Run all `parallelCandidates` concurrently, up to `maxWorkers`.
         2. Wait until they all finish (or fail).
         3. Run `sequentialTasks` one-by-one, in order.
   - Record success/failure to run-state.
   - Print per-milestone summary.
7. At the end, print:
   - All completed tasks
   - All failed tasks
   - Recommendation to re-run with `--continue` after fixes

## Task → Agent Mapping

Task types are still dispatched like this:

- `ddd` → create-ddd-agent
- `schema` → create-schema-agent
- `event` → create-event-agent
- `feature` → create-feature-agent
- `crud` → create-crud-agent
- `orm` → create-orm-agent
- `mvc` → create-mvc-agent
- `mvc-model` → create-mvc-model-agent
- `mvc-view` → create-mvc-view-agent
- `mvc-controller` → create-mvc-controller-agent
- `openapi` → create-openapi-schema-agent
- `graphql` → create-graphql-schema-agent
- `docker` → create-docker-agent
- `docker-test` → create-docker-test-agent
- `bdd` → create-bdd-agent
- `tdd` → create-tdd-agent
- `tests` → stack-specific test runner script
- `ui-docker` → create-ui-test-docker-agent
- `ui-tests` → create-ui-testing-agent
- `ui-runner` → create-ui-test-runner-agent
- `ui-ci` → create-ui-ci-agent
- `gui` → create-gui-agent (multi-gui dispatcher)
- `gui-desktop-pyside6` → create-gui-desktop-pyside6-agent
- `gui-mobile-kotlin` → create-gui-mobile-kotlin-agent
- `gui-web-next` → create-gui-web-next-agent
- `ssl` → create-docker-agent (SSL scripts and configuration)
- `nginx` → create-nginx-agent
- `certbot` → create-docker-agent (certbot service)

Each delegate call is independent when run in parallel.

**Note**: SSL, nginx, and certbot tasks are NOT parallel-safe and must run sequentially.

### GUI Task Mapping

| Task Type             | Agent                                   |
|----------------------|-------------------------------------------|
| gui                  | create-gui-agent                          |
| gui-desktop-pyside6  | create-gui-desktop-pyside6-agent          |
| gui-mobile-kotlin    | create-gui-mobile-kotlin-agent            |
| gui-web-next         | create-gui-web-next-agent                 |

All 3 GUI tasks can build in parallel (they are parallel-safe and do not conflict).

## Example Parallel Layer Output (Human-Friendly)

When `--parallel` is used, the agent should print:

```
Milestone: MVC Layer

  Layer 0:
    SEQ:  task-ddd                  (type: ddd, parallelSafe=false)

  Layer 1:
    PAR:  task-schema               (type: schema, parallelSafe=true)
          task-events               (type: event, parallelSafe=true)
          task-openapi              (type: openapi, parallelSafe=true)
          task-graphql              (type: graphql, parallelSafe=true)

  Layer 2:
    PAR:  task-mvc-models           (type: mvc-model, parallelSafe=true)
          task-mvc-controllers      (type: mvc-controller, parallelSafe=true)
          task-mvc-views            (type: mvc-view, parallelSafe=true)
    SEQ:  task-crud                 (type: crud, parallelSafe=false)

  Layer 3:
    SEQ:  task-orm                  (type: orm, parallelSafe=false)

  Layer 4:
    SEQ:  task-docker               (type: docker, parallelSafe=false)
```

## Error Handling in Parallel Mode

If any parallel task fails:

- mark that task as failed in run-state
- if `--fast` → stop entire execution
- else → continue later layers but skip dependent tasks whose `dependsOn` include the failed one

## No-Stop Integration
If .cursor/rules/no-stop.rules.json exists:

- All task executions inherit autoContinue, noStop, autoReplay.
- Multi-layer parallel execution continues until full output is delivered.
- Large tasks (MVC, Docker, CRUD, GraphQL) generate in automatic chunks.
- No "continue?" prompts are allowed.
- No plan stage will pause due to length or safety throttle.

## Dry Run Mode (`--dry` + `--parallel`)

In dry mode, instead of executing:

- Only print:
  - Layers
  - Task → Agent mapping
  - Which tasks would be parallel-safe
  - Which would be sequential
  - Which dependencies exist

No actual agents or filesystem changes.

This is extremely useful to debug the plan before real execution.
