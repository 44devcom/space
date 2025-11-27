---
globs:
  - "schemas/models/*.json"
  - "schemas/relations/*.json"
alwaysApply: false
description: "Generate full ORM structures for Laravel and Python ecosystems using JSON models + relations."
---

# Generate ORM (Laravel + Python)

This command generates BOTH Laravel and Python ORM ecosystems based entirely on your JSON schemas.

Outputs include:

## ✔ Laravel Output
Generated into `generated/laravel/`:

- Eloquent Models (`app/Models/*.php`)
- Migrations (`database/migrations/*.php`)
- Factories (`database/factories/*Factory.php`)
- Seeders (`database/seeders/*Seeder.php`)
- (optional) Policies (`app/Policies/*.php`)
- (optional) Form Requests (`app/Http/Requests/*.php`)

## ✔ Python Output
Generated into `generated/python/`:

- SQLAlchemy ORM Models (`sqlalchemy/*.py`)
- Pydantic v2 Models (`pydantic/*.py`)
- FastAPI Routers (`routers/*.py`)
- Alembic Migration Stubs (`alembic/versions/*.py`)
- FactoryBoy Factories (`factories/*.py`)
- Seeder Scripts (`seeders/*.py`)

## ✔ SQL Output
- `generated/sql/schema.sql`

---

# Features

### ### Laravel:
- Automatic PHP types inferred from JSON types
- FK relations mapped to Eloquent relationships
- Migrations include:
  - PK, unique, indexes, nullable, default
  - foreign keys with cascade rules
- Factories use:
  - Faker
  - Relationship-aware factories
- Seeders:
  - Per-model seeders
  - DatabaseSeeder integration

### ### Python:
- SQLAlchemy uses Declarative Base
- Relationships from relation graph
- Many-to-many pivot tables
- Pydantic:
  - camelCase → snake_case aliasing
  - enums generated automatically
- FastAPI router CRUD scaffold
- Alembic migration template per model
- FactoryBoy:
  - relational factory support
- Seeder:
  - sample data loaders per model

---

# Run

```
cursor-agent run generate-orm
```

---
