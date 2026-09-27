import re
from typing import Dict, Any, List

class GovernanceGateChecker:
    def __init__(self, loader=None):
        self.loader = loader

    def check_project(self, project_name: str, description: str, domain: str = "General") -> Dict[str, Any]:
        """Perform automated 15-point AI Governance Audit on a project proposal."""
        findings = []
        risks = []
        tier = "Tier 1: Low Risk (Autonomous)"
        requires_hitl = False

        desc_lower = description.lower()
        domain_lower = domain.lower()

        # Check for High-Risk Domains & HITL Triggers (Tier 3)
        tier3_keywords = [
            "healthcare", "medical", "hiring", "recruitment", "cv screening", 
            "financial", "loan", "underwriting", "production deploy", "delete database"
        ]
        
        hitl_matches = [kw for kw in tier3_keywords if kw in desc_lower or kw in domain_lower]
        if hitl_matches:
            tier = "Tier 3: Critical / High Risk (Mandatory Founder Sign-Off)"
            requires_hitl = True
            findings.append(f"🚨 TIER 3 TRIGGER DETECTED: Project involves sensitive domain or high-impact operation ({', '.join(hitl_matches)}). Requires explicit founder approval.")

        # Check DPDP Data Privacy
        pii_keywords = ["user data", "phone", "email", "aadhaar", "passport", "medical record", "personal data"]
        has_pii = any(kw in desc_lower for kw in pii_keywords)
        if has_pii:
            risks.append({
                "risk": "DPDP Data Privacy & Consent Exposure",
                "severity": "HIGH",
                "control": "Enforce purpose limitation, user consent logging, and data minimisation per portfolio/04-dpdp-ai-checklist.md."
            })
            findings.append("⚠️ DPDP Compliance Required: Personal Identifiable Information (PII) processing detected.")
        else:
            findings.append("✅ Privacy Check: No raw unmasked PII processing explicitly identified in initial spec.")

        # Check Bias & Fairness Controls
        bias_keywords = ["hiring", "screening", "grading", "evaluation", "scoring", "credit"]
        if any(kw in desc_lower for kw in bias_keywords):
            risks.append({
                "risk": "Algorithmic Bias & Unfair Exclusion",
                "severity": "HIGH",
                "control": "Execute demographic parity testing and audit against portfolio/06-ai-bias-audit.md before deployment."
            })
            findings.append("⚠️ Bias Audit Required: Automated evaluation/scoring mechanism detected.")

        # Hallucination Check
        rag_keywords = ["rag", "llm", "chatbot", "generative ai", "ai assistant", "search"]
        if any(kw in desc_lower for kw in rag_keywords):
            risks.append({
                "risk": "AI Hallucination & False Grounding",
                "severity": "MEDIUM",
                "control": "Implement strict system prompt grounding, source citation verification, and fallback responses."
            })
            findings.append("ℹ️ RAG/LLM Guardrails Needed: Generative AI text output detected.")

        # Standard 15-Point Checklist Results
        checklist_score = 15 - len(risks)
        status = "PASSED" if checklist_score >= 12 and not requires_hitl else ("REQUIRES FOUNDER APPROVAL" if requires_hitl else "REQUIRES REMEDIATION")

        return {
            "project_name": project_name,
            "domain": domain,
            "risk_tier": tier,
            "requires_hitl": requires_hitl,
            "status": status,
            "checklist_score": f"{checklist_score}/15 Passed",
            "findings": findings,
            "identified_risks": risks,
            "governance_policy_ref": "portfolio/07-ai-governance-policy.md",
            "disclaimer": "This audit report is generated for governance evaluation and technical risk management purposes. Not legal advice."
        }
