# Rollback Agent

## Purpose

Handles rollbacks for git/ssh (FTP usually cannot roll back reliably).

Perform a **safe rollback** after a failed deployment for methods that support it:

- **Git**: reset to previous commit.
- **SSH**: run configured rollback command.
- **FTP**: usually not supported (best-effort only if custom solution exists).

---

## Usage

```text
/rollback <environment> [--dry]
```

`<environment>` corresponds to key in `deploy.rules.json`.

---

## Workflow

1. Load `.cursor/rules/deploy.rules.json`.
2. Resolve environment and its `method` + `rulesFile`.
3. If `--dry`:
   - Print what would be done.
   - Do not execute any commands.
4. Else:
   - Branch based on method.

---

## Git Rollback Behavior

Using `git-deploy.rules.json` and SSH:

1. SSH into server as `username` with `privateKey`.
2. `cd` into `connection.remotePath`.
3. Run rollback command:
   - Default: `git reset --hard HEAD~1`.
4. Optionally restart service and healthcheck.

---

## SSH Rollback Behavior

Using `ssh-deploy.rules.json`:

1. Check if `rollback.enabled = true`.
2. SSH into server.
3. `cd` into `connection.remotePath` if needed.
4. Execute `rollback.command`:
   - Default: `cd {{remotePath}} && git reset --hard HEAD~1`.
5. Optionally restart service and healthcheck.

---

## FTP Rollback Behavior

By default:

- Print: "Rollback not supported for FTP deployments, manual restore required."

You may implement a custom mechanism if you have:

- versioned folders, or
- snapshot system, or
- remote backup endpoint.
