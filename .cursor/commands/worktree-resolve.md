# Worktree Resolve Command

## Usage

```text
/worktree resolve <stack> <key>
```

### Examples

```text
/worktree resolve laravel entities
/worktree resolve express api.controllers
/worktree resolve fastapi tests.bdd
```

## Description

Call the Worktree Resolver Agent to:

- determine path for the given stack and key
- auto-create directories
- expand `$ROOT_WORKTREE_PATH`
- print the final usable path

This helps debugging when creating plans or when writing agents manually.

---

## Configuration

### `.cursor/rules/worktree.rules.json`

```json
{
  "version": 1,
  "worktree": {
    "require_existing_stack": true,
    "require_existing_key": true,
    "auto_mkdir": true,
    "expand_root_env_vars": true,
    "allow_nested_keys": true,
    "fail_on_unsafe_paths": true,
    "log_resolutions": true
  }
}
```
