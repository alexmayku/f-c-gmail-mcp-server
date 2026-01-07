from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes must match exactly what you used in Step 0.6
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SECRETS_DIR = PROJECT_ROOT / "secrets"
TOKEN_FILE = SECRETS_DIR / "token.json"


def get_credentials() -> Credentials:
    if not TOKEN_FILE.exists():
        raise RuntimeError(
            "Missing token.json. Run scripts/auth_smoke_test.py first."
        )

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return creds