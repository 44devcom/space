---
name: create-openapi-schema
description: "Generate OpenAPI 3.1 specification from JSON models and relations."
stdin: true
inputSchema:
  type: object
  properties:
    title:
      type: string
      default: "API"
    version:
      type: string
      default: "1.0.0"
    format:
      type: string
      enum: ["json", "yaml"]
      default: "json"
---

# create-openapi-schema Agent

Generates a full OpenAPI 3.1 specification using the project's schema system.

---

# Step 1 — Load Schemas

- Load all `schemas/models/*.json`
- Load all `schemas/relations/*.json` (each file contains a single relation)
- Validate using model + relation rules

---

# Step 2 — Build OpenAPI Components

- Convert JSON Schema → OpenAPI schema
- Use `$ref` for nested models
- Build relations as:
  - object references
  - arrays of references for one-to-many
- Handle enums, arrays, objects, defaults

---

# Step 3 — Generate Paths

For each model, create CRUD endpoints:

- `GET /models`
- `GET /models/{id}`
- `POST /models`
- `PUT /models/{id}`
- `DELETE /models/{id}`

Use Pydantic/Laravel DTO inference

---

# Step 4 — Produce Output

Write:

- `schemas/openapi/openapi.json`

or

- `schemas/openapi/openapi.yaml`

---

# Step 5 — Return Summary

- Number of models processed
- Number of relations applied
- Path to created OpenAPI file
