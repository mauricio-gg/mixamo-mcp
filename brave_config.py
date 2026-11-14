"""Shared Brave launch settings for browser.py (CLI) and mcp_server.py.

MIXAMO_BRAVE_PATH  overrides the Brave binary.
MIXAMO_PROFILE_DIR overrides the dedicated profile folder (never use your real Brave profile).
"""
import os
from pathlib import Path

DEFAULT_BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
DEFAULT_PROFILE_DIR = "~/Library/Application Support/mixamo-mcp/brave-profile"


def launch_options() -> dict:
    """Keyword arguments for launch_persistent_context that start Brave with the dedicated profile."""
    brave = Path(os.environ.get("MIXAMO_BRAVE_PATH", DEFAULT_BRAVE_PATH)).expanduser()
    if not brave.is_file():
        raise FileNotFoundError(
            f"Brave not found at {brave}. Install Brave or set MIXAMO_BRAVE_PATH to its binary."
        )
    profile = Path(os.environ.get("MIXAMO_PROFILE_DIR", DEFAULT_PROFILE_DIR)).expanduser()
    profile.mkdir(parents=True, exist_ok=True)
    return {
        "user_data_dir": str(profile),
        "executable_path": str(brave),
        "args": ["--use-mock-keychain", "--password-store=basic"],
    }
