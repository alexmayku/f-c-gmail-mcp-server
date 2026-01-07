from typing import List, Dict

from googleapiclient.discovery import build

from gmail.auth import get_credentials


def list_unread_messages(max_results: int) -> List[Dict[str, str]]:
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            q="is:unread",
            maxResults=max_results,
        )
        .execute()
    )

    messages = results.get("messages", [])
    output = []

    for msg in messages:
        msg_id = msg["id"]

        full_msg = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="metadata")
            .execute()
        )

        headers = full_msg["payload"]["headers"]

        def header(name: str) -> str:
            for h in headers:
                if h["name"].lower() == name.lower():
                    return h["value"]
            return ""

        output.append(
            {
                "message_id": msg_id,
                "thread_id": full_msg["threadId"],
                "from": header("From"),
                "subject": header("Subject"),
                "snippet": full_msg.get("snippet", ""),
            }
        )

    return output

def get_message_metadata(message_id: str) -> dict:
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    message = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=["From", "Subject", "Message-Id", "References"],
        )
        .execute()
    )

    headers = {h["name"].lower(): h["value"] for h in message["payload"]["headers"]}

    return {
        "thread_id": message["threadId"],
        "from": headers.get("from", ""),
        "subject": headers.get("subject", ""),
        "message_id": headers.get("message-id", ""),
        "references": headers.get("references"),
    }

def create_draft_reply(
    *,
    thread_id: str,
    raw_message: str,
) -> dict:
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    draft = (
        service.users()
        .drafts()
        .create(
            userId="me",
            body={
                "message": {
                    "raw": raw_message,
                    "threadId": thread_id,
                }
            },
        )
        .execute()
    )

    return draft