---
globs: []
description: "Generate a new model JSON Schema using project conventions and models.schema.json."
---

# Create Schema

Guidelines for creating JSON data model schemas using Cursor AI commands.

**Name:** create-schema  
**Purpose:** Quickly scaffold a new model definition file in `schemas/models/`.

---

# Description

The `create-schema` command generates a new JSON Schema file that follows this project's standards:

- Uses `models.schema.json` validation
- Ensures:
  - `$schema` ref included
  - `title` in PascalCase
  - `properties` in camelCase
  - Infer correct JSON Schema field types
  - Support for typed arrays (`array<string>`)
  - Auto-generate descriptions
  - Add required fields array
  - Follow consistent formatting

---

# Parameters

### `name` (required)
Model name in **PascalCase**:

Examples:
- `User`
- `ProductOrder`
- `BlogPost`
- `InvoiceItem`

### `fields` (optional)
Object of:

```
fieldName: fieldType
```

Rules:
- Field names must be **camelCase**
- Types allowed:
  - `string`
  - `number`
  - `integer`
  - `boolean`
  - `array`
  - `object`
  - Typed arrays: `array<string>`, `array<integer>`, `array<object>`

### `required` (optional)
An array of strings declaring required fields.

### `relations` (optional)
An array of relation objects. Each relation will be saved as a separate file in `schemas/relations/<relationName>.json`.

Each relation object should follow the relations.schema.json structure with fields like:
- `name` (required) - Used as the filename
- `type` (required) - Relation type (one-to-one, one-to-many, etc.)
- `from` (required) - Source model name
- `to` (required) - Target model name
- `localField`, `foreignField`, `onDelete`, `onUpdate`, etc.

---

# Output

A JSON Schema at:

```
schemas/models/<Name>.json
```

If relations are provided, they are saved as individual files:

```
schemas/relations/<relationName>.json
```

Each relation file contains a single relation object with structure:

```json
{
  "$schema": "../.cursor/rules/relations.schema.json",
  "type": "one-to-many",
  "from": "ModelName",
  "to": "OtherModel",
  ...
}
```

with structure:

```json
{
  "$schema": "../rules/models.schema.json",
  "title": "ModelName",
  "type": "object",
  "properties": {
    ...
  },
  "required": []
}
```

Automatically adds:

- Descriptions for each field
- Typed array validation
- Consistent formatting
- Enforced camelCase naming
- Valid JSON Schema

---

# Example Input

```json
{
  "name": "User",
  "fields": {
    "id": "string",
    "email": "string",
    "age": "number",
    "isActive": "boolean",
    "roles": "array<string>"
  },
  "required": ["id", "email"]
}
```

# Example Output (Generated Schema)

```json
{
  "$schema": "../rules/models.schema.json",
  "title": "User",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "The id field."
    },
    "email": {
      "type": "string",
      "description": "The email field."
    },
    "age": {
      "type": "number",
      "description": "The age field."
    },
    "isActive": {
      "type": "boolean",
      "description": "The isActive field."
    },
    "roles": {
      "type": "array",
      "items": { "type": "string" },
      "description": "The roles field."
    }
  },
  "required": ["id", "email"]
}
```

---
