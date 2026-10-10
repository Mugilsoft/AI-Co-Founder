"""
Mugil AI Co-Founder — Leads & Growth Specialist
Mugil Soft Solutions — Innovating Today. Empowering Tomorrow.

Uses Gemini's built-in Google Search grounding tool to find REAL companies
matching an Ideal Customer Profile (ICP). Never fabricates leads: if search
grounding is unavailable or returns nothing, it says so instead of guessing.

Design mirrors GovernanceGateChecker's philosophy: structured output,
explicit disclaimers, and a hard rule that nothing gets auto-sent —
every lead is a draft for human review.
"""

import os
import re
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.google_sheets_exporter import GoogleSheetsExporter

# Top-level import — not repeated on every request
try:
    from google.genai import types as _genai_types
    _HAS_GENAI_TYPES = True
except ImportError:
    _HAS_GENAI_TYPES = False


class LeadFinder:
    """Leads sub-agent for the Mugil AI Co-Founder system."""

    DEFAULT_ICP = {
        "industry": "EPC / Construction / Infrastructure companies in India",
        "signals": ["active tender/bidding process", "digital transformation initiative", "AI adoption interest"],
        "company_size": "200-2000 employees",
        "region": "India",
        "buyer_titles": ["Digital Transformation Head", "IT Head", "VP Operations", "CTO"],
    }

    LEAD_FIELDS = ["company", "why_it_fits", "likely_contact_title", "source_url", "suggested_opener"]

    def __init__(self, loader=None, icp: Optional[Dict[str, Any]] = None, leads_dir: str = "memory/leads", creds_path: Optional[str] = None):
        self._load_env()
        self.loader = loader
        self.icp = icp or self.DEFAULT_ICP
        self.leads_dir = Path(leads_dir)
        self.leads_dir.mkdir(parents=True, exist_ok=True)
        self.sheets_exporter = GoogleSheetsExporter(creds_path=creds_path)

        self.api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        self.client = None
        self.search_enabled = False

        # ── Read config ONCE at startup ────────────────────────────────────
        self._model_name = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
        # Leads JSON needs more tokens than general chat — use separate budget
        self._max_tokens = int(os.environ.get("LEADS_MAX_OUTPUT_TOKENS", "2048"))

        # ── Build config ONCE — reused for all lead requests ──────────────────
        self._gen_config = None
        if _HAS_GENAI_TYPES:
            self._gen_config = _genai_types.GenerateContentConfig(
                max_output_tokens=self._max_tokens,
                temperature=0.1,  # low temp for consistent structured JSON output
                tools=[_genai_types.Tool(google_search=_genai_types.GoogleSearch())]
            )

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                self.search_enabled = True
            except Exception as e:
                print(f"Note: Gemini SDK initialization notice: {e}")

    def _load_env(self):
        p = Path(__file__).parent.parent / ".env"
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v

    def _icp_prompt(self) -> str:
        return (
            f"Industry: {self.icp.get('industry')}\n"
            f"Company size: {self.icp.get('company_size')}\n"
            f"Region: {self.icp.get('region')}\n"
            f"Buying signals: {', '.join(self.icp.get('signals', []))}\n"
            f"Typical buyer titles: {', '.join(self.icp.get('buyer_titles', []))}"
        )

    def _get_previously_saved_companies(self) -> List[str]:
        companies = set()
        for json_file in self.leads_dir.glob("leads_*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for lead in data.get("leads", []):
                        if lead.get("company"):
                            companies.add(lead["company"])
            except Exception:
                pass
        return list(companies)

    def find_leads(
        self,
        query: str,
        count: int = 5,
        export_sheets: bool = False,
        spreadsheet_name: str = "Mugil AI Leads",
        spreadsheet_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search the live web (via Gemini Google Search grounding) for companies
        matching the ICP + the user's request, and return structured leads.
        Every lead is a draft for human review — nothing is auto-sent.
        """
        if not self.search_enabled:
            return self._offline_response(query, reason="No GEMINI_API_KEY/GOOGLE_API_KEY configured.")

        try:

            previous_companies = self._get_previously_saved_companies()
            exclude_prompt = ""
            if previous_companies:
                exclude_prompt = (
                    f"\nDo NOT include these previously found companies; search for NEW, DISTINCT companies: "
                    f"{', '.join(previous_companies[:30])}\n"
                )

            system_prompt = f"""You are the Leads & Growth Specialist at Mugil Soft Solutions.

Ideal Customer Profile:
{self._icp_prompt()}
{exclude_prompt}
Task: Using live web search, find up to {count} REAL companies matching
this ICP and the user's request below. Use ONLY information you actually
find via search — never invent a company, contact name, or URL. If a
detail can't be verified, write "not found" for that field.

Return your findings as a JSON array ONLY (no markdown fences, no other
text). Each element must have exactly these keys:
"company", "why_it_fits", "likely_contact_title", "source_url", "suggested_opener".

The "suggested_opener" must be a short, specific, non-generic first-touch
line referencing something real you found about that company. It is a
DRAFT for human review — do not imply it will be sent automatically.

User request: {query}
"""

            response = self.client.models.generate_content(
                model=self._model_name,
                contents=system_prompt,
                config=self._gen_config,  # reused cached config (2048 tokens, temp=0.1)
            )

            leads = self._parse_leads_json(response.text or "")
            sources = self._extract_grounding_sources(response)

            result = {
                "query": query,
                "icp": self.icp,
                "leads": leads,
                "grounding_sources": sources,
                "disclaimer": (
                    "Draft leads for human review only. Verify each company and contact "
                    "before any outreach — nothing here is auto-sent."
                ),
                "generated_at": datetime.utcnow().isoformat() + "Z",
            }

            if leads:
                self._save_leads(
                    result,
                    export_sheets=export_sheets,
                    spreadsheet_name=spreadsheet_name,
                    spreadsheet_id=spreadsheet_id
                )
            return result

        except Exception as e:
            return self._offline_response(query, reason=f"Live search failed: {e}")

    def _parse_leads_json(self, raw_text: str) -> List[Dict[str, Any]]:
        cleaned = re.sub(r"^```(json)?|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
        try:
            data = json.loads(cleaned)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                pass
        return []

    def _extract_grounding_sources(self, response) -> List[str]:
        sources = []
        try:
            for candidate in getattr(response, "candidates", None) or []:
                gm = getattr(candidate, "grounding_metadata", None)
                if not gm:
                    continue
                for chunk in getattr(gm, "grounding_chunks", None) or []:
                    web = getattr(chunk, "web", None)
                    uri = getattr(web, "uri", None) if web else None
                    if uri:
                        sources.append(uri)
        except Exception:
            pass
        return sources

    def _offline_response(self, query: str, reason: str) -> Dict[str, Any]:
        return {
            "query": query,
            "icp": self.icp,
            "leads": [],
            "grounding_sources": [],
            "disclaimer": (
                f"{reason} No leads were fabricated. Configure a Gemini API key with "
                "search grounding enabled to generate real, verifiable leads."
            ),
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

    def _save_leads(
        self,
        result: Dict[str, Any],
        export_sheets: bool = False,
        spreadsheet_name: str = "Mugil AI Leads",
        spreadsheet_id: Optional[str] = None
    ) -> None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        json_path = self.leads_dir / f"leads_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        leads = result.get("leads", [])
        if leads:
            csv_path = self.leads_dir / f"leads_{timestamp}.csv"
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.LEAD_FIELDS)
                writer.writeheader()
                for lead in leads:
                    writer.writerow({k: lead.get(k, "") for k in self.LEAD_FIELDS})

        if export_sheets or self.sheets_exporter.is_available():
            sheets_res = self.sheets_exporter.export_leads(
                leads=leads,
                spreadsheet_name=spreadsheet_name,
                spreadsheet_id=spreadsheet_id
            )
            result["google_sheets"] = sheets_res

