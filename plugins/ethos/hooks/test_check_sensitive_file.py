"""tests for check-sensitive-file.py PostToolUse hook."""

import json
import os
import subprocess
import sys
from typing import Any

import pytest

SCRIPT = os.path.join(os.path.dirname(__file__), "check-sensitive-file.py")


def run_hook(tool_name: str, file_path: str) -> dict[str, Any] | None:
    """Run the hook and return parsed output, or None if no output."""
    input_data = json.dumps({"tool_name": tool_name, "tool_input": {"file_path": file_path}})
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=input_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Hook exited with {result.returncode}: {result.stderr}"
    if not result.stdout.strip():
        return None
    return json.loads(result.stdout)


def has_context(output: dict[str, Any] | None) -> bool:
    if output is None:
        return False
    return "additionalContext" in output.get("hookSpecificOutput", {})


WARN_CASES = [
    # ===== section 1: files that should trigger warnings =====
    # .env variants
    pytest.param("Write", "/app/.env", True, id=".env"),
    pytest.param("Write", "/app/.env.local", True, id=".env.local"),
    pytest.param("Write", "/app/.env.production", True, id=".env.production"),
    pytest.param("Edit", "/app/.env.development", True, id=".env.development"),
    # .envrc (direnv)
    pytest.param("Write", "/app/.envrc", True, id=".envrc"),
    # credential files
    pytest.param("Write", "/app/credentials.json", True, id="credentials.json"),
    pytest.param("Edit", "/home/user/credentials.yaml", True, id="credentials.yaml"),
    pytest.param("Write", "/app/gcp-credentials.json", True, id="gcp-credentials.json"),
    # secret files
    pytest.param("Write", "/app/secrets.yaml", True, id="secrets.yaml"),
    pytest.param("Edit", "/app/secrets.json", True, id="secrets.json"),
    pytest.param("Write", "/etc/myapp/secret.conf", True, id="secret.conf"),
    # key/cert files
    pytest.param("Write", "/app/private.pem", True, id="private.pem"),
    pytest.param("Write", "/etc/ssl/server.pem", True, id="server.pem"),
    pytest.param("Write", "/app/tls.key", True, id="tls.key"),
    pytest.param("Edit", "/etc/nginx/server.key", True, id="server.key"),
    # auth config files
    pytest.param("Write", "/home/user/.netrc", True, id=".netrc"),
    pytest.param("Write", "/home/user/.npmrc", True, id=".npmrc"),

    # ===== section 2: files that should NOT trigger warnings =====
    pytest.param("Write", "/app/README.md", False, id="README.md"),
    pytest.param("Edit", "/app/package.json", False, id="package.json"),
    pytest.param("Write", "/app/server.js", False, id="server.js"),
    pytest.param("Write", "/app/index.html", False, id="index.html"),
    pytest.param("Write", "/app/Dockerfile", False, id="Dockerfile"),
    pytest.param("Edit", "/app/.gitignore", False, id=".gitignore"),
    pytest.param("Write", "/app/config.ts", False, id="config.ts"),
    pytest.param("Write", "/app/docker-compose.yml", False, id="docker-compose.yml"),
    pytest.param("Edit", "/app/tsconfig.json", False, id="tsconfig.json"),
    # .env.example still matches .env. pattern — intentional
    pytest.param("Write", "/app/.env.example", True, id=".env.example"),

    # ===== section 3: only Write and Edit should trigger =====
    pytest.param("Read", "/app/.env", False, id="Read .env"),
    pytest.param("Glob", "/app/.env", False, id="Glob .env"),
    pytest.param("Grep", "/app/.env", False, id="Grep .env"),
]


@pytest.mark.parametrize("tool_name, file_path, should_warn", WARN_CASES)
def test_warns(tool_name: str, file_path: str, should_warn: bool) -> None:
    output = run_hook(tool_name, file_path)
    assert has_context(output) == should_warn


# ===== section 4: warning content validation =====


def test_env_write_warning_mentions_filename_gitignore_chmod() -> None:
    output = run_hook("Write", "/app/.env")
    assert output is not None, "no output for .env write"
    ctx = output["hookSpecificOutput"]["additionalContext"]
    assert ".env" in ctx, f"filename not in: {ctx[:100]}"
    assert "gitignore" in ctx.lower() or "git check-ignore" in ctx, (
        f"gitignore guidance not in: {ctx[:100]}"
    )
    assert "chmod" in ctx or "600" in ctx, f"chmod guidance not in: {ctx[:100]}"


# ===== section 5: malformed input, should not crash =====

MALFORMED_INPUTS = [
    pytest.param("", id="empty stdin"),
    pytest.param("not json", id="invalid json"),
    pytest.param(json.dumps({"tool_name": "Write"}), id="missing tool_input"),
    pytest.param(json.dumps({"tool_name": "Write", "tool_input": {}}), id="missing file_path"),
]


@pytest.mark.parametrize("bad_input", MALFORMED_INPUTS)
def test_malformed_input_does_not_crash(bad_input: str) -> None:
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=bad_input,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
