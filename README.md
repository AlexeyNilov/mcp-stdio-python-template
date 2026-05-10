# mcp-stdio-python-template

Minimal Python template for stdio-based MCP servers.

## What it includes

- A `src/` package layout.
- A console script entry point: `mcp-stdio-python-template`.
- A FastMCP server factory in `mcp_stdio_python_template.server`.
- One demo MCP tool named `status` that returns `ok`.
- Pytest, Ruff, and mypy configuration.

## Setup

* Create new Git repo
* Copy content of https://github.com/AlexeyNilov/mcp-stdio-python-template to the new repo
* Commit
* Rename from mcp-stdio-python-template to new repo name
* Create venv
* Install python -m pip install -e ".[dev]"

## Add to Codex

Add a stdio MCP server entry to your Codex config file:

```toml
[mcp_servers.mcp_stdio_python_template]
command = "C:\\an\\git\\mcp-stdio-python-template\\.venv\\Scripts\\python.exe"
args = ["-m", "mcp_stdio_python_template"]
cwd = "C:\\an\\git\\mcp-stdio-python-template"
```

Restart Codex after changing the config. The server exposes one tool:

```text
status -> ok
```

## Development checks

```powershell
.\.venv\Scripts\pytest.exe
.\.venv\Scripts\ruff.exe format --check .
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\mypy.exe
```
