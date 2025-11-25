const vscode = require("vscode");
const { spawn } = require("child_process");

function runAgent(agent) {
  const p = spawn("node", ["cursor-agent.js", "run", agent, "--with-deps"], {
    cwd: vscode.workspace.rootPath,
    env: process.env
  });

  p.stdout.on("data", data => vscode.window.showInformationMessage(String(data)));
  p.stderr.on("data", data => vscode.window.showErrorMessage(String(data)));
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("space.init", () => runAgent("init-agent"))
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("space.createTask", () => runAgent("docs-agent"))
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("space.completeTask", () => runAgent("docs-agent"))
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("space.runAgent", async () => {
      const agent = await vscode.window.showInputBox({
        prompt: "Enter agent name:"
      });
      if (agent) runAgent(agent);
    })
  );
}

exports.activate = activate;
exports.deactivate = () => {};
