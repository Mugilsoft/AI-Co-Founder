"""
gmail_connector.py — Gmail integration for the Mugil AI Co-Founder Agent.

Setup (one time):
    1. Enable the Gmail API in Google Cloud Console.
    2. Create an OAuth client ID (Desktop app) and save it as credentials.json
       in the project root.
    3. pip install google-api-python-client google-auth-oauthlib

First run opens a browser for consent and writes token.json, which is reused
on later runs until it expires or scopes change.
"""

from __future__ import annotations

import base64
import os
from email.mime.text import MIMEText
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Narrowest scope by default. Add "https://www.googleapis.com/auth/gmail.send"
# only once you're ready for the agent to send mail, and gmail.modify only if
# it needs to label/archive/delete.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CREDENTIALS_PATH = "credentials.json"
TOKEN_PATH = "token.json"


def get_gmail_service():
    """Authenticate (using a cached token if available) and return a Gmail API client."""
    creds: Optional[Credentials] = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"{CREDENTIALS_PATH} not found. Download it from Google Cloud "
                    "Console → APIs & Services → Credentials."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def list_recent_messages(max_results: int = 10, query: str = "") -> list[dict]:
    """Return metadata (id, subject, from, snippet) for recent messages.

    query supports Gmail search syntax, e.g. "is:unread", "from:client@x.com".
    Requires only the gmail.readonly scope.
    """
    service = get_gmail_service()
    resp = (
        service.users()
        .messages()
        .list(userId="me", maxResults=max_results, q=query)
        .execute()
    )
    messages = []
    for item in resp.get("messages", []):
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=item["id"], format="metadata",
                 metadataHeaders=["Subject", "From", "Date"])
            .execute()
        )
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        messages.append({
            "id": msg["id"],
            "subject": headers.get("Subject", "(no subject)"),
            "from": headers.get("From", "unknown"),
            "date": headers.get("Date", ""),
            "snippet": msg.get("snippet", ""),
        })
    return messages


def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email. Requires the gmail.send scope to be added to SCOPES above.

    Callers in the agent should route this through GovernanceGateChecker first —
    treat any outbound email to someone outside the org as at least Tier 2.
    """
    if "https://www.googleapis.com/auth/gmail.send" not in SCOPES:
        raise PermissionError(
            "gmail.send scope not enabled. Add it to SCOPES, delete token.json, "
            "and re-authenticate before sending mail."
        )

    service = get_gmail_service()
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return service.users().messages().send(userId="me", body={"raw": raw}).execute()


if __name__ == "__main__":
    # Quick manual test: list the 5 most recent unread messages.
    for m in list_recent_messages(max_results=5, query="is:unread"):
        print(f"[{m['date']}] {m['from']} — {m['subject']}")
