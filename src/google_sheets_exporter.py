"""
Mugil AI Co-Founder — Google Sheets Lead Exporter
Mugil Soft Solutions — Innovating Today. Empowering Tomorrow.

Exports leads discovered by LeadFinder directly to Google Sheets via gspread.
Supports authentication using Service Account JSON key files or dicts.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class GoogleSheetsExporter:
    """Exports leads to a Google Sheet."""

    HEADERS = ["Company", "Fit / ICP Match", "Likely Contact Title", "Source URL", "Suggested Opener", "Timestamp"]

    def __init__(self, creds_path: Optional[str] = None):
        self.creds_path = creds_path or self._detect_creds_path()
        self.client = None
        self._init_client()

    def _detect_creds_path(self) -> Optional[str]:
        """Detect service account credentials file location."""
        env_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or os.environ.get("GSPREAD_CREDENTIALS")
        if env_path and Path(env_path).exists():
            return env_path
        
        for candidate in ["credentials.json", "service_account.json", "config/credentials.json"]:
            if Path(candidate).exists():
                return str(Path(candidate).resolve())
        return None

    def _init_client(self):
        """Initialize gspread client if dependencies and credentials exist."""
        if not self.creds_path:
            return
        
        try:
            import gspread
            self.client = gspread.service_account(filename=self.creds_path)
        except Exception as e:
            print(f"Note: Google Sheets API initialization notice: {e}")
            self.client = None

    def is_available(self) -> bool:
        """Check if Google Sheets integration is active and authenticated."""
        return self.client is not None

    def export_leads(
        self,
        leads: List[Dict[str, Any]],
        spreadsheet_name: str = "Mugil AI Leads",
        spreadsheet_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export a list of lead dicts to Google Sheets.
        
        Creates a new spreadsheet or appends to an existing one.
        Returns result dict with status, spreadsheet URL, and row count.
        """
        if not leads:
            return {"status": "error", "message": "No leads provided to export."}

        if not self.is_available():
            return {
                "status": "error",
                "message": (
                    "Google Sheets integration unavailable. "
                    "Ensure `gspread` is installed and a valid Service Account JSON file is present "
                    "or set via GOOGLE_APPLICATION_CREDENTIALS."
                )
            }

        try:
            import gspread

            if spreadsheet_id:
                sheet = self.client.open_by_key(spreadsheet_id)
            else:
                try:
                    sheet = self.client.open(spreadsheet_name)
                except gspread.SpreadsheetNotFound:
                    sheet = self.client.create(spreadsheet_name)

            worksheet = sheet.sheet1

            existing_values = worksheet.get_all_values()
            existing_companies = set()
            if existing_values:
                # Column 0 is Company name
                for row in existing_values[1:]:
                    if row and row[0]:
                        existing_companies.add(row[0].strip().lower())
            else:
                worksheet.append_row(self.HEADERS)

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rows_to_append = []
            skipped_count = 0
            for lead in leads:
                comp_name = lead.get("company", "Unknown").strip()
                if comp_name.lower() in existing_companies:
                    skipped_count += 1
                    continue

                row = [
                    comp_name,
                    lead.get("why_it_fits", "N/A"),
                    lead.get("likely_contact_title", "N/A"),
                    lead.get("source_url", "N/A"),
                    lead.get("suggested_opener", "N/A"),
                    now_str
                ]
                rows_to_append.append(row)
                existing_companies.add(comp_name.lower())

            if rows_to_append:
                worksheet.append_rows(rows_to_append)

            msg = f"Successfully exported {len(rows_to_append)} new lead(s) to '{sheet.title}'."
            if skipped_count > 0:
                msg += f" ({skipped_count} duplicate lead(s) skipped)."

            return {
                "status": "success",
                "spreadsheet_title": sheet.title,
                "spreadsheet_url": sheet.url,
                "added_count": len(rows_to_append),
                "skipped_count": skipped_count,
                "message": msg
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to export to Google Sheets: {str(e)}"
            }
