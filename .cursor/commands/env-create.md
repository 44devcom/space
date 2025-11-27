# Environment Create

Creates a new development environment for the project.

## Behavior
- Detects project type (Python, Node.js, etc.)
- Creates environment-specific configuration
- Sets up virtual environment or equivalent
- Generates environment definition file:
  .space/env.json
- Links environment to current workspace

## Usage
/env-create <name?> <type?>

## Instructions
1. Determine <name>:
   - Provided by user, or
   - Default to "default"

2. Determine <type>:
   - Auto-detect from project files:
     - requirements.txt or pyproject.toml → Python
     - package.json → Node.js
     - Cargo.toml → Rust
     - go.mod → Go
   - Or use provided <type>

3. Create environment based on type:

   **Python:**
   - Create .venv/ directory
   - Run: python -m venv .venv
   - Create .space/env.json with:
     {
       "name": "<name>",
       "type": "python",
       "path": ".venv",
       "created": "<timestamp>",
       "workspace": "<current-workspace>"
     }

   **Node.js:**
   - Create node_modules/ if missing
   - Run: npm install (if package.json exists)
   - Create .space/env.json with:
     {
       "name": "<name>",
       "type": "nodejs",
       "path": ".",
       "created": "<timestamp>",
       "workspace": "<current-workspace>"
     }

   **Other types:**
   - Create appropriate environment structure
   - Document in .space/env.json

4. Activate environment (if applicable):
   - Python: source .venv/bin/activate
   - Node.js: No activation needed

5. Confirm environment created:
   "Environment <name> (<type>) successfully created."

