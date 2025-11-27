# Rollback Command

Shortcut to call rollback-agent.

## Usage

```text
/rollback <environment> [--dry]
```

### Examples

```text
/rollback staging
/rollback production-git --dry
```

## Description

Calls the Rollback Agent to revert a failed deployment:

- **Git**: `git reset --hard HEAD~1` and optionally restart.
- **SSH**: custom `rollback.command`.
- **FTP**: usually prints that rollback is not supported.
