#!/bin/bash
set -e

# Calls into the Workspace Engine to print runtime context
node - <<'EOF'
const engine = require("./.cursor/workspace-engine.js");
const ctx = engine.buildRuntimeContext();
console.log(JSON.stringify(ctx, null, 2));
EOF
