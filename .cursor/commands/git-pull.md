# Pull

Always pull before writing a single character of code.  
Ensures a clean and up-to-date working state.

## Behavior
- Fetches latest changes from the remote.
- Fast-forwards local master or feature branches.
- Warns if merge conflicts are likely.

## Usage
/git-pull

## Instructions
1. Start every work session with:
   git pull --rebase

2. If the branch has no remote tracking:
   git branch -u origin/<branch>

3. If a merge conflict is detected:
   - Cursor will pause and notify the user:
     "Resolve conflicts manually or with /git-commit after resolving"

4. After a successful pull:
   Always run tests or open documentation to ensure environment consistency.

