---
name: generate-orm
description: "Generate a complete Laravel + Python ORM ecosystem from JSON schemas."
stdin: true
inputSchema:
  type: object
  properties:
    laravel:
      type: boolean
      default: true
    python:
      type: boolean
      default: true
    fastapi:
      type: boolean
      default: true
    alembic:
      type: boolean
      default: true
    factories:
      type: boolean
      default: true
    seeders:
      type: boolean
      default: true
---

# generate-orm Agent  
Full ORM Generation for Laravel + Python

This agent analyzes:

- `schemas/models/*.json`
- `schemas/relations/relations.json`

and generates full ORMs, migrations, factories, and more for **both ecosystems**.

---

# STEP 1 — Load and Validate Schemas

- Validate models using: `rules/models.schema.json`
- Validate relations using: `rules/relations.schema.json`
- Load all models + relations into a unified graph

If invalid → return detailed error list.

---

# STEP 2 — Build Unified Schema Graph

Extract:

- Fields
- JSON → Language type mapping
- Required fields
- Enum detection
- Primary key (x-primary-key)
- Unique keys (x-unique)
- Indexes (x-index)
- Defaults
- Relations:
  - one-to-one
  - one-to-many
  - many-to-one
  - many-to-many (auto-build pivot tables)
  - polymorphic
  - self-relations

---

# STEP 3 — LARAVEL GENERATION (if enabled)

### Directory:
```
generated/laravel/
    app/Models/
    database/migrations/
    database/factories/
    database/seeders/
```

## Eloquent Models
- namespace App\Models
- Fillable fields
- Casts array
- Relationships (hasMany, belongsTo, hasOne, belongsToMany)
- SoftDeletes if flagged (`x-soft-delete`)

## Migrations
For each model:

- `create_<table>_table.php`  
- Fields mapped to column types:
  - string → `$table->string()`
  - integer → `$table->integer()`
  - boolean → `$table->boolean()`
  - array → `$table->json()`
- PK, indexes, unique, nullable, default
- Foreign keys + cascade rules

## Factories
Using Faker:

```
return [
  'email' => $this->faker->email(),
  'age' => $this->faker->numberBetween(18, 65),
];
```

Relation-aware factories:

```
'user_id' => User::factory(),
```

## Seeders
Per-model seeder:

```
UserSeeder.php
```

DatabaseSeeder integration:

```
$this->call(UserSeeder::class);
```

---

# STEP 4 — PYTHON GENERATION (if enabled)

### Directory:
```
generated/python/
    sqlalchemy/
    pydantic/
    routers/
    alembic/
    factories/
    seeders/
```

## SQLAlchemy ORM Models
- Declarative Base
- Typed Columns
- Relationships
- Pivot tables auto-built

## Pydantic Models
- Pydantic v2 BaseModel
- camelCase → snake_case alias aliaser
- Enums converted to `Enum` classes
- Default values inferred

## FastAPI Routers
CRUD endpoints:

```
GET /users
GET /users/{id}
POST /u
