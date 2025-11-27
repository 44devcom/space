# Deploy Command

Single user-facing command.

## Usage

```text
/deploy <environment> [--dry] [--rollback-on-fail]
```

### Examples

```text
/deploy staging
/deploy production-git --dry
/deploy production-ftp --rollback-on-fail
```

## Description

Use the Deploy Agent to deploy the application according to:

- `.cursor/rules/deploy.rules.json`
- Method-specific rules:
  - `.cursor/rules/ftp-deploy.rules.json`
  - `.cursor/rules/git-deploy.rules.json`
  - `.cursor/rules/ssh-deploy.rules.json`

The agent will:

1. Resolve method and rules file for `<environment>`.
2. Perform method-specific steps:
   - **FTP**: local build → FTP upload → remote rebuild endpoint → healthcheck
   - **Git**: SSH → git pull → build → restart → healthcheck
   - **SSH**: rsync/scp → remote build → restart → healthcheck
3. Report success or failure.
4. Optionally trigger rollback via rollback-agent on failure.
