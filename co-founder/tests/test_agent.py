import sys
import os
import re
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.knowledge_loader import KnowledgeBaseLoader
from src.governance_checker import GovernanceGateChecker
from src.agent_router import AgentRouter

class TestKnowledgeBaseLoader(unittest.TestCase):
    """Unit tests for RAG KnowledgeBaseLoader."""
    
    @classmethod
    def setUpClass(cls):
        cls.loader = KnowledgeBaseLoader(root_dir=str(PROJECT_ROOT))

    def test_documents_loaded(self):
        """Verify knowledge base loads documents from workspace folders."""
        self.assertGreater(len(self.loader.documents), 0, "KnowledgeBaseLoader should load at least one document.")
        
        categories = {doc["category"] for doc in self.loader.documents}
        self.assertIn("docs", categories)
        self.assertIn("portfolio", categories)
        self.assertIn("knowledge-base", categories)

    def test_document_structure(self):
        """Verify each document contains required metadata fields."""
        for doc in self.loader.documents:
            self.assertIn("file_name", doc)
            self.assertIn("relative_path", doc)
            self.assertIn("category", doc)
            self.assertIn("title", doc)
            self.assertIn("content", doc)
            self.assertIn("tokens", doc)
            self.assertIsInstance(doc["tokens"], set)

    def test_search_relevant_documents(self):
        """Verify search returns top_k documents that overlap with query terms."""
        query = "DPDP Act compliance"
        results = self.loader.search(query, top_k=3)
        self.assertEqual(len(results), 3)
        
        query_tokens = set(re.findall(r"\w+", query.lower()))
        for doc in results:
            overlap = query_tokens.intersection(doc["tokens"])
            self.assertGreater(len(overlap), 0, f"Document {doc['relative_path']} should have term overlap with query.")

    def test_search_empty_query(self):
        """Verify search handles empty or whitespace query gracefully."""
        results = self.loader.search("", top_k=2)
        self.assertEqual(len(results), 2)

    def test_get_summary_stats(self):
        """Verify summary statistics calculation."""
        stats = self.loader.get_summary_stats()
        self.assertIsInstance(stats, dict)
        self.assertGreater(sum(stats.values()), 0)


class TestGovernanceGateChecker(unittest.TestCase):
    """Unit tests for GovernanceGateChecker AI Governance Audit."""

    def setUp(self):
        self.loader = KnowledgeBaseLoader(root_dir=str(PROJECT_ROOT))
        self.checker = GovernanceGateChecker(self.loader)

    def test_low_risk_project(self):
        """Verify Tier 1 Low-Risk autonomous approval for benign project."""
        res = self.checker.check_project(
            project_name="Doc Assistant",
            description="Internal CLI tool for reading markdown documentation.",
            domain="Internal Tools"
        )
        self.assertEqual(res["risk_tier"], "Tier 1: Low Risk (Autonomous)")
        self.assertFalse(res["requires_hitl"])
        self.assertEqual(res["status"], "PASSED")
        self.assertIn("/15 Passed", res["checklist_score"])

    def test_high_risk_tier3_trigger(self):
        """Verify Tier 3 Critical High Risk HITL trigger for sensitive domain."""
        res = self.checker.check_project(
            project_name="MedScanner AI",
            description="Healthcare diagnostic tool for evaluating medical records and patient screening.",
            domain="Healthcare"
        )
        self.assertEqual(res["risk_tier"], "Tier 3: Critical / High Risk (Mandatory Founder Sign-Off)")
        self.assertTrue(res["requires_hitl"])
        self.assertEqual(res["status"], "REQUIRES FOUNDER APPROVAL")
        self.assertTrue(any("TIER 3 TRIGGER DETECTED" in f for f in res["findings"]))

    def test_dpdp_privacy_detection(self):
        """Verify DPDP PII data privacy risk identification."""
        res = self.checker.check_project(
            project_name="User Auth Sync",
            description="Service processing user email, phone, and personal data for onboarding.",
            domain="Fintech"
        )
        pii_risks = [r for r in res["identified_risks"] if "DPDP" in r["risk"]]
        self.assertGreater(len(pii_risks), 0, "DPDP risk should be identified when processing PII.")
        self.assertEqual(pii_risks[0]["severity"], "HIGH")

    def test_algorithmic_bias_detection(self):
        """Verify algorithmic bias risk detection for automated scoring/hiring."""
        res = self.checker.check_project(
            project_name="HireMatch AI",
            description="Automated candidate grading and CV screening tool for recruitment.",
            domain="HR Tech"
        )
        bias_risks = [r for r in res["identified_risks"] if "Bias" in r["risk"]]
        self.assertGreater(len(bias_risks), 0, "Bias risk should be identified for automated screening.")

    def test_rag_hallucination_guardrails(self):
        """Verify RAG/LLM hallucination guardrail recommendation."""
        res = self.checker.check_project(
            project_name="Support Bot",
            description="Customer support RAG chatbot powered by LLM.",
            domain="Customer Service"
        )
        hallucination_risks = [r for r in res["identified_risks"] if "Hallucination" in r["risk"]]
        self.assertGreater(len(hallucination_risks), 0, "Hallucination risk should be identified for RAG/LLM.")


