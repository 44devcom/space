# Workspace Engine v1 Specification

The Workspace Engine loads, validates, and applies the workspace configuration
stored in `.cursor/workspace.json`.

## Responsibilities
1. Load `.cursor/workspace.json`.
2. Validate fields:
   - name: string
   - branch: string
   - created: ISO timestamp
   - env: key/value map
   - tools: array of tool names
3. Merge with `.cursor/state.json` to produce final runtime context.
4. Provide resolved context object to agents on execution.
5. Ensure workspace name matches folder name (if mismatch, warn).
6. Ensure branch matches `git branch --show-current`.
7. Provide `.env` setter for runtime environment injection.
8. Resolve tool paths from `.cursor/tools/manifest.json`.
9. Provide module hooks for future expansion.

## Runtime Execution Flow
1. Read workspace.json → validate shape.
2. Read state.json → merge into workspace context.
3. Load tool manifest → map tool capabilities into context.
4. Provide runtimeContext = { workspace, state, tools }.
5. Agents receive runtimeContext as contextual metadata.

## Non-goals (v1)
- No dependency resolution for workspace modules.
- No remote workspace syncing.
- No environment virtualization.

Workspace Engine v2 will add modules, sync, and dynamic environments.
