globs:

"schemas/models/*.json"

"schemas/relations/*.json" description: "Generate OpenAPI 3.1 schema from project models and relations." alwaysApply: false

# Create OpenAPI Schema

Creates openapi.json or openapi.yaml by merging all model schemas and relations.

## Parameters

- format: "json" or "yaml" (default: json)
- title: API title
- version: semantic version string

## Output

- schemas/openapi/openapi.json or .yaml
- Components based on your model + relation schema