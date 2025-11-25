# Workspace Switch

Switches between portable workspaces.

## Behavior
- Changes active workspace.
- Updates environment variables.
- Updates shell context and Cursor context.
- Loads workspace-specific modules and docs.

## Usage
/ws-switch <workspace>

## Instructions
1. Look for workspace:
   .space/<workspace>.json OR  
   .space/workspace.json matching "name"

2. Load workspace configuration:
   - Set env vars
   - Load tools
   - Load dependencies

3. Print active workspace summary:
   Name, branch, env, tools
