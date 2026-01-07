from __future__ import annotations

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes needed for this project:
# - gmail.readonly: read messages
# - gmail.compose: create drafts
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SECRETS_DIR = PROJECT_ROOT / "secrets"
CLIENT_SECRET_FILE = SECRETS_DIR / "client_secret.json"
TOKEN_FILE = SECRETS_DIR / "token.json"


def main() -> None:
    # 1) Sanity checks
    if not CLIENT_SECRET_FILE.exists():
        raise FileNotFoundError(
            f"Missing OAuth client file at {CLIENT_SECRET_FILE}\n"
            "Put your downloaded Google OAuth client JSON at secrets/client_secret.json"
        )

    SECRETS_DIR.mkdir(parents=True, exist_ok=True)

    # 2) Load existing token.json if present
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # 3) If no valid creds, do local browser OAuth once
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh silently if we have a refresh token
            creds.refresh(Request())
        else:
            # This starts a temporary local server and opens the browser for consent
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE),
                scopes=SCOPES,
            )
            creds = flow.run_local_server(port=0)

        # 4) Save token.json for reuse
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    # 5) Smoke test. Call Gmail API and print something definitive
    service = build("gmail", "v1", credentials=creds)

    profile = service.users().getProfile(userId="me").execute()
    email_address = profile.get("emailAddress", "(unknown)")

    # List a few unread messages to prove scope and API access
    results = (
        service.users()
        .messages()
        .list(userId="me", q="is:unread", maxResults=5)
        .execute()
    )
    messages = results.get("messages", [])

    print("OAuth success.")
    print(f"Authenticated as: {email_address}")
    print(f"Token saved to: {TOKEN_FILE}")
    print(f"Unread messages found (showing up to 5 IDs): {len(messages)}")
    for m in messages:
        print(f"- messageId={m.get('id')} threadId={m.get('threadId')}")


if __name__ == "__main__":
    main()