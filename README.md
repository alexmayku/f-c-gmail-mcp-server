Gmail MCP Server

A local Model Context Protocol (MCP) server that allows an AI assistant (via Claude Desktop) to:
	•	Read unread emails from a Gmail account
	•	Create draft replies in Gmail, correctly threaded

This project demonstrates a complete end-to-end MCP integration with a real external API (Gmail), running locally and safely.

⸻

What this server does

The server exposes two MCP tools to Claude Desktop.

get_unread_emails

Returns unread emails from the user’s Gmail inbox.

Each item includes:
	•	message_id
	•	thread_id
	•	from
	•	subject
	•	snippet

create_draft_reply

Creates a real Gmail draft reply to an existing message.
	•	The draft appears in the correct Gmail thread
	•	The email is not sent
	•	Proper Gmail threading headers are applied

⸻

High-level architecture
	•	Language: Python
	•	Protocol: Model Context Protocol (MCP)
	•	Runtime: Local MCP server launched by Claude Desktop
	•	Email API: Gmail API (OAuth 2.0)

Flow:

Claude Desktop
→ MCP tool call
→ Local Python server
→ Gmail API
→ Draft appears in Gmail

⸻

Project structure

mcp-gmail-server/
├── server.py                # MCP server entrypoint
├── tools/
│   ├── unread_emails.py     # get_unread_emails tool
│   └── draft_reply.py       # create_draft_reply tool
├── gmail/
│   ├── auth.py              # OAuth token loading / refresh
│   ├── client.py            # Gmail API calls
│   └── mime_builder.py      # RFC 2822 email construction
├── scripts/
│   └── auth_smoke_test.py   # One-time OAuth setup script
├── config/
│   └── claude_desktop_config.example.json
├── secrets/                 # OAuth credentials and tokens (gitignored)
├── venv/
└── README.md


⸻

Prerequisites
	•	Python 3.11+
	•	A Gmail account
	•	Claude Desktop installed
	•	Google Cloud project with:
	•	Gmail API enabled
	•	OAuth 2.0 Desktop app credentials created

⸻

Setup instructions

1. Clone the repository

git clone https://github.com/alexmayku/f-c-gmail-mcp-server.git
cd f-c-gmail-mcp-server


⸻

2. Create and activate a virtual environment

python -m venv venv
source venv/bin/activate


⸻

3. Install dependencies

pip install mcp google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2


⸻

4. Set up Gmail OAuth (one time)
	1.	In Google Cloud Console:
	•	Enable Gmail API
	•	Create an OAuth 2.0 Client ID (Desktop app)
	2.	Download the OAuth client JSON
	3.	Save it as:

secrets/client_secret.json

Then run:

python scripts/auth_smoke_test.py

This will:
	•	Open a browser for consent
	•	Create secrets/token.json
	•	Verify Gmail API access

You only need to do this once.

⸻

5. Configure Claude Desktop

Copy:

config/claude_desktop_config.example.json

To Claude’s actual config location:

macOS

~/Library/Application Support/Claude/claude_desktop_config.json

Update the paths to point to:
	•	Your virtualenv Python executable
	•	Your server.py file

Example:

{
  "mcpServers": {
    "gmail": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/server.py"],
      "env": {}
    }
  }
}

Restart Claude Desktop after saving.

⸻

Using the server in Claude

Example prompt:

Read my unread emails and draft a short reply in Gmail to the most important email saying I’ll review it and get back later today.

Claude will:
	1.	Call get_unread_emails
	2.	Select a message
	3.	Call create_draft_reply
	4.	Create a real Gmail draft in the correct thread

⸻

Security notes
	•	OAuth tokens are stored locally in secrets/token.json
	•	No credentials are committed to the repository
	•	.gitignore excludes:
	•	secrets/
	•	__pycache__/
	•	virtual environment files

⸻
