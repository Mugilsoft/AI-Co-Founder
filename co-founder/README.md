# Mugil Soft Solutions — AI Co-Founder Agent

> **Mugil Soft Solutions — Innovating Today. Empowering Tomorrow.**

This repository contains the foundational documentation, governance assets, knowledge base, and operational templates for **Mugil Soft Solutions** — a startup focused on building commercially viable software and AI systems with trustworthy, responsible AI practices.

---

## Mission

Help Mugil Soft Solutions identify valuable business problems, create commercially viable products, build high-quality software and AI systems, manage technical and AI risks, develop customers, and establish trustworthy AI practices.

---

## Repository Structure

```
co-founder/
├── docs/                     # Company and architecture documentation
│   ├── company/              # Company identity, services, branding
│   └── architecture/         # Agent, memory, and approval system design
├── portfolio/                # 8-week AI Governance portfolio assets
├── knowledge-base/           # RAG source documents and reference material
├── templates/                # Reusable business, product, and decision templates
└── memory/                   # Persistent memory store (company, governance, technical)
```

---

## AI Governance Portfolio

The portfolio represents Mugil Soft Solutions' professional proof-of-work in AI governance:

| # | Asset | Week |
|---|-------|------|
| 1 | [AI Governance Glossary](portfolio/01-ai-governance-glossary.md) | Week 1 |
| 2 | [Responsible AI Principles Sheet](portfolio/02-responsible-ai-principles.md) | Week 2 |
| 3 | [Global AI Framework Comparison](portfolio/03-global-ai-framework-comparison.md) | Week 3 |
| 4 | [DPDP + AI Checklist](portfolio/04-dpdp-ai-checklist.md) | Week 4 |
| 5 | [AI Risk Register](portfolio/05-ai-risk-register.md) | Week 5 |
| 6 | [AI Bias Audit](portfolio/06-ai-bias-audit.md) | Week 6 |
| 7 | [AI Governance Policy](portfolio/07-ai-governance-policy.md) | Week 7 |
| 8 | [AI Governance Case Study](portfolio/08-ai-governance-case-study.md) | Week 8 |

---

## Core Principles

Every significant decision considers:

- **Customer Value** — Does it solve a real problem?
- **Business Viability** — Can it sustain revenue?
- **Technical Quality** — Is it well-built and maintainable?
- **AI Responsibility** — Is it fair, transparent, and accountable?
- **Privacy** — Is personal data protected?
- **Security** — Is the system secure by design?
- **Governance** — Are controls in place?
- **Scalability** — Can it grow?
- **Sustainability** — Can it last?

---

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| Backend | C#, .NET, ASP.NET Core, Entity Framework Core, REST APIs |
| Frontend | Angular, TypeScript, HTML, CSS, Angular Material |
| AI/ML | Python, PyTorch, scikit-learn, Hugging Face, LLMs, RAG, Ollama |
| Databases | SQL Server, MySQL, PostgreSQL, SQLite |
| Cloud | Microsoft Azure (App Service, Azure SQL, Storage, Functions) |
| DevOps | Git, GitHub/GitLab, Docker, CI/CD, Automated Testing |

---

## Key Documents

- [Company Profile](docs/company/COMPANY.md)
- [Services Catalog](docs/company/SERVICES.md)
- [Agent Architecture](docs/architecture/agent-architecture.md)
- [Memory Architecture](docs/architecture/memory-architecture.md)
- [Human Approval System](docs/architecture/human-approval-system.md)

---

## Demo-Safe CLI Behavior

This repository includes a safe demo implementation for CLI approval gates. The `guarded_actions.py` module simulates actions such as email sending, file writes, file deletion, and command execution unless an explicit approval path is triggered. This keeps the project safe for local testing and demonstration without performing destructive or external side effects by default.

For live or production usage, the same approval pattern can be extended to real integrations with email providers, file systems, and shell execution after adding the required credentials and safeguards.

---

## Shared PC and Mobile Chat

The responsive web chat lets your PC and phone use the same saved conversation while connected to the same private Wi-Fi network. The agent runs on the PC; the phone connects to it through a browser. Chat messages are stored locally on the PC in `memory/chat_history.sqlite3`.

1. Install dependencies with `.venv\Scripts\python.exe -m pip install -r requirements.txt`.
2. Start both agents and the chat server from the Co-Founder project root with `.venv\Scripts\python.exe run_web.py --host 0.0.0.0 --ba-project D:\BA-Agent-for-Mugil`. The BA Agent runs on localhost port 8001; the shared chat runs on port 8000.
3. Select **Business Analyst** in the chat to send a message to the BA agent. The other personas continue using the Co-Founder agents. The Business Analyst reuses one ADK conversation session.
4. Use the printed access code to sign in at the PC URL and the private Wi-Fi URL shown in the terminal on your phone. Both devices must be on the same Wi-Fi network.

The launcher expects the BA project at `D:\BA-Agent-for-Mugil` and uses that project's `.venv\Scripts\adk.exe` and `.env`; it does not read or display the BA credentials. The server generates a temporary chat access code at startup unless `COFOUNDER_CHAT_PASSWORD` is set in the environment or `.env`. Restarting without a configured code generates a new one; saved chat messages remain on the PC. If Windows Firewall prompts you, allow access on private networks only. Do not port-forward either server or expose them to the public internet. The BA API binds only to localhost; `--host 0.0.0.0` applies only to the shared chat so other devices on Wi-Fi can reach it.

---

*Built by Mugil Soft Solutions. All governance content is for professional and educational purposes. Legal advice should be sought from qualified professionals where required.*
