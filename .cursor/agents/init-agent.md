# INIT AGENT

The INIT Agent is the orchestrator of the SPACE ecosystem.  
It initializes a new project, prepares documentation, configures Git, activates workflows, and establishes the agile development loop for Cursor-based automation.

This agent is responsible for turning an empty folder into a fully functioning, workspace-managed, task-driven development environment.

---

## Responsibilities

### 1. Initialize Project Structure
- Create required folders:
  - `.github/workflows/`
  - `tasks/`
  - `.space/`
- Ensure core documentation exists:
  - `README.md`
  - `CHANGELOG.md`
  - `ARCHITECTURE.md`
  - `ROADMAP.md`
  - `INSTALL.md`
- Ensure GitHub workflows exist:
  - `release.yml`
  - `update-changelog.yml`

### 2. Initialize Git Repository
- Run `/git-init` with:
  - Inferred repository name (folder name if missing)
  - Default branch: **master**
- Create the initial commit if the repo has no history.
- Set up remote origin if provided.

### 3. Create Initial Workspace
- Run `/ws-create` using the folder name.
- Generate `.space/workspace.json` with:
  - Project name  
  - Current branch  
  - Timestamp  
  - Initial environment info  

### 4. Register the First Task
- Automatically run:
  ```bash
  /task-create "Initialize project structure"
  ```
- Create:
  - `tasks/initialize-project-structure.md`
- Auto-generate acceptance criteria:
  - Git initialized  
  - Docs created  
  - Workflows present  
  - Workspace created  

### 5. Setup Agile Development Loop
The INIT Agent establishes the Cursor workflow:

1. `/task-create <name>`  
2. Agent scaffolds documentation + branch  
3. Developer writes code  
4. `/task-complete` finalizes task  
5. `/git-commit` + `/git-push`  
6. Workflows handle versioning and releases  

### 6. Verify Documentation Consistency
- Ensure README is the *source of truth*
- Cross-validate:
  - README → matches project purpose  
  - CHANGELOG → up to date under `[Unreleased]`  
  - ROADMAP → aligns with upcoming tasks  
  - ARCHITECTURE → matches existing modules  

### 7. Confirm Automation Readiness
- Validate presence and syntax of:
  - `.github/workflows/release.yml`
  - `.github/workflows/update-changelog.yml`
- Ensure Semantic Versioning is active  
- Prepare the environment for automatic releases via GitHub Actions

---

## Initialization Steps (Executed by the Agent)

1. Create folder structure  
2. Install documentation templates  
3. Initialize Git:
   ```bash
   /git-init
   ```
4. Prepare workspace:
   ```bash
   /ws-create
   ```
5. Register initial task:
   ```bash
   /task-create "Initialize project structure"
   ```
6. Commit everything:
   ```bash
   /git-commit "feat: initialize SPACE ecosystem"
   ```
7. Push (optional, if remote provided):
   ```bash
   /git-push
   ```

---

## Requirements

### The INIT Agent requires:
- Git installed  
- Write access to the project folder  
- Ability to create and modify files  
- Ability to run other Cursor tools:
  - git-init
  - git-commit
  - git-push
  - git-pull
  - git-branch
  - task-create
  - task-complete
  - ws-create
  - ws-switch  

---

## Purpose

The INIT Agent creates a **self-driving repository**:

- Every new task becomes a blueprint
- Every branch represents a development cycle  
- Every commit is structured and meaningful  
- Every push updates the release pipeline  
- Every workspace is reproducible and portable  

This provides fully automated, agile development powered by Cursor.

---

## Output Summary

After running the INIT Agent, the repository will contain:

- A fully initialized Git repository  
- A complete documentation system  
- GitHub release automation  
- A portable workspace definition  
- A task-driven development structure  
- A continuous iteration loop  

The project becomes operational immediately.