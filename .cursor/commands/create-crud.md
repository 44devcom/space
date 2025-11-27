---
globs:
  - "schemas/models/*.json"
description: "Generate CRUD layers for Laravel and Python based on model schemas."
alwaysApply: false
---

# Create CRUD

Creates CRUD (Create, Read, Update, Delete) scaffolding automatically for:

- Laravel (controllers, requests, routes, resources)
- Python FastAPI (router, service, Pydantic DTOs)

CRUD generation is fully schema-driven from `schemas/models/*.json`.

---

# Parameters

### `name` (required)
Model name in PascalCase.

### `options` (optional)
- `laravel`: boolean (default: true)
- `python`: boolean (default: true)
- `fastapi`: boolean (default: true)
- `express`: boolean (default: false)
- `sql`: boolean (default: false)

---

# What This Command Generates

## Laravel
- `app/Http/Controllers/<Model>Controller.php`
- `app/Http/Requests/<Model>StoreRequest.php`
- `app/Http/Requests/<Model>UpdateRequest.php`
- `app/Http/Resources/<Model>Resource.php`
- `routes/api.php` CRUD entries

## Python (FastAPI)
- `routers/<model>_router.py`
- `schemas/<model>_dto.py`
- `services/<model>_service.py`

## SQL CRUD (optional)
- Stored procedures (MySQL/PostgreSQL)
- CRUD table script

## Express.js CRUD (optional)
- Controller
- Router
- Service

---

# Example

```
/create-crud User
```

Generates controllers, routes, DTOs, services, etc., for model `User`.

