#!/usr/bin/env python3
"""
Mugil Soft Solutions — AI Co-Founder Agent
===========================================
CLI with a rich terminal UI, plus governed real-world actions (email,
filesystem, shell) wired through guarded_actions.py / GovernanceGateChecker.

Commands:
    python cli.py status
    python cli.py audit --desc "Automated CV screening for recruitment"
    python cli.py ask "What are our AI governance principles?"
    python cli.py chat
    python cli.py agents

Inside `ask` / `chat`, action commands are recognized by a leading `!` so a
plain question can never accidentally trigger a real email send or file
change:
    !email to=someone@x.com subject="Hello" body="Hi there"
    !write path=notes/draft.md content="Some text" [overwrite]
    !delete path=scratch/old.md
    !run pytest -q

Any action above Tier 1 prints the governance result and asks for founder
approval (y/n) before it executes. Nothing executes silently.
"""

import os
import re
import glob
import shlex
import argparse
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from dotenv import load_dotenv
load_dotenv()

try:
    from google import genai  # google-genai package
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

import guarded_actions
from guarded_actions import ApprovalRequired

console = Console(legacy_windows=False)

# ---------------------------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------------------------

KNOWLEDGE_DIRS = {
    "docs": "Company & Architecture Docs",
    "portfolio": "AI Governance Portfolio",
    "knowledge-base": "RAG Source Documents",
    "templates": "Business & Product Templates",
    "memory": "Persistent Memory Store",
}


@dataclass
class KBDocument:
    path: str
    category: str
    title: str
    content: str

    @property
    def word_count(self) -> int:
        return len(self.content.split())


