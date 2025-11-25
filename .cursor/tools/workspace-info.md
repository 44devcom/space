# Workspace Info

Displays the fully resolved SPACE workspace context.  
This includes:

- **workspace.json** fields  
- **state.json** fields  
- **merged environment** variables  
- **loaded tool manifest**  
- **active runtime information** from the Workspace Engine

The output is emitted as formatted JSON and can be piped or consumed by other agents.

Internally, this tool triggers the event:
`onWorkspaceInfo`

which allows listener agents to react to workspace inspections.

## Usage

```
/workspace-info
```

Runs the `workspace-info-runner.sh` script and prints the runtime context.

## Optional Filters

You may filter output using environment variables:

| Variable | Meaning |
|----------|---------|
| `SPACE_INFO_SECTION=workspace` | Print only workspace section |
| `SPACE_INFO_SECTION=state` | Print only state section |
| `SPACE_INFO_SECTION=env` | Print only environment |
| `SPACE_INFO_SECTION=tools` | Print only tools |
| *unset* | Print full context |

Example:

```
SPACE_INFO_SECTION=workspace /workspace-info
```
