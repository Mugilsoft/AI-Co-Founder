import json
import os
import urllib.error
import urllib.request
from typing import Any


class BAAgentClient:
    """Sends requests to the BA Agent's loopback-only Google ADK API."""

    def __init__(
        self,
        base_url: str | None = None,
        app_name: str = "mugil_ba",
        user_id: str = "cofounder_shared_user",
        session_id: str = "cofounder_shared_chat",
    ):
        self.base_url = (
            base_url
            or os.environ.get("BA_AGENT_API_URL", "http://127.0.0.1:8001")
        ).rstrip("/")
        self.app_name = app_name
        self.user_id = user_id
        self.session_id = session_id

    def ask(self, message: str) -> str:
        session_path = (
            f"/apps/{self.app_name}/users/{self.user_id}/sessions/{self.session_id}"
        )
        try:
            self._request("GET", session_path)
        except RuntimeError as exc:
            if not str(exc).startswith("ADK returned 404"):
                raise
            self._request(
                "POST",
                f"/apps/{self.app_name}/users/{self.user_id}/sessions",
                {"session_id": self.session_id},
            )

        events = self._request(
            "POST",
            "/run",
            {
                "app_name": self.app_name,
                "user_id": self.user_id,
                "session_id": self.session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": message}],
                },
            },
        )
        answer = self._extract_answer(events)
        if not answer:
            raise RuntimeError("BA Agent returned no text response.")
        return answer

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers={"Content-Type": "application/json"} if data else {},
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"ADK returned {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise RuntimeError(
                "BA Agent is not responding on localhost:8001. "
                "Start it with run_web.py --ba-project D:\\BA-Agent-for-Mugil."
            ) from exc

    def _extract_answer(self, events: Any) -> str:
        if not isinstance(events, list):
            raise RuntimeError("BA Agent returned an invalid response.")

        root_agent_text = []
        any_text = []
        for event in events:
            if not isinstance(event, dict):
                continue
            content = event.get("content")
            if not isinstance(content, dict):
                continue
            parts = content.get("parts")
            if not isinstance(parts, list):
                continue
            text = "\n".join(
                part["text"]
                for part in parts
                if isinstance(part, dict) and isinstance(part.get("text"), str)
            ).strip()
            if text:
                any_text.append(text)
                if event.get("author") == "Mugil_BA_Agent":
                    root_agent_text.append(text)
        return (root_agent_text or any_text)[-1] if (root_agent_text or any_text) else ""
