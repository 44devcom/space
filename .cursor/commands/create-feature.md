---
globs:
  - "schemas/features/*.json"
  - "schemas/models/*.json"
description: "Create a new feature using features.schema.json and project conventions."
alwaysApply: false
---

# Create Feature

Generates a new feature folder and all associated boilerplate across selected stacks (Laravel, FastAPI, Express, SQL, Docs).

This command uses:
- `features.schema.json`
- `models.schema.json`
- project `.mdc` rules

## Parameters

- `name`: Feature name in PascalCase (e.g., UserAuth, TaskManagement)
- `description`: Optional description of the feature
- `stacks`: Array of stacks to generate (`laravel`, `python-fastapi`, `node-express`, `sql`, `docs`)
- `model`: Optional model structure
- `endpoints`: CRUD or custom endpoints
- `dependencies`: List of feature dependencies

## Output Structure
```
schemas/features/<feature>.json
features/<FeatureName>/
laravel/...
python/...
express/...
sql/...
docs/...
```

## Example Usage
```
/create-feature UserProfile
```

Or with more detail:

```json
{
  "name": "UserProfile",
  "stacks": ["laravel", "python-fastapi"],
  "model": {
    "title": "Profile",
    "properties": { "bio": { "type": "string" } }
  },
  "endpoints": { "crud": true }
}
```