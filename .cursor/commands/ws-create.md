# Workspace Create

Creates a new portable workspace for the project.

## Behavior
- Generates a workspace definition file:
    .space/workspace.json
- Detects platform (Linux, macOS, Windows).
- Creates a clean environment with:
    - tools
    - env vars
    - paths
    - recommended structure
- Links workspace to current Git branch.

## Usage
/ws-create <name?>

## Instructions
1. Determine <name>:
   - Provided by user, or
   - Derived from current folder name.

2. Create directory:
   .space/

3. Write file workspace.json:
   {
     "name": "<name>",
     "branch": "<current-branch>",
     "created": "<timestamp>",
     "dependencies": [],
     "env": {},
     "tools": []
   }

4. Confirm workspace created:
   "Workspace <name> successfully created."
