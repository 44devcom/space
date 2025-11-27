---
globs:
  - "schemas/events/*.json"
alwaysApply: false
description: "Generate event + handler boilerplate for all supported stacks using events.schema.json."
---

# Create Event

Generates a complete multi-stack event + handler structure using:

- `events.schema.json`
- abstract event + handler templates
- stack-specific rules (.mdc files)

## Parameters
- `name`: PascalCase event name (e.g. UserRegistered)
- `feature`: lowercase_feature_name (determines file grouping)
- `payload`: object of typed event fields
- `broadcast`: whether the event is externally published
- `stacks`: list of target stacks (python-fastapi, laravel, node-express, sql)

## Output

Creates:

```
schemas/events/<feature>/<feature>.json (schema copy)
generated/<python|laravel|node|sql>/
  ... (stack-specific files)
```

Stack output example:

```
schemas/events/user/user.json
generated/python/events/
  user_events.py
  user_handlers.py
generated/laravel/
  Events/UserRegistered.php
  Listeners/HandleUserRegistered.php
generated/node/
  user_event_bus.js
  UserRegistered.js
  UserRegisteredHandler.js
generated/sql/
  user_userregistered_trigger.sql
  user_userregistered_table.sql
```

## Example

```json
{
  "name": "UserRegistered",
  "feature": "user",
  "payload": { "userId": "integer", "email": "string" },
  "stacks": ["python-fastapi", "laravel"]
}
```
