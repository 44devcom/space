# Wizard No-Stop Extension

## Purpose
Extends create-wizard-agent to include global no-stop rules.

## Implementation

Whenever the Wizard spawns an agent:

- Prepend the global no-stop directive.
- Enforce chunked output using the value from no-stop.rules.json.
- Ensure pipelines continue automatically until completion.

All wizard-generated agents inherit no-stop behavior.
