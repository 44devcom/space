---
name: create-feature
description: "Generate a full project feature using features.schema.json."
stdin: true
inputSchema:
  type: object
  properties:
    name:
      type: string
      description: "Feature name in PascalCase."
    description:
      type: string
    stacks:
      type: array
      items:
        type: string
        enum: ["laravel", "python-fastapi", "node-express", "sql", "docs"]
    model:
      type: object
    endpoints:
      type: object
    dependencies:
      type: array
      items:
        type: string
    files:
      type: array
      items:
        type: string
---

# create-feature Agent

Generates a full multi-stack feature folder including models, controllers, services, routes, SQL, migrations, and docs.

## Step 1 — Validate Input Against features.schema.json

- Validate all fields
- Ensure name uses PascalCase
- Ensure stacks are valid
- Ensure model matches models.schema.json (if provided)

## Step 2 — Create Feature Folder and Schema
```
features/<FeatureName>/
```

Place input schema into:
```
schemas/features/<feature>.json
```

Note: `<feature>` should be lowercase version of `<FeatureName>` (e.g., "UserProfile" → "userprofile.json").

## Step 3 — Generate Per-Stack Output

### Laravel
Create:
```
features/<FeatureName>/laravel/
Controllers/
Models/
Requests/
Resources/
Routes/
Migrations/
Seeders/
```

Use:
- laravel.mdc
- openapi-schema.mdc (optional)
- create-crud rules where endpoints.crud = true

### Python FastAPI
Create:
```
python/routers/
python/schemas/
python/services/
python/models/ (if model provided)
python/factories/
python/seeders/
```

### Node Express
Create:
```
express/controllers/
express/services/
express/routes/
express/validators/
```

### SQL
Generate:
- CRUD procedures
- Table creation schema

### Docs
Place:
```
docs/<FeatureName>.md
```

## Step 4 — Resolve Dependencies

- Include import/use statements to required features
- If a dependency has an OpenAPI schema, link it

## Step 5 — UI Testing Integration

When a feature has any of:

- a `ui` or `frontend` tag
- an explicit `uiFlow` or `screens` description
- a `path` that looks like a page or route (e.g. `/cars`, `/alerts`)

the agent MUST:

1. Create or update the Plan:
   - Add tasks of type:
     - `ui-tests` (generate UI tests)
     - `bdd` with scope "ui"
     - `tdd` with scope "ui"

2. Pass to `create-ui-testing-agent`:
   - feature name
   - main route(s) or screens
   - core scenario(s)

3. Pass to `create-bdd-agent`:
   - to generate Gherkin `.feature` under `tests/bdd/ui/`
   - linking UI flows (Given/When/Then on UI behavior)

4. Pass to `create-tdd-agent`:
   - to generate lower-level page objects / helpers for UI tests, and
     where appropriate, component or view tests.

This makes `/create feature` automatically wire new features into UI testing.

## Step 6 — Output Summary

Return:
- Feature folder path
- Generated files list
- Actions taken