# Environment Switch

Switches between development environments.

## Behavior
- Changes active environment
- Updates environment variables
- Activates/deactivates virtual environments
- Updates shell context and Cursor context
- Loads environment-specific configuration

## Usage
/env-switch <environment>

## Instructions
1. Look for environment:
   .space/env.json OR
   .space/<environment>.json

2. If <environment> is provided:
   - Look for .space/<environment>.json
   - If not found, check .space/env.json and verify name matches

3. Load environment configuration:
   - Read .space/env.json
   - Extract type, path, and settings

4. Switch based on environment type:

   **Python:**
   - Deactivate current environment (if any)
   - Activate: source <path>/bin/activate
   - Update PATH and VIRTUAL_ENV variables
   - Verify: which python should point to <path>/bin/python

   **Node.js:**
   - Switch to directory with node_modules
   - Update NODE_PATH if needed
   - Verify: npm --version works

   **Other types:**
   - Apply type-specific activation steps

5. Update workspace context:
   - Set active environment in workspace.json or state.json
   - Update environment variables in runtime context

6. Print active environment summary:
   Name, type, path, workspace

