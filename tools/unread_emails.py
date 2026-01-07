from typing import Dict, List
from gmail.client import list_unread_messages


def register_unread_emails(mcp):
    @mcp.tool()
    def get_unread_emails(max_results: int = 5) -> List[Dict[str, str]]:
        """
        Return a list of unread emails from Gmail.
        """
        if max_results < 1:
            return []
        if max_results > 50:
            max_results = 50

        return list_unread_messages(max_results)