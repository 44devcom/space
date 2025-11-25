/**
 * SPACE Workspace Engine v1
 *
 * Responsibilities:
 * - Load `.cursor/workspace.json`
 * - Load `.cursor/state.json`
 * - Load `.cursor/tools/manifest.json`
 * - Validate and normalize workspace config
 * - Merge workspace + state + tools into a runtimeContext object
 *
 * Non-goals (v1):
 * - No module dependency resolution
 * - No remote workspace sync
 * - No virtualization/sandbox
 */

const fs = require("fs");
const path = require("path");

const WORKSPACE_PATH = path.resolve(".cursor", "workspace.json");
const STATE_PATH = path.resolve(".cursor", "state.json");
const TOOL_MANIFEST_PATH = path.resolve(".cursor", "tools", "manifest.json");

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
    throw new Error(`[workspace-engine] Missing JSON file: ${p}`);
  }
  const raw = fs.readFileSync(p, "utf8");
  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new Error(`[workspace-engine] Failed to parse JSON: ${p}\n${err.message}`);
  }
}

function saveJson(p, data) {
  const dir = path.dirname(p);
  if (!fileExists(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(p, JSON.stringify(data, null, 2) + "\n", "utf8");
}

function log(...args) {
  console.log("[workspace-engine]", ...args);
}

// ---------- Validation ----------

function validateWorkspace(ws) {
  const errors = [];

  if (!ws || typeof ws !== "object") {
    throw new Error("[workspace-engine] workspace.json must be an object");
  }

  if (typeof ws.name !== "string" || !ws.name.trim()) {
    errors.push("workspace.name must be a non-empty string");
  }

  if (typeof ws.branch !== "string" || !ws.branch.trim()) {
    errors.push("workspace.branch must be a non-empty string");
  }

  if (typeof ws.created !== "string" || !ws.created.trim()) {
    errors.push("workspace.created must be an ISO timestamp string");
  }

  if (ws.env && typeof ws.env !== "object") {
    errors.push("workspace.env must be an object (key/value)");
  }

  if (ws.tools && !Array.isArray(ws.tools)) {
    errors.push("workspace.tools must be an array of tool names");
  }

  if (errors.length > 0) {
    throw new Error("[workspace-engine] Invalid workspace.json:\n- " + errors.join("\n- "));
  }

  return ws;
}

// ---------- Loading ----------

function loadWorkspace() {
  const ws = loadJson(WORKSPACE_PATH, null);
  return validateWorkspace(ws);
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

function loadToolManifest() {
  return loadJson(TOOL_MANIFEST_PATH, { tools: {} });
}

// ---------- Merging / Context ----------

function getGitBranch() {
  try {
    const { execSync } = require("child_process");
    return execSync("git branch --show-current", { encoding: "utf8" }).trim() || null;
  } catch {
    return null;
  }
}

/**
 * Build the runtime context:
 * {
 *   workspace: {...},
 *   state: {...},
 *   tools: {...},      // from manifest
 *   env: {...}         // merged environment for runtime use
 * }
 */
function buildRuntimeContext() {
  const workspace = loadWorkspace();
  const state = loadState();
  const manifest = loadToolManifest();

  // Warn if workspace.name != folder
  const folderName = path.basename(process.cwd());
  if (workspace.name !== folderName) {
    log(
      `Warning: workspace.name="${workspace.name}" does not match current folder "${folderName}".`
    );
  }

  // Warn if workspace.branch != current git branch
  const gitBranch = getGitBranch();
  if (gitBranch && workspace.branch !== gitBranch) {
    log(
      `Warning: workspace.branch="${workspace.branch}" does not match git branch "${gitBranch}".`
    );
  }

  // Normalize env
  const envFromWorkspace = workspace.env || {};
  const mergedEnv = {
    ...process.env,
    ...envFromWorkspace
  };

  const tools = manifest.tools || {};

  const runtimeContext = {
    workspace,
    state,
    tools,
    env: mergedEnv
  };

  return runtimeContext;
}

// ---------- Optional: Apply env to process.env ----------

function applyWorkspaceEnv(context) {
  if (!context || !context.env) return;
  Object.entries(context.env).forEach(([key, value]) => {
    process.env[key] = value;
  });
  log("Applied workspace environment variables to process.env");
}

// ---------- Optional: Helper to update state ----------

function updateState(mutator) {
  const current = loadState();
  const next = mutator({ ...current }) || current;
  saveJson(STATE_PATH, next);
  return next;
}

// ---------- Public API ----------

module.exports = {
  loadWorkspace,
  loadState,
  loadToolManifest,
  buildRuntimeContext,
  applyWorkspaceEnv,
  updateState
};
