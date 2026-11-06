"""Official MCP v2 stdio server exposing scoped Video AI Editor operations.

No network listener, hosted API, tokens or uploads are enabled by this module.
"""
from __future__ import annotations

from mcp.server import MCPServer

from mcp_server import bridge

mcp = MCPServer("Video AI Editor")


@mcp.tool()
def project_status() -> dict:
    """Read approved English production defaults, characters and current voices."""
    return bridge.project_status()


@mcp.tool()
def list_production_skills() -> dict:
    """List 21 real modular project skills and their repository paths."""
    return bridge.list_skills()


@mcp.tool()
def verify_character_assets() -> dict:
    """Run the existing approved 13-PNG SHA-256 and pixel asset verifier."""
    return bridge.verify_character_assets()


@mcp.tool()
def validate_current_edit(check_media: bool = True) -> dict:
    """Validate ExampleEdit JSON and, by default, referenced physical media."""
    return bridge.validate_edit(media=check_media)


@mcp.tool()
def inspect_local_media(relative_path: str) -> dict:
    """FFprobe an actual safe local video/audio file within input/, out/ or public/."""
    return bridge.inspect_media(relative_path)


@mcp.tool()
def render_approved_preview(confirmed: bool = False) -> dict:
    """Render a local 30-frame Remotion proof only after explicit CPU/disk approval."""
    return bridge.preview_render(confirmed=confirmed)


@mcp.tool()
def inspect_approved_video_url(url: str, approved_network: bool = False) -> dict:
    """Request restricted yt-dlp metadata only after approval; no video download."""
    return bridge.inspect_online_source(url, approved_network=approved_network)


@mcp.resource("video-ai://production-policy")
def production_policy() -> str:
    """Current authoritative production policy, not an obsolete demo profile."""
    return (bridge.ROOT / "docs/PRODUCTION_POLICY.md").read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()  # Local stdio only. HTTP deployment is not enabled.
