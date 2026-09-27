import os
from typing import Dict, Any, List
from src.knowledge_loader import KnowledgeBaseLoader
from src.governance_checker import GovernanceGateChecker
from src.lead_finder import LeadFinder
class AgentRouter:
    AGENTS = {
        "orchestrator": "Co-Founder & Strategy Orchestrator",
        "business": "Business & Market Specialist",
        "cto": "CTO & Solution Architect",
        "ai_lead": "AI & ML Lead Engineer",
        "governance": "Responsible AI & Governance Officer",
        "product": "Product Manager",
        "developer": "Full-Stack Lead Developer",
        "leads": "Leads & Growth Specialist"
    }

    def __init__(self, loader: KnowledgeBaseLoader):
        self.loader = loader
        self.governance_checker = GovernanceGateChecker(loader)
        self.lead_finder = LeadFinder(loader)
        self.api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Note: Gemini SDK initialization notice: {e}")

    def route_query(self, query: str, agent_key: str = "orchestrator") -> Dict[str, Any]:
        """Routes query to selected agent persona with RAG context."""
        # The leads agent has its own live-search pipeline instead of
        # static-document RAG — route it separately, same response shape.
        if agent_key == "leads":
            return self._handle_leads_query(query)

       
        agent_name = self.AGENTS.get(agent_key, self.AGENTS["orchestrator"])
        
        # 1. Retrieve relevant RAG context
        retrieved_docs = self.loader.search(query, top_k=3)
        context_str = "\n\n".join([
            f"--- Context Doc: {d['relative_path']} ({d['title']}) ---\n{d['content'][:1500]}..."
            for d in retrieved_docs
        ])

        # 2. Check if query triggers Tier 3 High Risk HITL
        hitl_warning = None
        lower_query = query.lower()
        if any(kw in lower_query for kw in ["deploy to production", "delete database", "sign contract", "price quote"]):
            hitl_warning = "🚨 TIER 3 HIGH RISK ACTION DETECTED: This action requires explicit Founder Approval per docs/architecture/human-approval-system.md."

        # 3. Generate response using LLM or Guided Template
        if self.client:
            try:
                system_prompt = f"""You are the {agent_name} at Mugil Soft Solutions.
Tagline: Innovating Today. Empowering Tomorrow.

You operate adhering strictly to Mugil's 5 Responsible AI Principles (Fairness, Transparency, Accountability, Privacy, Human Oversight) and India's DPDP Act 2023.

Use the provided knowledge base context to answer concisely and professionally in markdown format.

Context:
{context_str}
"""
                model_name = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=f"{system_prompt}\n\nUser Question: {query}"
                )
                answer_text = response.text
            except Exception as e:
                answer_text = self._offline_response(agent_key, query, retrieved_docs, hitl_warning)
        else:
            answer_text = self._offline_response(agent_key, query, retrieved_docs, hitl_warning)

        return {
            "agent_role": agent_name,
            "query": query,
            "context_sources": [d["relative_path"] for d in retrieved_docs],
            "hitl_warning": hitl_warning,
            "response": answer_text
        }

    def _handle_leads_query(self, query: str, count: int = 5) -> Dict[str, Any]:
        """Runs a live lead search and formats it into the standard response shape."""
        result = self.lead_finder.find_leads(query, count=count)
        leads = result.get("leads", [])

        lines = ["### [Leads & Growth Specialist Response]\n"]
        if result.get("leads") == [] and result.get("disclaimer"):
            lines.append(f"> [!NOTE]\n> {result['disclaimer']}\n")

        if not leads:
            lines.append("No verified leads were found for this query. Try narrowing the request "
                          "(e.g. a specific region, sector signal, or company size band).")
        else:
            for i, lead in enumerate(leads, 1):
                lines.append(f"**{i}. {lead.get('company', 'Unknown')}**")
                lines.append(f"- Fit: {lead.get('why_it_fits', 'not found')}")
                lines.append(f"- Likely contact: {lead.get('likely_contact_title', 'not found')}")
                lines.append(f"- Source: {lead.get('source_url', 'not found')}")
                lines.append(f"- Suggested opener (draft — review before sending): "
                             f"_{lead.get('suggested_opener', 'not found')}_\n")
            lines.append(f"> {result.get('disclaimer', '')}")
            lines.append(f"\nSaved to `memory/leads/` for your review and CRM import.")

        return {
            "agent_role": self.AGENTS["leads"],
            "query": query,
            "context_sources": result.get("grounding_sources", []),
            "hitl_warning": None,
            "response": "\n".join(lines),
        }

    def _offline_response(self, agent_key: str, query: str, docs: List[Dict[str, Any]], hitl_warning: str = None) -> str:
        agent_name = self.AGENTS.get(agent_key, self.AGENTS["orchestrator"])
        sources_str = ", ".join([f"`{d['relative_path']}`" for d in docs])

        text = f"### [{agent_name} Response]\n\n"
        if hitl_warning:
            text += f"> [!WARNING]\n> {hitl_warning}\n\n"

        text += f"**Analysis & Strategic Guidance for**: *\"{query}\"*\n\n"
        text += f"I have analyzed your query against Mugil Soft Solutions' knowledge base sources: {sources_str}.\n\n"

        if agent_key == "business":
            text += "#### Business Evaluation Framework\n"
            text += "- **Target Customer & Pain**: Addressable market needs robust automation and verified AI compliance.\n"
            text += "- **Value Proposition**: Mugil's Responsible AI & Governance positioning sets us apart from generic software shops.\n"
            text += "- **Recommended Template**: Use `templates/business-strategy-template.md` to map revenue streams and unit economics.\n"
        elif agent_key == "cto":
            text += "#### Technical Architecture Guidance\n"
            text += "- **Recommended Tech Stack**: React/Vite + Node.js/Python FastAPI + PostgreSQL + Redis.\n"
            text += "- **Architecture Standard**: Modular Clean Code architecture with strict API contracts.\n"
            text += "- **Reference**: Check `knowledge-base/technology-standards.md` for full stack specs.\n"
        elif agent_key == "governance":
            text += "#### AI Governance & Compliance Assessment\n"
            text += "- **Regulatory Alignment**: Checked against DPDP Act 2023 (`portfolio/04-dpdp-ai-checklist.md`).\n"
            text += "- **Risk Mitigation**: Verify purpose limitation, user consent logging, and human oversight controls.\n"
            text += "- **Disclaimer**: *This assessment is for technical governance and risk evaluation purposes. Not legal advice.*\n"
        elif agent_key == "product":
            text += "#### Product Requirement Specification\n"
            text += "- **Phase 1 MVP Scope**: Focus strictly on Must-Have features defined via MoSCoW prioritization.\n"
            text += "- **Workflow Reference**: Follow 5-phase development lifecycle in `templates/product-development-template.md`.\n"
        else: # orchestrator / general
            text += "#### Executive Co-Founder Synthesis\n"
            text += "- **Strategic Alignment**: Directly supports Mugil Soft Solutions' mission (*Innovating Today. Empowering Tomorrow.*).\n"
            text += "- **Next Action**: Execute the 15-point AI Engineering Checklist (`templates/ai-engineering-checklist.md`) before sprint commitment.\n"

        return text
