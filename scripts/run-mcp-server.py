#!/usr/bin/env python3
"""Launch the local MCP server from anywhere without relying on a shell or CWD."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mcp_server.server import mcp  # noqa: E402

if __name__ == "__main__":
    mcp.run()
