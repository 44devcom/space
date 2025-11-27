---
name: create-crud
description: "Generate CRUD controllers, requests, DTOs, routers, and services from JSON model schemas."
stdin: true
inputSchema:
  type: object
  properties:
    name:
      type: string
      description: "Model name in PascalCase."
    laravel:
      type: boolean
      default: true
    python:
      type: boolean
      default: true
    fastapi:
      type: boolean
      default: true
    express:
      type: boolean
      default: false
    sql:
      type: boolean
      default: false
---

# create-crud Agent

Generates full CRUD layers for Laravel + Python ecosystems from JSON Schema models.

---

# Step 1 — Load and Validate Model

- Load `schemas/models/{{name}}.json`
- Validate using `rules/models.schema.json`
- Extract fields, types, required fields

---

# Step 2 — Generate Laravel CRUD (optional)

Create:

```
generated/laravel/app/Http/Controllers/{{Name}}Controller.php
generated/laravel/app/Http/Requests/{{Name}}StoreRequest.php
generated/laravel/app/Http/Requests/{{Name}}UpdateRequest.php
generated/laravel/app/Http/Resources/{{Name}}Resource.php
generated/laravel/routes/{{name}}.php
```

## Laravel Controller
- index()
- show()
- store()
- update()
- destroy()

## StoreRequest & UpdateRequest
- Validation rules built from:
  - type
  - required
  - enum
  - array/object validation

## Laravel API Resource
Formats output fields based on JSON Schema.

## Laravel Routes
```
Route::apiResource('{{plural}}', {{Name}}Controller::class);
```

---

# Step 3 — Generate Python CRUD (FastAPI)

Create:

```
generated/python/routers/{{model}}_router.py
generated/python/schemas/{{model}}_dto.py
generated/python/services/{{model}}_service.py
```

### Router
- GET list  
- GET by id  
- POST create  
- PUT update  
- DELETE remove  

### Pydantic DTO
- CreateDTO (required fields only)
- UpdateDTO (optional fields)
- ResponseDTO (all fields)

### Service
- find_all()
- find_by_id()
- create()
- update()
- delete()

All type hints inferred from JSON Schema.

---

# Step 4 — Express.js CRUD (optional)

Creates:

```
generated/node/controllers/{{model}}.js
generated/node/services/{{model}}Service.js
generated/node/routes/{{model}}Routes.js
```

Includes express-validator based validation if desired.

---

# Step 5 — SQL CRUD (optional)

Generate:

- `CREATE PROCEDURE create_<table>()`
- `read_<table>()`
- `update_<table>()`
- `delete_<table>()`

Works for PostgreSQL or MySQL.

---

# Step 6 — Summary Output

Return:

- Generated files list
- CRUD summary
- Previews of controller + router + DTO

Example:

```
Laravel CRUD created for User:
  Controllers, Requests, Resource, Routes

Python CRUD created for User:
  Router, DTOs, Service

SQL CRUD optional: false
```

---
