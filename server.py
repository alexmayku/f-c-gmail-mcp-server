from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("gmail-mcp-server")

# Register tools
from tools.unread_emails import register_unread_emails
from tools.draft_reply import register_draft_reply

register_unread_emails(mcp)
register_draft_reply(mcp)

if __name__ == "__main__":
    mcp.run()