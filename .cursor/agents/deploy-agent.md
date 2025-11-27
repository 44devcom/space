# Deploy Agent

## Purpose

Single entrypoint to deploy the application using one of:

- FTP (upload + remote rebuild endpoint)
- Git (git pull + build + restart)
- SSH (rsync/scp + remote build + restart)

The agent:

1. Reads `.cursor/rules/deploy.rules.json`.
2. Resolves the target environment.
3. Loads the corresponding method rules:
   - `.cursor/rules/ftp-deploy.rules.json`
   - `.cursor/rules/git-deploy.rules.json`
   - `.cursor/rules/ssh-deploy.rules.json`
4. Executes the deployment pipeline for that method.
5. Runs a healthcheck.
6. Optionally triggers rollback on failure (via rollback-agent).

---

## Usage

Invoked via command:

```text
/deploy <environment> [--dry] [--rollback-on-fail]
```

### Examples

```text
/deploy staging
/deploy production-git --dry
/deploy production-ftp --rollback-on-fail
```

If `<environment>` is omitted, the agent uses the default from `deploy.rules.json`.

---

## Step 1 — Resolve Environment

1. Load `.cursor/rules/deploy.rules.json`.
2. Determine target environment:
   - from command argument OR
   - from `defaults.environment`.
3. Validate environment key exists.
4. Extract:
   - `method` (ftp / git / ssh)
   - `rulesFile` (path to specific rules JSON)

---

## Step 2 — Load Method-Specific Rules

Depending on method:

- `ftp` → load `ftp-deploy.rules.json`
- `git` → load `git-deploy.rules.json`
- `ssh` → load `ssh-deploy.rules.json`

Validate against their schemas:

- **FTP**: must have `connection`, `remoteRebuild`, `healthcheck`.
- **Git**: must have `connection`, `git`, `serviceRestart`, `healthcheck`.
- **SSH**: must have `connection`, `upload`, `remoteBuild`, `serviceRestart`, `healthcheck`.

If validation fails, stop and report.

---

## Step 3 — Dry Run Mode

If `--dry` is passed:

- DO NOT execute any commands.
- Instead, print a detailed plan:
  - Which method will be used
  - Which server/host
  - Which steps (in order)
  - Which commands would run
  - What healthcheck URL would be used
- Then exit.

---

## Step 4 — Method Pipelines

### 4.1 FTP Deploy Pipeline

Using `ftp-deploy.rules.json`:

1. **Local build**:
   - Run `localBuild[]` commands.

2. **Upload**:
   - FTP connect (host, port, user, pass).
   - Upload files to `remotePath`.
   - Respect `upload.exclude[]`.
   - Optionally `deleteOrphans`.

3. **Remote rebuild endpoint**:
   - Call `remoteRebuild.url` with `remoteRebuild.method`.
   - Include `authHeader` and `payload` if defined.

4. **Healthcheck**:
   - Poll `healthcheck.url`.
   - Verify `expectedStatus`.

If any step fails:

- Mark deployment failed.
- If `--rollback-on-fail`, call rollback-agent (if possible).

### 4.2 Git Deploy Pipeline

Using `git-deploy.rules.json`:

1. **SSH connect** to `host` as `username` with `privateKey`.
2. `cd` into `connection.remotePath`.
3. Run `git.prePull[]` commands (if any).
4. Run `git.pull` (e.g., `git pull origin main`).
5. Run `git.postPull[]` commands:
   - `composer install`
   - `npm install`
   - `npm run build`
6. **Service restart**:
   - Run `serviceRestart.command` (e.g. `systemctl restart app`).
   - Run `serviceRestart.verifyCommand`.
7. **Healthcheck**:
   - HTTP check to `healthcheck.url`.

On failure:

- Mark fail.
- If `--rollback-on-fail`, call rollback-agent (e.g., `git reset --hard HEAD~1`).

### 4.3 SSH Deploy Pipeline

Using `ssh-deploy.rules.json`:

1. **Upload code**:
   - If `upload.method = rsync` → use rsync with excludes.
   - If `upload.method = scp` → use scp.

2. **Remote build**:
   - Run `remoteBuild[]` commands (npm/composer/build).

3. **Service restart**:
   - Run `serviceRestart.command`.
   - Verify with `serviceRestart.verifyCommand`.

4. **Healthcheck**:
   - HTTP check.

On failure:

- If `rollback.enabled = true` and `--rollback-on-fail`:
  - Call rollback-agent with `rollback.command`.

---

## Step 5 — Summary Output

After deployment, print:

- Environment name
- Method used (ftp/git/ssh)
- Status: success/failure
- Healthcheck result

If failed:

- which step
- whether rollback was attempted

---

## Integration with Rollback Agent

On failure and with `--rollback-on-fail`, the Deploy Agent should:

1. Determine rollback strategy:
   - **FTP**: usually no rollback (FTPs rarely have atomic rollbacks).
   - **Git**: rollback via `git reset --hard HEAD~1`.
   - **SSH**: rollback via `rollback.command` from `ssh-deploy.rules.json`.

2. Delegate to rollback-agent with:
   - `environment`
   - `method`
   - `context` (host, path, last commit if known).
