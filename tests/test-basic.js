const engine = require("../../.cursor/workspace-engine.js");

console.log("Running Workspace Engine v1 Tests...");

try {
  const ws = engine.loadWorkspace();
  console.log("✓ loadWorkspace(): OK");

  const ctx = engine.buildRuntimeContext();
  if (ctx.workspace && ctx.state && ctx.tools && ctx.env) {
    console.log("✓ buildRuntimeContext(): OK");
  } else {
    console.error("✗ buildRuntimeContext(): Missing fields");
  }

  console.log("✓ Workspace Engine v1 test suite completed");
} catch (err) {
  console.error("✗ ERROR:", err.message);
  process.exit(1);
}
