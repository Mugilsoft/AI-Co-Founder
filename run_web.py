import argparse
import os
import secrets
import socket
import subprocess
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import uvicorn
from dotenv import dotenv_values, load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")


def _lan_addresses() -> list[str]:
    addresses: set[str] = set()
    try:
        for result in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            address = result[4][0]
            if not address.startswith("127."):
                addresses.add(address)
    except OSError:
        return []
    return sorted(addresses)


def _ensure_port_available(host: str, port: int) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.bind((host, port))
    except OSError as exc:
        raise RuntimeError(
            f"Cannot start: {host}:{port} is already in use. "
            "An earlier server instance may still be running; stop it or choose another port."
        ) from exc


def _start_ba_agent(project: Path, port: int) -> subprocess.Popen:
    project = project.resolve()
    adk_cli = project / ".venv" / "Scripts" / "adk.exe"
    if not adk_cli.is_file():
        raise FileNotFoundError(f"Could not find the BA Agent ADK executable: {adk_cli}")
    if not (project / "mugil_ba" / "agent.py").is_file():
        raise FileNotFoundError(f"Could not find the BA Agent module in: {project}")

    environment = os.environ.copy()
    environment.update(
        {
            key: value
            for key, value in dotenv_values(project / ".env").items()
            if value is not None
        }
    )
    environment["ADK_DEFAULT_APP_NAME"] = "mugil_ba"
    process = subprocess.Popen(
        [
            str(adk_cli),
            "api_server",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--no-reload",
            str(project),
        ],
        cwd=project,
        env=environment,
    )

    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"BA Agent API exited during startup (exit code {process.returncode}).")
        try:
            with urlopen(f"http://127.0.0.1:{port}/list-apps", timeout=2) as response:
                apps = response.read().decode("utf-8")
                if '"mugil_ba"' in apps:
                    return process
        except (OSError, URLError):
            time.sleep(0.5)

    process.terminate()
    process.wait(timeout=10)
    raise TimeoutError("BA Agent API did not become ready within 60 seconds.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AI Co-Founder shared chat.")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Use 0.0.0.0 to allow devices on your private Wi-Fi to connect.",
    )
    parser.add_argument("--port", default=8000, type=int)
    parser.add_argument(
        "--ba-project",
        type=Path,
        help="Also start Google ADK for the BA Agent from this project directory.",
    )
    parser.add_argument("--ba-port", default=8001, type=int)
    args = parser.parse_args()

    _ensure_port_available(args.host, args.port)
    if args.ba_project:
        _ensure_port_available("127.0.0.1", args.ba_port)

    ba_process = None
    if args.ba_project:
        ba_process = _start_ba_agent(args.ba_project, args.ba_port)
        print(f"Business Analyst agent API is ready at http://127.0.0.1:{args.ba_port}", flush=True)
        os.environ["BA_AGENT_API_URL"] = f"http://127.0.0.1:{args.ba_port}"

    configured_code = os.environ.get("COFOUNDER_CHAT_PASSWORD")
    if configured_code:
        print("Using the COFOUNDER_CHAT_PASSWORD value from your environment or .env file.", flush=True)
    else:
        configured_code = secrets.token_urlsafe(18)
        os.environ["COFOUNDER_CHAT_PASSWORD"] = configured_code
        print(f"Temporary chat access code (keep it private): {configured_code}", flush=True)

    print(f"On this PC: http://127.0.0.1:{args.port}", flush=True)
    if args.host == "0.0.0.0":
        for address in _lan_addresses():
            print(f"On your private Wi-Fi: http://{address}:{args.port}", flush=True)
        print("Use the same access code on your PC and phone. Do not port-forward this server.", flush=True)

    try:
        uvicorn.run("web_app:app", host=args.host, port=args.port)
    finally:
        if ba_process and ba_process.poll() is None:
            ba_process.terminate()
            try:
                ba_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ba_process.kill()
                ba_process.wait()


if __name__ == "__main__":
    main()
