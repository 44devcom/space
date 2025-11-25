#!/usr/bin/env node

/**
 * SPACE Cursor Agent Runtime
 *
 * Final merged version:
 * - Original minimal runtime
 * - Workspace Engine v1 integration
 * - Agent Event Bus v1
 * - Load .cursor/ecosystem.json
 * - Load .cursor/agents/*.json
 * - Load / update .cursor/state.json
 * - Dependency resolution
 * - Execute agent scripts (agent.runs)
 * - Inject workspace context into execution environment
 * - Provide /workspace-info
 */

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

// Workspace Engine v1
const workspaceEngine = require("./.cursor/workspace-engine.js");
// Event Bus v1
const eventBus = require("./.cursor/event-bus.js");

// Paths
const ECOSYSTEM_PATH = path.resolve(".cursor", "ecosystem.json");
const AGENTS_DIR = path.resolve(".cursor", "agents");
const STATE_PATH = path.resolve(".cursor", "state.json");

// -----------------------------------------
// Helpers
// -----------------------------------------

function fileExists(p) {
  try {
    fs.accessSync(p, fs.constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

function loadJson(p, fallback = null) {
  if (!fileExists(p)) {
    if (fallback !== null) return fallback;
    throw new Error(`Missing JSON file: ${p}`);
  }
  const raw = fs.readFileSync(p, "utf8");
  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new Error(`Failed to parse JSON file: ${p}\n${err.message}`);
  }
}

function saveJson(p, data) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(data, null, 2) + "\n", "utf8");
}

function log(...args) {
  console.log("[cursor-agent]", ...args);
}

function error(...args) {
  console.error("[cursor-agent][ERROR]", ...args);
}

// -----------------------------------------
// Loaders
// -----------------------------------------

function loadEcosystem() {
  return loadJson(ECOSYSTEM_PATH);
}

function loadAgent(name) {
  const filePath = path.resolve(AGENTS_DIR, `${name}.json`);
  return loadJson(filePath);
}

function loadState() {
  return loadJson(STATE_PATH, {
    activeTask: null,
    lastBranch: null,
    lastCommit: null,
    lastWorkspace: null,
    lastRelease: null,
    flags: {
      initialized: false,
      docsInSync: false
    }
  });
}

function saveState(state) {
  saveJson(STATE_PATH, state);
}

// -----------------------------------------
// Workspace Runtime: Inject Context into Scripts
// -----------------------------------------

function buildEnvForAgent(runtimeContext) {
  return {
    ...process.env,

    // Workspace metadata
    SPACE_WORKSPACE_NAME: runtimeContext.workspace.name,
    SPACE_WORKSPACE_BRANCH: runtimeContext.workspace.branch,

    // State metadata
    SPACE_LAST_COMMIT: runtimeContext.state.lastCommit || "",
    SPACE_LAST_RELEASE: runtimeContext.state.lastRelease || "",
    SPACE_ACTIVE_TASK: runtimeContext.state.activeTask || "",

    // Tools
    SPACE_TOOLS: Object.keys(runtimeContext.tools).join(","),

    // Merged env
    ...runtimeContext.env
  };
}

// -----------------------------------------
// Listener Agents via Event Bus
// -----------------------------------------

function runListenerAgentsForEvent(eventName, payload) {
  let ecosystem;
  try {
    ecosystem = loadEcosystem();
  } catch (err) {
    return;
  }

  const agents = ecosystem.agents || [];

  for (const name of agents) {
    let agent;
    try {
      agent = loadAgent(name);
    } catch {
      continue;
    }

    if (!Array.isArray(agent.listens)) continue;
    if (!agent.listens.includes(eventName)) continue;
    if (!agent.runs) continue;

    const scriptPath = path.resolve(agent.runs);
    if (!fileExists(scriptPath)) continue;

    try {
      const runtimeContext = workspaceEngine.buildRuntimeContext();
      const env = {
        ...buildEnvForAgent(runtimeContext),
        SPACE_EVENT_NAME: eventName,
        SPACE_EVENT_PAYLOAD: JSON.stringify(payload || {})
      };

      // Execute listener scripts silently in background
      spawnSync(scriptPath, {
        stdio: "ignore",
        shell: true,
        env
      });
    } catch (err) {
      error(`Listener agent "${agent.name}" failed on event ${eventName}:`, err.message);
    }
  }
}

eventBus.setAgentListenerRunner(runListenerAgentsForEvent);

// -----------------------------------------
// Run an agent
// -----------------------------------------

