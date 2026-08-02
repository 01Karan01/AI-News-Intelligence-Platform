const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const rootDir = __dirname;
const venvPython = path.join(rootDir, "backend", ".venv", "Scripts", "python.exe");
const pythonCmd = fs.existsSync(venvPython) ? venvPython : "python";
const isWin = process.platform === "win32";

console.log("\x1b[36m[NewsLens AI]\x1b[0m Starting Backend API on http://127.0.0.1:8000 ...");
const backend = spawn(pythonCmd, ["-m", "uvicorn", "backend.api:app", "--host", "127.0.0.1", "--port", "8000"], {
  cwd: rootDir,
  stdio: "inherit",
  shell: isWin,
});

console.log("\x1b[36m[NewsLens AI]\x1b[0m Starting Frontend Server on http://localhost:5173 ...");
const frontend = spawn(isWin ? "npm.cmd" : "npm", ["--prefix", "frontend", "run", "dev"], {
  cwd: rootDir,
  stdio: "inherit",
  shell: isWin,
});

const shutdown = () => {
  try {
    if (backend && !backend.killed) backend.kill();
  } catch (e) {}
  try {
    if (frontend && !frontend.killed) frontend.kill();
  } catch (e) {}
  process.exit(0);
};

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
