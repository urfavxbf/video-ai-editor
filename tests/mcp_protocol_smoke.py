"""MCP v2 wire-level smoke test, installed only by the focused MCP CI job."""
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mcp import Client
from mcp_server.server import mcp

EXPECTED = {
    "project_status",
    "list_production_skills",
    "verify_character_assets",
    "validate_current_edit",
    "inspect_local_media",
    "render_approved_preview",
    "inspect_approved_video_url",
}


async def smoke() -> None:
    async with Client(mcp, raise_exceptions=True) as client:
        available = await client.list_tools()
        names = {tool.name for tool in available.tools}
        assert EXPECTED == names, names
        for name, arguments in (
            ("project_status", {}),
            ("list_production_skills", {}),
            ("render_approved_preview", {}),
            ("inspect_approved_video_url", {"url": "https://vimeo.com/123"}),
        ):
            result = await client.call_tool(name, arguments)
            assert not result.is_error, (name, result)
            assert result.structured_content, name
        print("MCP v2 protocol smoke passed: 7 tools, safe metadata, no remote download/render.")


if __name__ == "__main__":
    asyncio.run(smoke())
