import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import web_app
from run_web import _ensure_port_available
from src.ba_agent_client import BAAgentClient


class ServerLauncherTests(unittest.TestCase):
    def test_occupied_port_is_reported_before_starting_another_server(self):
        import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", 0))
            _, port = listener.getsockname()
            listener.listen()
            with self.assertRaisesRegex(RuntimeError, "already in use"):
                _ensure_port_available("127.0.0.1", port)


class BAAgentClientTests(unittest.TestCase):
    def test_ask_creates_reusable_session_and_returns_root_agent_text(self):
        client = BAAgentClient()
        events = [
            {
                "author": "Mugil_BA_Agent",
                "content": {"parts": [{"text": "I can help with requirements."}]},
            }
        ]
        with patch.object(
            client,
            "_request",
            side_effect=[
                RuntimeError("ADK returned 404: session not found"),
                {"id": "cofounder_shared_chat"},
                events,
            ],
        ) as request:
            answer = client.ask("Help define requirements")

        self.assertEqual(answer, "I can help with requirements.")
        self.assertEqual(request.call_count, 3)
        self.assertEqual(request.call_args_list[1].args[0], "POST")
        self.assertEqual(request.call_args_list[2].args[1], "/run")

    def test_ask_reports_adk_errors_instead_of_returning_demo_text(self):
        client = BAAgentClient()
        with patch.object(
            client,
            "_request",
            side_effect=RuntimeError("ADK returned 500: model unavailable"),
        ):
            with self.assertRaisesRegex(RuntimeError, "model unavailable"):
                client.ask("Create acceptance criteria")


class SharedChatTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "chat.sqlite3"
        self.database_patch = patch.object(web_app, "DATABASE_PATH", self.database_path)
        self.database_patch.start()
        self.access_code_patch = patch.dict(os.environ, {"COFOUNDER_CHAT_PASSWORD": "test-access-code"})
        self.access_code_patch.start()
        self.agent_patch = patch.object(
            web_app.agent_router,
            "route_query",
            return_value={
                "agent_role": "Co-Founder & Strategy Orchestrator",
                "response": "A demo answer.",
            },
        )
        self.agent_patch.start()
        self.client = TestClient(web_app.app)
        self.client.__enter__()
        self.headers = {"Authorization": "Bearer test-access-code"}

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.agent_patch.stop()
        self.access_code_patch.stop()
        self.database_patch.stop()
        self.temp_dir.cleanup()

    def test_login_rejects_incorrect_access_code(self):
        response = self.client.post("/api/login", json={"access_code": "wrong"})

        self.assertEqual(response.status_code, 401)

    def test_messages_require_access_code(self):
        response = self.client.get("/api/messages")

        self.assertEqual(response.status_code, 401)

    def test_shared_chat_page_serves_ui_and_assets(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("/static/style.css", response.text)
        self.assertEqual(self.client.get("/static/app.js").status_code, 200)

    def test_chat_persists_user_and_agent_messages_for_shared_devices(self):
        response = self.client.post(
            "/api/messages",
            headers=self.headers,
            json={"message": "How should we start?", "agent_key": "orchestrator"},
        )

        self.assertEqual(response.status_code, 200)
        with TestClient(web_app.app) as other_device:
            messages = other_device.get("/api/messages", headers=self.headers).json()
        self.assertEqual([message["role"] for message in messages], ["user", "assistant"])
        self.assertEqual(messages[0]["content"], "How should we start?")
        self.assertEqual(messages[1]["content"], "A demo answer.")

    def test_unknown_agent_is_rejected(self):
        response = self.client.post(
            "/api/messages",
            headers=self.headers,
            json={"message": "Hello", "agent_key": "not-an-agent"},
        )

        self.assertEqual(response.status_code, 422)

    def test_business_analyst_persona_uses_local_ba_agent(self):
        with patch.object(web_app.ba_agent_client, "ask", return_value="BA response.") as ask:
            response = self.client.post(
                "/api/messages",
                headers=self.headers,
                json={"message": "Create acceptance criteria.", "agent_key": "ba_agent"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["agent_role"], "Business Analyst Agent")
        self.assertEqual(response.json()["response"], "BA response.")
        ask.assert_called_once_with("Create acceptance criteria.")

    def test_business_analyst_failure_is_reported_and_not_saved_as_an_answer(self):
        with patch.object(
            web_app.ba_agent_client,
            "ask",
            side_effect=RuntimeError("ADK returned 500: Internal Server Error"),
        ):
            response = self.client.post(
                "/api/messages",
                headers=self.headers,
                json={"message": "Create acceptance criteria.", "agent_key": "ba_agent"},
            )

        self.assertEqual(response.status_code, 502)
        self.assertIn("ADK returned 500", response.json()["detail"])
        messages = self.client.get("/api/messages", headers=self.headers).json()
        self.assertEqual(messages, [])

    def test_client_can_poll_only_messages_after_last_seen_id(self):
        self.client.post(
            "/api/messages",
            headers=self.headers,
            json={"message": "First message", "agent_key": "orchestrator"},
        )

        response = self.client.get("/api/messages?after_id=2", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


if __name__ == "__main__":
    unittest.main()
