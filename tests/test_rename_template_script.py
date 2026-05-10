from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


def find_usable_bash() -> str | None:
    bash = shutil.which("bash")
    if bash is None:
        return None

    completed = subprocess.run(
        [bash, "-lc", "printf ok"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0 or completed.stdout != "ok":
        return None

    return bash


def test_rename_template_script_updates_project_and_package_names(tmp_path):
    bash = find_usable_bash()
    if bash is None:
        pytest.skip("bash is required to execute the rename script")

    repo = tmp_path / "weather-mcp-server"
    old_package = repo / "src" / "mcp_stdio_python_template"
    old_package.mkdir(parents=True)
    (repo / "tests").mkdir()
    (old_package / "__init__.py").write_text("", encoding="utf-8")
    (old_package / "cli.py").write_text(
        "PACKAGE_NAME = 'mcp-stdio-python-template'\n"
        "from mcp_stdio_python_template.server import build_server\n",
        encoding="utf-8",
    )
    (old_package / "server.py").write_text(
        "FastMCP('mcp-stdio-python-template')\n",
        encoding="utf-8",
    )
    (repo / "tests" / "test_cli.py").write_text(
        "from mcp_stdio_python_template.cli import main\n",
        encoding="utf-8",
    )
    (repo / "pyproject.toml").write_text(
        "[project]\n"
        'name = "mcp-stdio-python-template"\n'
        "\n"
        "[project.scripts]\n"
        'mcp-stdio-python-template = "mcp_stdio_python_template.cli:main"\n',
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        "# mcp-stdio-python-template\n`mcp_stdio_python_template.server`\n",
        encoding="utf-8",
    )

    script = Path(__file__).resolve().parents[1] / "scripts" / "rename-template.sh"
    assert script.exists()

    completed = subprocess.run(
        [bash, str(script), "weather-mcp-server"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert not old_package.exists()
    assert (repo / "src" / "weather_mcp_server").is_dir()
    assert 'name = "weather-mcp-server"' in (repo / "pyproject.toml").read_text(encoding="utf-8")
    assert 'weather-mcp-server = "weather_mcp_server.cli:main"' in (
        repo / "pyproject.toml"
    ).read_text(encoding="utf-8")

    text_files = [
        repo / "README.md",
        repo / "src" / "weather_mcp_server" / "cli.py",
        repo / "src" / "weather_mcp_server" / "server.py",
        repo / "tests" / "test_cli.py",
    ]
    for text_file in text_files:
        content = text_file.read_text(encoding="utf-8")
        assert "weather-mcp-server" in content or "weather_mcp_server" in content
        assert "mcp-stdio-python-template" not in content
        assert "mcp_stdio_python_template" not in content
