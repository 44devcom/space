#!/usr/bin/env node

/**
 * SPACE Cursor Agent Runtime
 *
 * Minimal runtime to:
 * - load .cursor/ecosystem.json
 * - load agent definitions from .cursor/agents/
 * - load and update .cursor/state.json
 * - run agents (with optional dependency execution)
 * - execute external scripts defined in agent.runs (e.g. run-init-agent.sh)
 *
 * Usage:
 *   node cursor-agent.js list
 *   node cursor-agent.js run <agent-name> [--with-deps]
 *
 * Examples:
 *   node cursor-agent.js list
 *   node cursor-agent.js run init-agent --with-deps
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ECOSYSTEM_PATH = path.resolve('.cursor', 'ecosystem.json');
const AGENTS_DIR = path.resolve('.cursor', 'agents');
const STATE_PATH = path.resolve('.cursor', 'state.json');

// ---------- Helpers ----------

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
  const raw = fs.readFileSync(p, 'utf8');
  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new Error(`Failed to parse JSON: ${p}\n${err.message}`);
  }
}

function saveJson(p, data) {
  const dir = path.dirname(p);
  if (!fileExists(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(p, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

function log(...args) {
  console.log('[cursor-agent]', ...args);
}

function error(...args) {
  console.error('[cursor-agent][ERROR]', ...args);
}

// ---------- Ecosystem / Agent / State loading ----------

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

// ---------- Core: run an agent ----------

/**
 * Run an agent by name.
 *
 * Options:
 *   - withDeps: if true, run dependencies first (depth-first)
 */
function runAgent(agentName, options = {}, visited = new Set()) {
  const { withDeps = false } = options;

  if (visited.has(agentName)) {
    // prevent cycles
    return;
  }
  visited.add(agentName);

  const agent = loadAgent(agentName);
  log(`Running agent: ${agent.name} v${agent.version}`);

  // 1. Run dependencies (if requested)
  if (withDeps && Array.isArray(agent.dependencies)) {
    for (const dep of agent.dependencies) {
      log(`→ Running dependency: ${dep}`);
      runAgent(dep, { withDeps }, visited);
    }
  }

  // 2. Execute the agent's external "runs" script, if present.
  if (agent.runs) {
    const scriptPath = path.resolve(agent.runs);
    if (!fileExists(scriptPath)) {
      error(`Agent "${agent.name}" has runs="${agent.runs}", but file not found: ${scriptPath}`);
    } else {
      log(`→ Executing script: ${scriptPath}`);
      const result = spawnSync(scriptPath, {
        stdio: 'inherit',
        shell: true
      });

      if (result.error) {
        error(`Failed to execute script for agent "${agent.name}":`, result.error.message);
      }
      if (result.status !== 0) {
        error(`Script for agent "${agent.name}" exited with code ${result.status}`);
      }
    }
  } else {
    log(`No external 'runs' script defined for agent "${agent.name}". Nothing to execute.`);
  }

  // 3. Update .cursor/state.json if agent declares output stateKeys
  if (agent.output && agent.output.updatesState && Array.isArray(agent.output.stateKeys)) {
    const state = loadState();
    for (const key of agent.output.stateKeys) {
      // Support simple dotted paths like "flags.initialized"
      const parts = key.split('.');
      let cur = state;

      for (let i = 0; i < parts.length; i++) {
        const part = parts[i];
        const isLast = i === parts.length - 1;

        if (isLast) {
          // Heuristic: set booleans to true, others to a timestamp
          if (part.startsWith('is') || part === 'initialized' || part === 'docsInSync') {
            cur[part] = true;
          } else if (part === 'lastWorkspace') {
            cur[part] = state.lastWorkspace || (state.lastWorkspace === null ? null : state.lastWorkspace);
          } else if (part === 'lastCommit' || part === 'lastRelease') {
            cur[part] = new Date().toISOString();
          } else {
            cur[part] = true;
          }
        } else {
          if (typeof cur[part] !== 'object' || cur[part] === null) {
            cur[part] = {};
          }
          cur = cur[part];
        }
      }
    }
    saveState(state);
    log('State updated for agent:', agent.name);
  }

  log(`Agent "${agent.name}" finished.`);
}

// ---------- CLI ----------

function printHelp() {
  console.log(`
SPACE Cursor Agent Runtime

Usage:
  node cursor-agent.js list
  node cursor-agent.js run <agent-name> [--with-deps]

Commands:
  list                 List all agents from .cursor/ecosystem.json
  run <agent-name>     Run a specific agent by name

Options:
  --with-deps          Run the agent's dependencies first (depth-first)

Examples:
  node cursor-agent.js list
  node cursor-agent.js run init-agent --with-deps
`);
}

function listAgents() {
  const ecosystem = loadEcosystem();
  const agents = ecosystem.agents || [];
  console.log('Registered agents:');
  for (const name of agents) {
    try {
      const agent = loadAgent(name);
      console.log(` - ${agent.name} v${agent.version} :: ${agent.description}`);
    } catch (err) {
      console.log(` - ${name} (failed to load: ${err.message})`);
    }
  }
}

// Entry point
(function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === 'help' || cmd === '--help' || cmd === '-h') {
    printHelp();
    return;
  }

  if (cmd === 'list') {
    listAgents();
    return;
  }

  if (cmd === 'run') {
    const agentName = args[1];
    if (!agentName) {
      error('Missing agent name. Usage: node cursor-agent.js run <agent-name>');
      process.exit(1);
    }

    const withDeps = args.includes('--with-deps');
    try {
      runAgent(agentName, { withDeps });
    } catch (err) {
      error(err.message);
      process.exit(1);
    }
    return;
  }

  error(`Unknown command: ${cmd}`);
  printHelp();
  process.exit(1);
})();