class TestAgentRouter(unittest.TestCase):
    """Unit tests for AgentRouter query routing and personas."""

    def setUp(self):
        self.loader = KnowledgeBaseLoader(root_dir=str(PROJECT_ROOT))
        self.router = AgentRouter(self.loader)

    def test_all_agent_roles_exist(self):
        """Verify all mandatory agent roles are defined."""
        expected_roles = ["orchestrator", "business", "cto", "ai_lead", "governance", "product", "developer"]
        for role in expected_roles:
            self.assertIn(role, AgentRouter.AGENTS)

    def test_route_query_orchestrator(self):
        """Verify routing query to orchestrator persona."""
        res = self.router.route_query("What is our overall company mission?", agent_key="orchestrator")
        self.assertEqual(res["agent_role"], AgentRouter.AGENTS["orchestrator"])
        self.assertIn("response", res)
        self.assertGreater(len(res["context_sources"]), 0)

    def test_route_query_cto(self):
        """Verify routing query to CTO persona."""
        res = self.router.route_query("What is our recommended technology stack?", agent_key="cto")
        self.assertEqual(res["agent_role"], AgentRouter.AGENTS["cto"])
        self.assertTrue(
            "Technical Architecture Guidance" in res["response"] or
            "tech" in res["response"].lower() or
            "architecture" in res["response"].lower(),
            "Response should contain CTO architecture guidance."
        )

    def test_route_query_governance(self):
        """Verify routing query to governance persona."""
        res = self.router.route_query("How do we comply with DPDP?", agent_key="governance")
        self.assertEqual(res["agent_role"], AgentRouter.AGENTS["governance"])
        self.assertTrue(
            "AI Governance" in res["response"] or "DPDP" in res["response"],
            "Response should contain DPDP or Governance guidance."
        )


    def test_hitl_action_detection(self):
        """Verify Tier 3 high-risk action queries trigger HITL warnings."""
        high_risk_queries = [
            "We need to deploy to production tomorrow.",
            "Can you delete database records?",
            "Please sign contract with vendor.",
            "Send price quote to potential customer."
        ]
        for q in high_risk_queries:
            res = self.router.route_query(q, agent_key="orchestrator")
            self.assertIsNotNone(res["hitl_warning"], f"Query '{q}' should trigger HITL warning.")
            self.assertIn("TIER 3 HIGH RISK ACTION DETECTED", res["hitl_warning"])

    def test_invalid_agent_key_defaults_to_orchestrator(self):
        """Verify invalid agent key gracefully falls back to orchestrator."""
        res = self.router.route_query("Hello", agent_key="non_existent_key")
        self.assertEqual(res["agent_role"], AgentRouter.AGENTS["orchestrator"])


from src.google_sheets_exporter import GoogleSheetsExporter
from src.lead_finder import LeadFinder


class TestGoogleSheetsExporter(unittest.TestCase):
    """Unit tests for GoogleSheetsExporter and LeadFinder export functionality."""

    def test_exporter_graceful_fallback(self):
        """Verify GoogleSheetsExporter handles missing credentials without crashing."""
        exporter = GoogleSheetsExporter(creds_path="non_existent_file.json")
        self.assertFalse(exporter.is_available())

        res = exporter.export_leads([{"company": "Test Co"}])
        self.assertEqual(res["status"], "error")
        self.assertIn("unavailable", res["message"].lower())

    def test_lead_finder_sheets_export_fallback(self):
        """Verify LeadFinder integrates GoogleSheetsExporter gracefully."""
        finder = LeadFinder(creds_path="non_existent_file.json")
        res = finder._offline_response("test query", "Test offline mode")
        finder._save_leads(res, export_sheets=True)
        self.assertIn("google_sheets", res)
        self.assertEqual(res["google_sheets"]["status"], "error")


if __name__ == "__main__":
    unittest.main()

