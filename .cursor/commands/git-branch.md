# Branch

Creates a new branch following SPACE naming conventions.

## Behavior
- If a branch name is provided, use it.
- If not provided, auto-generate one based on:
    - Current task name (if active)
    - Or folder name + timestamp
- Enforces naming rules:
    feature/<name>
    fix/<name>
    docs/<name>
    chore/<name>

## Usage
/git-branch <branch-name?>

## Instructions
1. If <branch-name> provided:
   - Normalize:
     Replace spaces → "-", lowercase, remove invalid chars.
   - If it doesn't start with a type ("feature/", etc.), default to:
       feature/<normalized-name>

2. If <branch-name> missing:
   - If an active task exists:
       feature/<task-title-slug>
   - Else:
       feature/auto-<timestamp>

3. Create and switch to branch:
   git checkout -b <branch>

4. Confirm branch creation:
   git branch --show-current
