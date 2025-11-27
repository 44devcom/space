---
name: create-schema-agent
description: "Generate a new model JSON Schema file using models.schema.json and project conventions."
inputSchema:
  type: string
stdin: true
---

# create-schema-agent

## Purpose
Creates a new JSON model schema file that follows:
- models.schema.json rules  
- PascalCase model name  
- camelCase fields  
- Typed arrays (array<string>)  
- Auto-generated descriptions  

---

# Step 1 — Ask for Input

Ask user for:

- `name` (PascalCase)
- `fields` (optional)
- `required` (optional)
- `relations` (optional) - Array of relation objects

Example:

```json
{
  "name": "User",
  "fields": {
    "email": "string",
    "tags": "array<string>"
  },
  "required": ["email"],
  "relations": [
    {
      "name": "userPosts",
      "type": "one-to-many",
      "from": "User",
      "to": "Post",
      "localField": "id",
      "foreignField": "userId"
    }
  ]
}
```

---

# Step 2 — Validate Input

1. Ensure `name` is PascalCase  
2. Ensure all field names are camelCase  
3. Validate field types:
   - string
   - number
   - integer
   - boolean
   - object
   - array
   - array<string>, array<number>, array<integer>, array<boolean>

If invalid → return helpful errors.

---

# Step 3 — Generate Schema

Create file:

```
schemas/models/{{Name}}.json
```

Template with inferred types:

```json
{
  "$schema": "../rules/models.schema.json",
  "title": "{{Name}}",
  "type": "object",
  "properties": {
    {{properties}}
  },
  "required": {{required}}
}
```

Type inference rules:

| Input | Generated |
|-------|-----------|
| string | `"type": "string"` |
| number | `"type": "number"` |
| integer | `"type": "integer"` |
| boolean | `"type": "boolean"` |
| array | `"type": "array"` |
| array<string> | `"items": { "type": "string" }` |
| array<object> | `"items": { "type": "object" }` |

Also add:

```
"description": "The <field> field."
```

---

# Step 4 — Save Schema File

Write to:

```
schemas/models/{{Name}}.json
```

If file exists → warn user.

---

# Step 4b — Save Relations (if provided)

If relations are provided in the input, save each relation as a separate file:

```
schemas/relations/{{relationName}}.json
```

Each relation file should contain:

```json
{
  "$schema": "../.cursor/rules/relations.schema.json",
  "type": "{{type}}",
  "from": "{{from}}",
  "to": "{{to}}",
  ...
}
```

Note: Each relation file contains a **single relation object** (not an array).

If a relation file already exists → warn user.

---

# Step 5 — Output

Return:

- Schema file path  
- Generated schema preview  
- Relation file paths (if any were created)
- Success message  

```
Model schema created: schemas/models/User.json
Relation created: schemas/relations/userPosts.json
```
