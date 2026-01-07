import base64
from email.message import EmailMessage


def build_reply_message(
    *,
    to_address: str,
    subject: str,
    body: str,
    message_id: str,
    references: str | None = None,
) -> str:
    """
    Build a base64url-encoded RFC 2822 email suitable for Gmail drafts.
    """
    msg = EmailMessage()
    msg["To"] = to_address
    msg["Subject"] = subject if subject.lower().startswith("re:") else f"Re: {subject}"
    msg["In-Reply-To"] = message_id
    msg["References"] = references or message_id
    msg.set_content(body)

    raw_bytes = msg.as_bytes()
    encoded = base64.urlsafe_b64encode(raw_bytes).decode("utf-8")

    return encoded