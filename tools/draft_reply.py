from gmail.client import (
    get_message_metadata,
    create_draft_reply as create_gmail_draft,
)
from gmail.mime_builder import build_reply_message


def register_draft_reply(mcp):
    @mcp.tool()
    def create_draft_reply(message_id: str, reply_body: str) -> dict:
        """
        Create a Gmail draft reply inside the user's mailbox.
        """
        meta = get_message_metadata(message_id)

        raw_message = build_reply_message(
            to_address=meta["from"],
            subject=meta["subject"],
            body=reply_body,
            message_id=meta["message_id"],
            references=meta["references"],
        )

        draft = create_gmail_draft(
            thread_id=meta["thread_id"],
            raw_message=raw_message,
        )

        return {
            "draft_id": draft["id"],
            "thread_id": meta["thread_id"],
        }