class KnowledgeBaseLoader:
    """Loads and indexes all workspace documents for retrieval."""

    def __init__(self, root: str = "."):
        self.root = root
        self.documents: List[KBDocument] = []

    def load_all(self) -> List[KBDocument]:
        self.documents = []
        readme_path = os.path.join(self.root, "README.md")
        if os.path.exists(readme_path):
            self.documents.append(self._load_file(readme_path, "root"))

        for folder in KNOWLEDGE_DIRS:
            pattern = os.path.join(self.root, folder, "**", "*.md")
            for path in glob.glob(pattern, recursive=True):
                self.documents.append(self._load_file(path, folder))

        return self.documents

    def _load_file(self, path: str, category: str) -> KBDocument:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            content = ""
        title = os.path.splitext(os.path.basename(path))[0].replace("-", " ").replace("_", " ").title()
        return KBDocument(path=path, category=category, title=title, content=content)

    def search(self, query: str, top_k: int = 5) -> List[KBDocument]:
        """Simple term-overlap search across loaded documents (swap for embeddings later)."""
        if not query.strip():
            return []
        terms = set(re.findall(r"\w+", query.lower()))
        scored = []
        for doc in self.documents:
            doc_terms = set(re.findall(r"\w+", doc.content.lower()))
            overlap = len(terms & doc_terms)
            if overlap > 0:
                scored.append((overlap, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]

    def summary_stats(self) -> Dict[str, int]:
        stats: Dict[str, int] = {}
        for doc in self.documents:
            stats[doc.category] = stats.get(doc.category, 0) + 1
        return stats


# ---------------------------------------------------------------------------
# Governance Gate Checker
# ---------------------------------------------------------------------------

TIER_3_KEYWORDS = {
    "healthcare": ["health", "medical", "patient", "diagnosis", "clinical"],
    "recruitment": ["recruitment", "hiring", "cv screening", "resume screening", "candidate"],
    "database_deletion": ["delete database", "drop table", "delete all records", "wipe data"],
}

TIER_2_KEYWORDS = {
    "pii_dpdp": ["personal data", "pii", "aadhaar", "dpdp", "consent", "customer data"],
    "bias_sensitive": ["bias", "fairness", "discriminat", "protected class"],
}


@dataclass
class GovernanceResult:
    tier: int
    label: str
    requires_approval: bool
    triggers: List[str] = field(default_factory=list)
    controls: List[str] = field(default_factory=list)


class GovernanceGateChecker:
    """Classifies a project/action description into a governance risk tier."""

    def check(self, description: str) -> GovernanceResult:
        desc_lower = description.lower()

        triggers = [label for label, kws in TIER_3_KEYWORDS.items() if any(k in desc_lower for k in kws)]
        if triggers:
            return GovernanceResult(
                tier=3,
                label="Tier 3 — Critical (Human Approval Required)",
                requires_approval=True,
                triggers=triggers,
                controls=[
                    "Founder approval required before proceeding",
                    "Mandatory bias audit prior to deployment",
                    "Documented human-in-the-loop (HITL) checkpoint",
                    "Risk register entry logged",
                ],
            )

        triggers = [label for label, kws in TIER_2_KEYWORDS.items() if any(k in desc_lower for k in kws)]
        if triggers:
            return GovernanceResult(
                tier=2,
                label="Tier 2 — Moderate Risk (Review Recommended)",
                requires_approval=False,
                triggers=triggers,
                controls=[
                    "DPDP / privacy impact review",
                    "Data minimization check",
                    "Manager-level review recommended",
                ],
            )

        return GovernanceResult(
            tier=1,
            label="Tier 1 — Low Risk (Autonomous)",
            requires_approval=False,
            triggers=[],
            controls=["Standard logging only"],
        )


# ---------------------------------------------------------------------------
# Agent Router
# ---------------------------------------------------------------------------

AGENTS: Dict[str, Dict[str, object]] = {
    "orchestrator": {
        "label": "Orchestrator",
        "color": "bold white",
        "keywords": [],
        "system_prompt": "You are the Orchestrator for Mugil Soft Solutions' AI Co-Founder Agent. "
                          "You coordinate between business, technical, governance, and product concerns.",
    },
    "business": {
        "label": "Business Co-Founder",
        "color": "bold green",
        "keywords": ["revenue", "pricing", "customer", "market", "sales", "business model", "gtm"],
        "system_prompt": "You are the Business Co-Founder agent. Focus on customer value, "
                          "business viability, pricing, and go-to-market strategy.",
    },
    "cto": {
        "label": "CTO",
        "color": "bold cyan",
        "keywords": ["architecture", "backend", "database", "api", "infrastructure", "scal"],
        "system_prompt": "You are the CTO agent. Focus on technical architecture, scalability, "
                          "and engineering quality.",
    },
    "governance": {
        "label": "Governance Officer",
        "color": "bold red",
        "keywords": ["governance", "risk", "compliance", "bias", "dpdp", "privacy", "audit"],
        "system_prompt": "You are the AI Governance agent. Focus on responsible AI, risk tiers, "
                          "and regulatory compliance (e.g., DPDP).",
    },
    "product": {
        "label": "Product Lead",
        "color": "bold magenta",
        "keywords": ["feature", "roadmap", "ux", "user experience", "product"],
        "system_prompt": "You are the Product Lead agent. Focus on features, roadmap, and user needs.",
    },
    "ai_lead": {
        "label": "AI Lead",
        "color": "bold yellow",
        "keywords": ["model", "llm", "rag", "embedding", "fine-tun", "prompt", "hallucin"],
        "system_prompt": "You are the AI Lead agent. Focus on model selection, RAG design, "
                          "prompt engineering, and hallucination guardrails.",
    },
    "developer": {
        "label": "Developer",
        "color": "bold blue",
        "keywords": ["bug", "code", "implement", "function", "test", "deploy"],
        "system_prompt": "You are the Developer agent. Focus on implementation details, "
                          "code quality, and testing.",
    },
}


class AgentRouter:
    def __init__(self, kb: KnowledgeBaseLoader):
        self.kb = kb

    def route(self, query: str) -> str:
        query_lower = query.lower()
        best_key, best_score = "orchestrator", 0
        for key, agent in AGENTS.items():
            if key == "orchestrator":
                continue
            score = sum(1 for kw in agent["keywords"] if kw in query_lower)
            if score > best_score:
                best_key, best_score = key, score
        return best_key

    def is_high_risk_action(self, query: str) -> bool:
        return GovernanceGateChecker().check(query).tier >= 2


# ---------------------------------------------------------------------------
# LLM call (optional live mode — falls back to demo mode with no key)
# ---------------------------------------------------------------------------

def call_llm(system_prompt: str, query: str, context: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

    if not (HAS_GENAI and api_key):
        return (
            "**[DEMO MODE — no GEMINI_API_KEY detected]**\n\n"
            f"*Would respond as:* {system_prompt}\n\n"
            f"**Relevant context found:**\n\n{context[:400] or '(none found in knowledge base)'}"
        )

    try:
        from google.genai import types
        client = genai.Client(api_key=api_key)
        prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {query[:2000]}"
        max_tokens = int(os.environ.get("MAX_OUTPUT_TOKENS", "1024"))
        config = types.GenerateContentConfig(max_output_tokens=max_tokens)
        response = client.models.generate_content(model=model, contents=prompt, config=config)
        # Guard against empty/None response (e.g. safety filter blocks)
        text = getattr(response, "text", None)
        if not text:
            finish = getattr(response.candidates[0], "finish_reason", "UNKNOWN") if response.candidates else "NO_CANDIDATES"
            return (
                f"> [!WARNING]\n"
                f"> **Model returned an empty response** (finish_reason: `{finish}`). "
                "This may be due to a safety filter or a blocked prompt. "
                "Please rephrase your question.\n\n"
                f"{context[:400] or '(no knowledge base context found)'}"
            )
        return text
    except Exception as e:
        err_str = str(e)
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
            return (
                "> [!NOTE]\n"
                "> **API Quota Limit Reached (429 Rate Limit)**: Free-tier quota exceeded. "
                "Falling back to verified knowledge base context.\n\n"
                f"{context}"
            )
        return f"**[LLM call failed]** {e}"


# ---------------------------------------------------------------------------
# Action commands — !email / !write / !delete / !run inside ask/chat
# ---------------------------------------------------------------------------

ACTION_HELP = (
    "[dim]Action commands (require founder approval above Tier 1):[/dim]\n"
    '[dim]  !email to=addr subject="..." body="..."[/dim]\n'
    '[dim]  !write path=... content="..." [overwrite][/dim]\n'
    "[dim]  !delete path=...[/dim]\n"
    "[dim]  !run <command> [args...][/dim]\n"
)

_KV_PATTERN = re.compile(r'(\w+)=(".*?"|\'.*?\'|\S+)')


def _parse_kv(text: str) -> Dict[str, str]:
    out = {}
    for key, val in _KV_PATTERN.findall(text):
        out[key] = val.strip("\"'")
    return out


def parse_action(query: str) -> Optional[dict]:
    """Return a structured action dict if query is an action command, else None."""
    q = query.strip()
    if not q.startswith("!"):
        return None

    parts = q[1:].split(None, 1)
    verb = parts[0].lower() if parts else ""
    rest = parts[1] if len(parts) > 1 else ""

    if verb == "email":
        kv = _parse_kv(rest)
        return {"type": "email", "to": kv.get("to", ""), "subject": kv.get("subject", ""), "body": kv.get("body", "")}
    if verb == "write":
        kv = _parse_kv(rest)
        return {
            "type": "write",
            "path": kv.get("path", ""),
            "content": kv.get("content", ""),
            "overwrite": "overwrite" in rest.lower(),
        }
    if verb == "delete":
        kv = _parse_kv(rest)
        return {"type": "delete", "path": kv.get("path", "")}
    if verb == "run":
        return {"type": "run", "command": shlex.split(rest)}

    return {"type": "unknown", "verb": verb}


def _approval_prompt(exc: ApprovalRequired) -> bool:
    console.print(Panel(
        f"[bold]{exc.result.label}[/bold]\n\n"
        f"Action: {exc.description}\n"
        f"Triggers: {', '.join(exc.result.triggers) or '(action-type floor, no keyword trigger)'}\n\n"
        "[bold]Required controls:[/bold]\n" + "\n".join(f"  - {c}" for c in exc.result.controls),
        title="Founder approval required",
        border_style="red",
        box=box.HEAVY,
    ))
    return Confirm.ask("[bold red]Approve this action and proceed?[/bold red]", default=False)


def execute_action(action: dict) -> None:
    """Run a parsed action through guarded_actions, prompting for approval as needed."""
    try:
        if action["type"] == "email":
            if not action["to"] or not action["subject"]:
                console.print("[red]Usage:[/red] !email to=addr subject=\"...\" body=\"...\"")
                return
            guarded_actions.guarded_send_email(action["to"], action["subject"], action["body"])
            console.print(Panel(f"Email sent to {action['to']}.", border_style="green", title="Email sent"))

        elif action["type"] == "write":
            if not action["path"]:
                console.print("[red]Usage:[/red] !write path=... content=\"...\" [overwrite]")
                return
            result = guarded_actions.guarded_write_file(action["path"], action["content"], overwrite=action["overwrite"])
            console.print(Panel(result, border_style="green", title="File written"))

        elif action["type"] == "delete":
            if not action["path"]:
                console.print("[red]Usage:[/red] !delete path=...")
                return
            result = guarded_actions.guarded_delete_path(action["path"])
            console.print(Panel(result, border_style="green", title="File deleted"))

        elif action["type"] == "run":
            if not action["command"]:
                console.print("[red]Usage:[/red] !run <command> [args...]")
                return
            result = guarded_actions.guarded_run_command(action["command"])
            console.print(Panel(
                f"[bold]stdout:[/bold]\n{result['stdout']}\n[bold]stderr:[/bold]\n{result['stderr']}\n"
                f"[bold]exit code:[/bold] {result['returncode']}",
                border_style="green", title="Command finished",
            ))

        else:
            console.print(f"[red]Unknown action:[/red] !{action.get('verb', '')}")
            console.print(ACTION_HELP)

    except ApprovalRequired as exc:
        if _approval_prompt(exc):
            try:
                if action["type"] == "email":
                    guarded_actions.guarded_send_email(action["to"], action["subject"], action["body"], approved=True)
                    console.print(Panel(f"Email sent to {action['to']}.", border_style="green", title="Email sent"))
                elif action["type"] == "write":
                    r = guarded_actions.guarded_write_file(
                        action["path"], action["content"], overwrite=action["overwrite"], approved=True
                    )
                    console.print(Panel(r, border_style="green", title="File written"))
                elif action["type"] == "delete":
                    r = guarded_actions.guarded_delete_path(action["path"], approved=True)
                    console.print(Panel(r, border_style="green", title="File deleted"))
                elif action["type"] == "run":
                    r = guarded_actions.guarded_run_command(action["command"], approved=True)
                    console.print(Panel(
                        f"[bold]stdout:[/bold]\n{r['stdout']}\n[bold]stderr:[/bold]\n{r['stderr']}\n"
                        f"[bold]exit code:[/bold] {r['returncode']}",
                        border_style="green", title="Command finished",
                    ))
            except Exception as e:
                console.print(f"[red]Action failed after approval:[/red] {e}")
        else:
            console.print("[yellow]Action cancelled — not approved.[/yellow]")

    except Exception as e:
        console.print(f"[red]Action failed:[/red] {e}")


# ---------------------------------------------------------------------------
# Rich Terminal UI
# ---------------------------------------------------------------------------

BANNER = (
    "[bold cyan]"
    "+-----------------------------------------------+\n"
    "|      MUGIL SOFT SOLUTIONS - AI CO-FOUNDER      |\n"
    "|   Innovating Today. Empowering Tomorrow.       |\n"
    "+-----------------------------------------------+"
    "[/bold cyan]"
)


def show_banner():
    console.print(BANNER)


def cmd_status(kb: KnowledgeBaseLoader):
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                  console=console, transient=True) as progress:
        progress.add_task("Indexing workspace documents...", total=None)
        kb.load_all()

    stats = kb.summary_stats()
    table = Table(title="Knowledge Base Status", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("Category")
    table.add_column("Documents", justify="right")
    total = 0
    all_categories = {"root": "Root README", **KNOWLEDGE_DIRS}
    active = 0
    for category, label in all_categories.items():
        count = stats.get(category, 0)
        total += count
        if count:
            active += 1
        table.add_row(label, str(count))
    console.print(table)
    console.print(f"[bold green]Total indexed:[/bold green] {total} documents across {active} categories\n")


def cmd_audit(description: str):
    result = GovernanceGateChecker().check(description)
    tier_colors = {1: "green", 2: "yellow", 3: "red"}
    color = tier_colors.get(result.tier, "white")

    body = f"[bold]{result.label}[/bold]\n\n"
    if result.triggers:
        body += "[bold]Triggers detected:[/bold]\n"
        for t in result.triggers:
            body += f"  - {t.replace('_', ' ').title()}\n"
        body += "\n"
    body += "[bold]Required controls:[/bold]\n"
    for c in result.controls:
        body += f"  - {c}\n"
    if result.requires_approval:
        body += "\n[bold red]** FOUNDER APPROVAL REQUIRED BEFORE PROCEEDING **[/bold red]"

    console.print(Panel(body, title=f"Governance Audit: {description}", border_style=color, box=box.HEAVY))


def cmd_agents():
    table = Table(title="Available Agent Personas", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("Key")
    table.add_column("Persona")
    table.add_column("Focus Keywords")
    for key, agent in AGENTS.items():
        color = agent["color"]
        table.add_row(key, f"[{color}]{agent['label']}[/{color}]", ", ".join(agent["keywords"]) or "(default/fallback)")
    console.print(table)


def cmd_ask(kb: KnowledgeBaseLoader, router: AgentRouter, query: str, reload_kb: bool = True):
    # Action commands (!email, !write, !delete, !run) bypass the Q&A path entirely.
    action = parse_action(query)
    if action is not None:
        execute_action(action)
        return

    if reload_kb:
        kb.load_all()
    agent_key = router.route(query)
    agent = AGENTS[agent_key]

    if router.is_high_risk_action(query):
        gov = GovernanceGateChecker().check(query)
        console.print(Panel(
            f"[bold red]This query touches a {gov.label} area.[/bold red]\n"
            f"Triggers: {', '.join(gov.triggers) or 'sensitive data handling'}",
            border_style="red", title="Governance Notice",
        ))

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                  console=console, transient=True) as progress:
        progress.add_task(f"Routing to {agent['label']} - searching knowledge base...", total=None)
        results = kb.search(query)
        context = "\n\n".join(f"[{d.title}]\n{d.content[:500]}" for d in results)
        answer = call_llm(agent["system_prompt"], query, context)

    console.print(Panel(
        Markdown(answer),
        title=f"[{agent['color']}]{agent['label']}[/{agent['color']}] responding",
        border_style=agent["color"],
        box=box.ROUNDED,
    ))

    if results:
        console.print("[dim]Sources: " + ", ".join(d.title for d in results) + "[/dim]\n")


def cmd_chat(kb: KnowledgeBaseLoader, router: AgentRouter):
    show_banner()
    kb.load_all()
    console.print("[dim]Type your question, or 'exit' to quit.[/dim]")
    console.print(ACTION_HELP)
    while True:
        query = Prompt.ask("[bold cyan]You[/bold cyan]")
        if query.strip().lower() in {"exit", "quit"}:
            console.print("[bold]Goodbye![/bold]")
            break
        cmd_ask(kb, router, query, reload_kb=False)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Mugil AI Co-Founder Agent CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show knowledge base indexing status")

    audit_parser = sub.add_parser("audit", help="Run a governance risk audit on a project description")
    audit_parser.add_argument("--desc", required=True, help="Description of the project/action to audit")

    ask_parser = sub.add_parser("ask", help="Ask the AI Co-Founder Agent a single question (or run a !action)")
    ask_parser.add_argument("query", help="Your question, or an !email / !write / !delete / !run command")

    sub.add_parser("chat", help="Start an interactive chat session (supports !action commands)")
    sub.add_parser("agents", help="List available agent personas")

    args = parser.parse_args()

    kb = KnowledgeBaseLoader(root=".")
    router = AgentRouter(kb)

    if args.command == "status":
        show_banner()
        cmd_status(kb)
    elif args.command == "audit":
        show_banner()
        cmd_audit(args.desc)
    elif args.command == "ask":
        show_banner()
        cmd_ask(kb, router, args.query)
    elif args.command == "chat":
        cmd_chat(kb, router)
    elif args.command == "agents":
        show_banner()
        cmd_agents()
    else:
        show_banner()
        parser.print_help()


if __name__ == "__main__":
    main()