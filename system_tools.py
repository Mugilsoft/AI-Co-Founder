"""
system_tools.py — Local system access for the Mugil AI Co-Founder Agent.

Every function here is a *capability*, not an unconditional action: the agent's
GovernanceGateChecker should classify the intended action (e.g. "delete file X",
"run script Y") into Tier 1/2/3 BEFORE calling into this module, exactly as it
already does for other high-risk actions (recruitment, DB deletion, etc.).

This module intentionally does not import your governance module, to avoid a
circular import — wire the check in the agent layer that calls these functions.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

# Restrict all file operations to this root, so the agent can never touch
# anything outside the project/workspace by accident (or by a bad prompt).
WORKSPACE_ROOT = Path(__file__).resolve().parent

# Commands the agent is allowed to run at all. Extend deliberately — every
# addition here is a Tier decision, not just a code change.
ALLOWED_COMMANDS = {"git", "pytest", "python", "pip"}


class SystemToolError(Exception):
    pass


def _resolve_safe(path: str) -> Path:
    """Resolve a path and ensure it stays inside WORKSPACE_ROOT."""
    target = (WORKSPACE_ROOT / path).resolve()
    if WORKSPACE_ROOT not in target.parents and target != WORKSPACE_ROOT:
        raise SystemToolError(f"Path '{path}' escapes the workspace root — refused.")
    return target


def list_directory(path: str = ".") -> list[str]:
    """List files and folders under path, relative to the workspace root."""
    target = _resolve_safe(path)
    if not target.exists():
        raise SystemToolError(f"'{path}' does not exist.")
    return sorted(p.name for p in target.iterdir())


def read_file(path: str, max_bytes: int = 200_000) -> str:
    """Read a text file's contents. Refuses files above max_bytes."""
    target = _resolve_safe(path)
    if not target.is_file():
        raise SystemToolError(f"'{path}' is not a file.")
    if target.stat().st_size > max_bytes:
        raise SystemToolError(f"'{path}' exceeds the {max_bytes}-byte read limit.")
    return target.read_text(encoding="utf-8", errors="replace")


def write_file(path: str, content: str, overwrite: bool = False) -> str:
    """Write content to a file. Refuses to overwrite existing files unless told to.

    Governance note: any write is at minimum a Tier 2 action; overwriting an
    existing file should be treated as Tier 3 in your gate checker.
    """
    target = _resolve_safe(path)
    if target.exists() and not overwrite:
        raise SystemToolError(f"'{path}' already exists — pass overwrite=True to replace it.")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} characters to {path}"


def delete_path(path: str) -> str:
    """Delete a file or directory. Always a Tier 3 action — irreversible."""
    target = _resolve_safe(path)
    if not target.exists():
        raise SystemToolError(f"'{path}' does not exist.")
    if target.is_dir():
        shutil.rmtree(target)
    else:
        target.unlink()
    return f"Deleted {path}"


def run_command(command: list[str], timeout: int = 30) -> dict:
    """Run a whitelisted command inside the workspace and capture output.

    Only the executables in ALLOWED_COMMANDS may be run, and the process is
    always launched with the workspace root as its working directory.
    """
    if not command or command[0] not in ALLOWED_COMMANDS:
        raise SystemToolError(
            f"'{command[0] if command else ''}' is not in ALLOWED_COMMANDS."
        )
    result = subprocess.run(
        command,
        cwd=WORKSPACE_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


if __name__ == "__main__":
    print("Workspace root:", WORKSPACE_ROOT)
    print("Contents:", list_directory("."))
