---
name: create-event
description: "Generate event and handler classes for multiple stacks using events.schema.json."
stdin: true

inputSchema:
  type: object
  properties:
    name:
      type: string
    feature:
      type: string
    description:
      type: string
    payload:
      type: object
    broadcast:
      type: boolean
    stacks:
      type: array
      items:
        type: string
      default:
        - "python-fastapi"
---

# create-event Agent

This agent generates a complete event system for the provided stacks.

The agent must follow these rules:

---

## 1. Folder + File Structure Rules

Create base structure:

```
schemas/events/<feature>/<feature>.json (schema copy)
generated/<python|laravel|node|sql>/
  ... (stack-specific files)
```

For each stack, create files in stack-specific subfolders at root level:

- **python**: `generated/python/events/<feature>_events.py`, `generated/python/events/<feature>_handlers.py`
- **laravel**: `generated/laravel/Events/<EventName>.php`, `generated/laravel/Listeners/Handle<EventName>.php`, `generated/laravel/Providers/EventServiceProvider.php` (append)
- **node**: `generated/node/<feature>_event_bus.js`, `generated/node/<EventName>.js`, `generated/node/<EventName>Handler.js`
- **sql**: `generated/sql/<feature>_<event>trigger.sql`, `generated/sql/<feature><event>_table.sql`

For each additional stack, create stack-specific files in their respective `generated/<stack>/` subfolders without overwriting.

---

## 2. Python Rules

Note: Stack identifier "python-fastapi" maps to folder `generated/python/events/`.

### Event file: `generated/python/events/<feature>_events.py` must:
- import AbstractEvent and BaseModel
- generate a Pydantic payload class
- generate a concrete Event class inheriting AbstractEvent
- use type-safe constructor
- expose `name` property

### Handler file: `generated/python/events/<feature>_handlers.py` must:
- import AbstractHandler and AbstractAsyncHandler
- generate a sync handler class
- generate an async handler class
- NOT mix multiple event handlers in one file
- end with an auto-registration stub (commented)

---

## 3. Laravel Rules

If Laravel is included:
Generate in `generated/laravel/`:

```
generated/laravel/Events/<EventName>.php
generated/laravel/Listeners/Handle<EventName>.php
generated/laravel/Providers/EventServiceProvider.php (append)
```

Note: Stack identifier "laravel" maps to folder `generated/laravel/`.

---

## 4. Node/Express Rules

If "node-express" is included:
Generate in `generated/node/`:

```
generated/node/<feature>_event_bus.js
generated/node/<EventName>.js
generated/node/<EventName>Handler.js
```

Note: Stack identifier "node-express" maps to folder `generated/node/`.

---

## 5. SQL Rules

If "sql" is included:
Generate in `generated/sql/`:

```
generated/sql/<feature>_<event>trigger.sql
generated/sql/<feature><event>_table.sql
```

Note: Stack identifier "sql" maps to folder `generated/sql/`.

---

## 6. Summary

Return:
- all generated files
- relative paths
- stack breakdown 