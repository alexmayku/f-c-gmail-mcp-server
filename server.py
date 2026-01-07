from typing import List, Dict

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("gmail-mcp-server")


@mcp.tool()
def get_unread_emails(max_results: int = 5) -> List[Dict[str, str]]:
    """
    Return a list of unread emails.

    This is a mock implementation used to validate MCP tool wiring.
    """
    mock_emails = [
        {
            "message_id": "msg_123",
            "thread_id": "thread_abc",
            "from": "alice@example.com",
            "subject": "Project update",
            "snippet": "Here’s a quick update on the project...",
        },
        {
            "message_id": "msg_456",
            "thread_id": "thread_def",
            "from": "bob@example.com",
            "subject": "Meeting tomorrow",
            "snippet": "Are we still on for tomorrow?",
        },
    ]

    return mock_emails[:max_results]


if __name__ == "__main__":
    mcp.run()