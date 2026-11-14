# mixamo-mcp

A Playwright-based automation tool for [Mixamo](https://www.mixamo.com), with both a CLI operator and an MCP server for Claude Code integration.

## Features

- Browse and search animations
- Upload custom characters (FBX / OBJ / ZIP) via Auto-Rigger
- Set animation parameters (inplace, mirror, overdrive, arm-space, trim)
- Download animations with your character (FBX for Unity/Unreal, Collada)
- Persistent browser session — log in once, stays logged in
- MCP server so Claude Code can drive everything as tools

## Setup

Requires the [Brave](https://brave.com) browser (macOS). Playwright drives the installed Brave; no Chromium download is needed.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Configuration (environment variables, both optional):

| Variable | Default |
|---|---|
| `MIXAMO_BRAVE_PATH` | `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser` |
| `MIXAMO_PROFILE_DIR` | `~/Library/Application Support/mixamo-mcp/brave-profile` |

The profile is a dedicated folder for this tool. Never point it at your real Brave profile.

### One-time login

```bash
.venv/bin/python login.py
```

A visible Brave window opens on mixamo.com. Log in yourself; the script never handles credentials. When it detects the login it prints that the session is saved and exits. If you close the window first it exits with an error. The MCP server then runs headless with the same profile.

## CLI usage

```bash
.venv/bin/python main.py
```

Available commands:

| Command | Description |
|---|---|
| `list [query]` | List animations, optionally filtered by query |
| `select <id>` | Select animation by ID |
| `set inplace true/false` | Toggle in-place mode |
| `set mirror true/false` | Toggle mirror |
| `set overdrive <0-100>` | Set overdrive slider |
| `upload <path>` | Upload a character file |
| `download <path>` | Download current animation |
| `status` | Show current screen and animation info |
| `quit` | Exit |

## MCP server (Claude Code)

The MCP server lets Claude Code control Mixamo directly as tools.

### Configure

Add to your `.mcp.json`, with your own paths:

```json
{
  "mcpServers": {
    "mixamo": {
      "command": "/path/to/mixamo-mcp/.venv/bin/python",
      "args": ["/path/to/mixamo-mcp/mcp_server.py"]
    }
  }
}
```

### Available tools

| Tool | Description |
|---|---|
| `status()` | Current screen, character, animation, params |
| `list_animations(query)` | Search animations |
| `select_animation(id)` | Select animation by ID |
| `set_param(name, value)` | Set inplace / mirror / overdrive / arm-space / trim |
| `upload_character(path)` | Upload character to Auto-Rigger |
| `download_animation(path, format, skin, fps)` | Download animation |
| `confirm_review()` | Confirm Auto-Rigger review step |
| `close_upload_modal()` | Dismiss upload modal |

### Download formats

| Key | Format |
|---|---|
| `fbx_unity` | FBX for Unity (default) |
| `fbx` | FBX 2019 |
| `fbx_ascii` | FBX 2019 ASCII |
| `fbx_7.4` | FBX 2014 |
| `fbx_6.1` | FBX 6.1 |
| `collada` | Collada (.dae) |

## Notes

- Do not run `main.py` and `mcp_server.py` at the same time — both use the same browser profile
- Log in once with `login.py`; the session is saved in the dedicated Brave profile (see `MIXAMO_PROFILE_DIR`)