function runAgent(agentName, options = {}, visited = new Set()) {
  const { withDeps = false } = options;

  // Build runtime context for agents
  const runtimeContext = workspaceEngine.buildRuntimeContext();
  workspaceEngine.applyWorkspaceEnv(runtimeContext);

  if (visited.has(agentName)) return;
  visited.add(agentName);

  const agent = loadAgent(agentName);

  eventBus.emit("onAgentStart", { agent: agent.name });
  log(`Running agent: ${agent.name} v${agent.version}`);

  // Dependencies
  if (withDeps && Array.isArray(agent.dependencies)) {
    for (const dep of agent.dependencies) {
      log(`→ Running dependency: ${dep}`);
      eventBus.emit("onAgentDependencyStart", { agent: agent.name, dependency: dep });
      runAgent(dep, { withDeps }, visited);
      eventBus.emit("onAgentDependencyEnd", { agent: agent.name, dependency: dep });
    }
  }

  // Execute the agent's script
  if (agent.runs) {
    const scriptPath = path.resolve(agent.runs);

    if (!fileExists(scriptPath)) {
      error(`Agent "${agent.name}" has runs="${agent.runs}", but file not found: ${scriptPath}`);
    } else {
      eventBus.emit("onScriptStart", { agent: agent.name, script: scriptPath });
      log(`→ Executing script: ${scriptPath}`);

      const result = spawnSync(scriptPath, {
        stdio: "inherit",
        shell: true,
        env: buildEnvForAgent(runtimeContext)
      });

      eventBus.emit("onScriptEnd", {
        agent: agent.name,
        script: scriptPath,
        status: result.status
      });

      if (result.error) {
        eventBus.emit("onError", {
          agent: agent.name,
          message: result.error.message
        });
        error(`Failed to execute script for agent "${agent.name}":`, result.error.message);
      }
      if (result.status !== 0) {
        eventBus.emit("onError", {
          agent: agent.name,
          status: result.status
        });
        error(`Script for agent "${agent.name}" exited with code ${result.status}`);
      }
    }
  } else {
    log(`No external 'runs' script for agent "${agent.name}".`);
  }

  // Update state
  if (agent.output && agent.output.updatesState && Array.isArray(agent.output.stateKeys)) {
    const state = loadState();

    for (const key of agent.output.stateKeys) {
      const parts = key.split(".");
      let cur = state;

      for (let i = 0; i < parts.length; i++) {
        const part = parts[i];
        const isLast = i === parts.length - 1;

        if (isLast) {
          if (part.includes("initialized") || part.includes("docsInSync")) {
            cur[part] = true;
          } else {
            cur[part] = new Date().toISOString();
          }
        } else {
          if (typeof cur[part] !== "object" || cur[part] === null) {
            cur[part] = {};
          }
          cur = cur[part];
        }
      }
    }

    saveState(state);
    log(`State updated for agent: ${agent.name}`);
    eventBus.emit("onStateUpdate", {
      agent: agent.name,
      stateKeys: agent.output.stateKeys
    });
  }

  eventBus.emit("onAgentEnd", { agent: agent.name });
  log(`Agent "${agent.name}" finished.`);
}

// -----------------------------------------
// CLI
// -----------------------------------------

function printHelp() {
  console.log(`
SPACE Cursor Agent Runtime

Usage:
  node cursor-agent.js list
  node cursor-agent.js run <agent-name> [--with-deps]
  node cursor-agent.js workspace-info

Commands:
  list                 List all agents
  run <agent-name>     Run an agent
  workspace-info       Print resolved workspace context

Examples:
  node cursor-agent.js list
  node cursor-agent.js run init-agent --with-deps
  node cursor-agent.js workspace-info
`);
}

function listAgents() {
  const ecosystem = loadEcosystem();
  const agents = ecosystem.agents || [];

  console.log("Registered agents:");
  for (const name of agents) {
    try {
      const agent = loadAgent(name);
      console.log(` - ${agent.name} v${agent.version} :: ${agent.description}`);
    } catch (err) {
      console.log(` - ${name} (failed to load: ${err.message})`);
    }
  }
}

function workspaceInfo() {
  const ctx = workspaceEngine.buildRuntimeContext();
  eventBus.emit("onWorkspaceContextReady", { workspace: ctx.workspace });
  console.log(JSON.stringify(ctx, null, 2));
}

// -----------------------------------------
// Entry point
// -----------------------------------------

(function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === "help" || cmd === "--help" || cmd === "-h") {
    return printHelp();
  }

  if (cmd === "list") {
    return listAgents();
  }

  if (cmd === "workspace-info") {
    return workspaceInfo();
  }

  if (cmd === "run") {
    const agentName = args[1];
    if (!agentName) {
      error("Missing agent name. Usage: node cursor-agent.js run <agent-name>");
      process.exit(1);
    }

    const withDeps = args.includes("--with-deps");

    try {
      runAgent(agentName, { withDeps });
    } catch (err) {
      eventBus.emit("onError", { agent: agentName, message: err.message });
      error(err.message);
      process.exit(1);
    }
    return;
  }

  error(`Unknown command: ${cmd}`);
  printHelp();
  process.exit(1);
})();