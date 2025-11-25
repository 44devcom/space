# Task Create

Creates a new development task and links it to Git branching and documentation.

## Behavior
- Asks for a task title (or generates one from current context).
- Creates a new entry in tasks/<slug>.md
- Generates:
    - description
    - acceptance criteria
    - related files
    - implementation plan
- Creates a Git branch automatically unless disabled.
- Updates CHANGELOG under "Unreleased → Added: New task: <title>"

## Usage
/task-create <title?>

## Instructions
1. If <title> provided, use it.
2. If missing:
   - Infer from **code diff**, README, or issue templates.
   - Example: "Initialize workspace engine"

3. Create file:
   tasks/<slug>.md

4. Include sections:
   # Task: <title>
   ## Summary
   ## Acceptance Criteria
   ## Implementation Plan
   ## Related Files
   ## Status: open

5. Auto-create branch:
   /git-branch <slug>

6. Update CHANGELOG "Unreleased":
   Added – New task: <title>
