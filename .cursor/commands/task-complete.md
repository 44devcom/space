# Task Complete

Marks a task finished and links completion to commit + changelog entry.

## Behavior
- Detects the active task from branch name or tasks directory.
- Appends "Completed" entry to task file.
- Updates CHANGELOG "Unreleased → Changed"
- Generates a final commit for the task.
- Prompts to push or create PR.

## Usage
/task-complete

## Instructions
1. Identify current task:
   - Match branch name → tasks/<slug>.md
   - If not found, fallback to latest modified task file.

2. Append to task file:
   ## Completed
   - Date
   - Summary of work
   - Commit hash

3. Update CHANGELOG:
   Changed – Completed task: <title>

4. Commit all:
   /git-commit "feat: complete task <title>"

5. Recommend pushing:
   /git-push
