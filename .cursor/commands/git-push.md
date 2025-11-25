# Push

Pushes commits to the remote repository.  
Handles upstream setup automatically if missing.

## Behavior
- Pushes the current branch to origin.
- If no upstream is set, sets upstream automatically.
- If the remote does not exist, instruct to create one.

## Usage
/git-push

## Instructions
1. Check if 'origin' exists:
   git remote -v
   If missing → instruct user: "Add a remote: git remote add origin <url>"

2. Push the current branch:
   git push

3. If Git reports:
   "fatal: The current branch <x> has no upstream branch"
   then run:
   git push --set-upstream origin <current-branch>

4. Confirm success:
   git status should show a clean state.

