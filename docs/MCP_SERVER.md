# Video AI Editor — local MCP server / hybrid AI plugin

This repository has **21 modular agent skills** and a separate, functional
**Model Context Protocol (MCP) server**. Together they form a *hybrid* design:
skills explain how to work; the MCP server exposes bounded local operations.
A skill ZIP alone never installs executable software or grants video access.

## Scope and deployment status

- **Implemented:** official Python MCP SDK v2 on **stdio**, so the host
  launches the server as a child process. No listener, public URL, paid API,
  third-party upload or OAuth token is introduced.
- **Supported hosts:** MCP-capable local coding assistants, Claude Desktop,
  and other compatible IDE agents that can launch a Python process.
- **Not yet supported:** hosted/remote ChatGPT MCP app. That requires a
  separately deployed authenticated HTTPS endpoint, permission review,
  operational monitoring and explicit user connection in ChatGPT.
- **Source of truth:** AGENTS.md, docs/PRODUCTION_POLICY.md,
  characters/registry.json and the approved character manifest.
- **Runtime:** Python 3.11+, Node 22+ and FFmpeg/FFprobe as required by the
  invoked tool; rendering also requires npm ci and the Remotion browser.

## Install and run locally

From the repository checkout:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -r requirements-mcp.txt
npm ci
# Local interactive users must configure their MCP host to spawn this:
.venv/bin/python scripts/run-mcp-server.py
```

The last process is deliberately silent on stdout, which MCP reserves for
protocol messages. It normally waits for a client. **Do not** install or
launch the server on an untrusted machine; local stdio servers inherit the
permissions of the process that starts them.

### Configure a desktop MCP client

In a client configuration that supports the standard `mcpServers` key
(e.g., Claude Desktop), insert this object with your actual **absolute**
workspace path. Do not commit the resulting user-specific config or secrets:

```json
{
  "mcpServers": {
    "video-ai-editor": {
      "command": "/ABSOLUTE/PATH/video-ai-editor/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/video-ai-editor/scripts/run-mcp-server.py"
      ]
    }
  }
}
```

The checked-in [example](../examples/video-ai-editor.mcp.json) uses exactly
this placeholder format. The launcher resolves the checkout root from its
own location, so it does not require the client's current working directory.

For Codex-style TOML MCP configuration where supported:

```toml
[mcp_servers.video_ai_editor]
command = "/ABSOLUTE/PATH/video-ai-editor/.venv/bin/python"
args = ["/ABSOLUTE/PATH/video-ai-editor/scripts/run-mcp-server.py"]
```

You must **enable/connect** the server from the host's own settings. Changing
a GitHub repo or a server config example does not install it in ChatGPT.

## Exposed tools

| MCP tool | Operations and bounds |
| --- | --- |
| `project_status` | Read active English/16:9/character voice defaults from the registry; **no render** |
| `list_production_skills` | Report real paths for 21 project skills; **no file modifications** |
| `verify_character_assets` | Run existing 13-pose PNG/hash checker; read-only, bounded |
| `validate_current_edit` | Validate `src/edit/edit.json` and optionally physical media via existing scripts |
| `inspect_local_media` | FFprobe a local file under `input/`, `public/` or `out/`; no remote protocols, 1 GiB input bound |
| `render_approved_preview` | **Explicit approval required**; encode 30 frames of `PixelProductionProof`, at quarter scale and concurrency 2, into ignored `out/mcp/`; not an episode |
| `inspect_approved_video_url` | **Explicit approval required**; limited yt-dlp metadata request, no source download |

The server also provides a `video-ai://production-policy` read-only
resource containing the current project policy.

## Guardrails and limits

- An approved Boolean in a tool call is a *request parameter*, not proof the
  human gave consent: **configure the MCP host to ask the owner before every
  network or render invocation**. Do not set blanket auto-approval.
- The core bridge uses constant command arguments, subprocess timeouts,
  no `shell=True`, sanitized failure messages, and a minimal child-process
  environment that omits known provider secrets and GitHub credentials.
- Local-media paths are checked against the repo root and specific ignored/
  reviewable media directories. They cannot be arbitrary host filesystem paths.
- No default tools synthesize voice, use Groq, call paid/cloud rendering,
  publish videos, modify GitHub, merge PRs or perform yt-dlp downloads.
  The separate media ingestion CLI still requires licensed use.
- Studio, real lip-sync, full narrated episodes and audiovisual quality still
  need their own media inputs, human approval and actual QA.
- **Security boundary:** stdio is not an operating-system sandbox.
  Run the server as a regular user with limited filesystem permissions. Do
  not expose the stdio process over a reverse proxy or public internet.

## Tests and proof

The normal repository Python test suite covers the bridge without installing
the SDK. The focused GitHub Actions workflow additionally installs the
pinned SDK and uses its **real in-process client** to call registered MCP
tools, proving protocol registration and structured replies:

```bash
python3 -m unittest discover -s tests -p 'test_mcp_bridge.py' -v
.venv/bin/python tests/mcp_protocol_smoke.py
```

The smoke test intentionally performs no external request, media upload,
video render, or download. A successful in-memory protocol test does not
replace an installed MCP host or finished video.

Source: [official MCP SDK](https://github.com/modelcontextprotocol/python-sdk),
[Python MCP v2 documentation](https://py.sdk.modelcontextprotocol.io/).
