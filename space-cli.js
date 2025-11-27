#!/usr/bin/env node

/**
 * SPACE CLI
 * A wrapper over cursor-agent.js that provides a clean command interface.
 */

const { spawnSync } = require("child_process");

const AGENT = (name, withDeps = false) => {
  const args = ["cursor-agent.js", "run", name];
  if (withDeps) args.push("--with-deps");
  const result = spawnSync("node", args, { stdio: "inherit" });
  process.exit(result.status ?? 0);
};

const help = () => {
  console.log(`
SPACE CLI

Usage:
  space init
  space task create <title>
  space task complete
  space workspace create <name>
  space workspace switch <name>
  space env create <name?> <type?>
  space env switch <name>
  space build
  space test
  space release

Commands map to agents and tools in the ecosystem.
  `);
};

(async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd) return help();

  switch (cmd) {
    case "init":
      return AGENT("init-agent", true);

    case "task":
      if (args[1] === "create") {
        return spawnSync("node", [
          "cursor-agent.js",
          "run",
          "docs-agent",
          "--with-deps"
        ], { stdio: "inherit" });
      }
      if (args[1] === "complete") {
        return AGENT("docs-agent");
      }
      return help();

    case "workspace":
      if (args[1] === "create")
        return AGENT("workspace-agent");
      if (args[1] === "switch")
        return AGENT("workspace-agent");
      return help();

    case "env":
      if (args[1] === "create")
        return AGENT("env-agent");
      if (args[1] === "switch")
        return AGENT("env-agent");
      return help();

    case "build":
      return AGENT("build-agent");

    case "test":
      return AGENT("test-agent", true);

    case "release":
      return AGENT("release-agent", true);

    default:
      return help();
  }
})();
