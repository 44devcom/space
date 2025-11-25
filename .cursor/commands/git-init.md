# Initialize Repository

Initializes a new Git repository following the SPACE development strategy.
Always run this command before creating the first file.

## Behavior
- Creates a new Git repository in the current directory.
- If a repository name is provided, uses it as the directory name.
- If no name is provided, uses the current folder name as the repository name.
- Ensures the default branch is **master** (not main).
- Creates an initial commit if none exists.

## Usage
/git-init <repository?>

## Instructions
1. If <repository> is provided:
   - Create a folder named <repository> and enter it.
2. If not:
   - Use the current directory name as the repository name.
3. Run:
   git init
4. Rename default branch to **master**:
   git branch -M master
5. If the directory contains files, create an initial commit:
   git add .
   git commit -m "Initial commit"
6. If empty, create a README placeholder before committing.

