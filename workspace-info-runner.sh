#!/bin/bash
set -e

# Workspace Info Runner
# Prints the fully resolved SPACE runtime context.
# Supports filtering via SPACE_INFO_SECTION.

node - <<'EOF'
const workspace = require("./.cursor/workspace-engine.js");
const eventBus = require("./.cursor/event-bus.js");

const ctx = workspace.buildRuntimeContext();

// Emit workspace-info event for listener agents
eventBus.emit("onWorkspaceInfo", { context: ctx });

// Optional filtering
const filter = process.env.SPACE_INFO_SECTION;

// Standard pretty print
const pretty = (obj) => console.log(JSON.stringify(obj, null, 2));

if (!filter) {
  pretty(ctx);
  return;
}

switch (filter) {
  case "workspace":
    pretty(ctx.workspace);
    break;
  case "state":
    pretty(ctx.state);
    break;
  case "env":
    pretty(ctx.env);
    break;
  case "tools":
    pretty(ctx.tools);
    break;
  default:
    console.error(`[workspace-info] Unknown filter: ${filter}`);
    process.exit(1);
}
EOF
