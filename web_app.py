import hmac
import os
import sqlite3
from contextlib import asynccontextmanager
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.agent_router import AgentRouter
from src.ba_agent_client import BAAgentClient
from src.knowledge_loader import KnowledgeBaseLoader


PROJECT_ROOT = Path(__file__).resolve().parent
WEB_DIR = PROJECT_ROOT / "web"
load_dotenv(PROJECT_ROOT / ".env")
DATABASE_PATH = Path(
    os.environ.get("COFOUNDER_CHAT_DATABASE", PROJECT_ROOT / "memory" / "chat_history.sqlite3")
)

knowledge_base = KnowledgeBaseLoader(root_dir=str(PROJECT_ROOT))
agent_router = AgentRouter(knowledge_base)
ba_agent_client = BAAgentClient()
bearer_scheme = HTTPBearer(auto_error=False)


@contextmanager
def _database_connection():
    connection = sqlite3.connect(DATABASE_PATH, timeout=5)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _database_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                agent_key TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
    yield


app = FastAPI(
    title="AI Co-Founder Shared Chat",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


class LoginRequest(BaseModel):
    access_code: str = Field(min_length=1, max_length=256)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    agent_key: str = Field(default="orchestrator", min_length=1, max_length=40)


def _configured_access_code() -> str:
    return os.environ.get("COFOUNDER_CHAT_PASSWORD", "")


def _require_access_code(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> None:
    access_code = _configured_access_code()
    if not access_code:
        raise HTTPException(status_code=503, detail="The chat server has no access code configured.")
    if credentials is None or not hmac.compare_digest(credentials.credentials, access_code):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing access code.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.post("/api/login")
def login(request: LoginRequest) -> dict[str, str]:
    access_code = _configured_access_code()
    if not access_code:
        raise HTTPException(status_code=503, detail="The chat server has no access code configured.")
    if not hmac.compare_digest(request.access_code, access_code):
        raise HTTPException(status_code=401, detail="Incorrect access code.")
    return {"token": access_code}


@app.get("/api/messages")
def get_messages(
    _: Annotated[None, Depends(_require_access_code)],
    after_id: Annotated[int | None, Query(ge=0)] = None,
) -> list[dict[str, object]]:
    with _database_connection() as connection:
        connection.row_factory = sqlite3.Row
        if after_id is None:
            rows = connection.execute(
                "SELECT id, role, content, agent_key, created_at "
                "FROM messages ORDER BY id DESC LIMIT 100"
            ).fetchall()
            rows.reverse()
        else:
            rows = connection.execute(
                "SELECT id, role, content, agent_key, created_at "
                "FROM messages WHERE id > ? ORDER BY id",
                (after_id,),
            ).fetchall()
    return [dict(row) for row in rows]


@app.post("/api/messages")
def send_message(
    request: ChatRequest,
    _: Annotated[None, Depends(_require_access_code)],
) -> dict[str, object]:
    if request.agent_key not in AgentRouter.AGENTS:
        raise HTTPException(status_code=422, detail="Unknown agent persona.")

    try:
        if request.agent_key == "ba_agent":
            result = {
                "agent_role": AgentRouter.AGENTS["ba_agent"],
                "response": ba_agent_client.ask(request.message),
            }
        else:
            result = agent_router.route_query(request.message, agent_key=request.agent_key)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"{result_agent_name(request.agent_key)} could not process the message: {exc}",
        ) from exc

    created_at = datetime.now(timezone.utc).isoformat()
    with _database_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO messages (role, content, agent_key, created_at) VALUES (?, ?, ?, ?)",
            ("user", request.message.strip(), request.agent_key, created_at),
        )
        user_message_id = cursor.lastrowid
        cursor = connection.execute(
            "INSERT INTO messages (role, content, agent_key, created_at) VALUES (?, ?, ?, ?)",
            ("assistant", result["response"], request.agent_key, created_at),
        )
        assistant_message_id = cursor.lastrowid

    return {
        "user_message_id": user_message_id,
        "assistant_message_id": assistant_message_id,
        "agent_role": result["agent_role"],
        "response": result["response"],
        "created_at": created_at,
    }


def result_agent_name(agent_key: str) -> str:
    if agent_key == "ba_agent":
        return AgentRouter.AGENTS["ba_agent"]
    return AgentRouter.AGENTS.get(agent_key, AgentRouter.AGENTS["orchestrator"])
