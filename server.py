from typing import List, Dict

from mcp.server.fastmcp import FastMCP
from gmail.client import list_unread_messages

mcp = FastMCP("gmail-mcp-server")


@mcp.tool()
def get_unread_emails(max_results: int = 5) -> List[Dict[str, str]]:
    """
    Return a list of unread emails from Gmail.
    """
    return list_unread_messages(max_results)


if __name__ == "__main__":
    mcp.run()