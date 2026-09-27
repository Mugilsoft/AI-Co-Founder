import os
import shlex
import subprocess
from dataclasses import dataclass
from typing import Any, Dict

from src.governance_checker import GovernanceGateChecker


@dataclass
class ApprovalRequired(Exception):
    """Raised when an action requires human approval before execution.

    Attributes:
        result: GovernanceResult-like object returned by GovernanceGateChecker.check()
        description: short text describing the pending action
    """
    result: Any
    description: str

    def __str__(self):
        return f"Approval required: {self.description} (tier={getattr(self.result,'tier', '?')})"


_project_root = os.path.abspath(os.path.dirname(__file__))


def _ensure_safe_relative_path(path: str) -> str:
    # Disallow absolute paths and parent-directory escapes for safety in demo mode
    if os.path.isabs(path):
        raise ValueError("Absolute paths are not allowed in demo guarded_actions")
    normalized = os.path.normpath(path)
    if normalized.startswith(".."):
        raise ValueError("Paths outside the project root are not allowed")
    return os.path.join(_project_root, normalized)


def _check_requires_approval(text: str):
    checker = GovernanceGateChecker()
    res = checker.check(text)
    return res


# ----- Guarded operations (demo-friendly) -----

def guarded_send_email(to: str, subject: str, body: str, approved: bool = False) -> Dict[str, Any]:
    """Simulate sending an email. Raises ApprovalRequired if governance tier >= 3 and not approved.

    This demo implementation does NOT send a real email. When `approved=True` it records a
    simulated send and returns a success summary.
    """
    description = f"Send email to {to} subject={subject}"
    res = _check_requires_approval(subject + "\n" + body)
    if res.requires_approval and not approved:
        raise ApprovalRequired(result=res, description=description)

    # Simulate send (no network calls)
    return {"status": "ok", "message": f"(demo) email recorded to {to}", "to": to, "subject": subject}


def guarded_write_file(path: str, content: str, overwrite: bool = False, approved: bool = False) -> str:
    """Write a file under the project root. Raises ApprovalRequired for high-risk content.

    For safety this will only write files relative to the project and will refuse absolute or
    parent-traversing paths.
    """
    description = f"Write file {path} (overwrite={overwrite})"
    res = _check_requires_approval(content)
    if res.requires_approval and not approved:
        raise ApprovalRequired(result=res, description=description)

    dest = _ensure_safe_relative_path(path)
    dirname = os.path.dirname(dest)
    os.makedirs(dirname, exist_ok=True)

    if os.path.exists(dest) and not overwrite and not approved:
        return f"(demo) file exists and overwrite not permitted: {path}"

    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)

    return f"(demo) wrote file: {path}"


def guarded_delete_path(path: str, approved: bool = False) -> str:
    """Simulate deletion. For safety the demo mode does NOT perform destructive deletes unless approved.

    If approved=True and the target is a file inside the project, it will be removed.
    """
    description = f"Delete path {path}"
    res = _check_requires_approval(path)
    if res.requires_approval and not approved:
        raise ApprovalRequired(result=res, description=description)

    dest = _ensure_safe_relative_path(path)
    if not os.path.exists(dest):
        return f"(demo) path does not exist: {path}"

    if not approved:
        return f"(demo) deletion simulated for {path} (approve to actually delete)"

    # approved destructive action: only remove files, not directories
    if os.path.isfile(dest):
        os.remove(dest)
        return f"(demo) file deleted: {path}"
    else:
        return f"(demo) target is not a file; no action taken: {path}"


def guarded_run_command(command, approved: bool = False) -> Dict[str, Any]:
    """Run a shell command securely.

    - If `approved` is False, commands are simulated and not executed (returns a notice).
    - If `approved` is True, the command is executed via subprocess and stdout/stderr returned.

    `command` may be a list (preferred) or a string.
    """
    if isinstance(command, str):
        cmd_list = shlex.split(command)
    else:
        cmd_list = list(command)

    description = " ".join(cmd_list[:6])
    res = _check_requires_approval(" ".join(cmd_list))
    if res.requires_approval and not approved:
        raise ApprovalRequired(result=res, description=f"Run command: {description}")

    if not approved:
        return {"stdout": "", "stderr": "(demo) command not executed — approval required to run.", "returncode": None}

    try:
        proc = subprocess.run(cmd_list, capture_output=True, text=True, cwd=_project_root, timeout=60)
        return {"stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": -1}
