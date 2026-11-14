#!/usr/bin/env python3
"""One-time Mixamo login. Opens a visible Brave window with the dedicated profile.

Log in yourself in that window. This script never touches credentials; it only
waits until Mixamo shows a logged-in page, then closes the browser. The session
stays in the profile, so mcp_server.py (headless) is logged in afterwards.
"""
import sys
import time

import browser
from screens.auth import is_logged_in


def main() -> int:
    page = browser._launch(headless=False)
    try:
        page.goto(browser.MIXAMO_URL, wait_until="domcontentloaded")
        print("Log in to Mixamo in the Brave window. Waiting", end="", flush=True)
        while True:
            if page.is_closed():
                print("\nWindow closed before login finished. Session not saved.")
                return 1
            try:
                if is_logged_in(page.evaluate("window.location.href"), page.content()):
                    print("\nLogged in. Session saved.")
                    return 0
            except Exception:
                pass  # page is mid-navigation or closing; the next tick decides
            time.sleep(1)
            print(".", end="", flush=True)
    finally:
        browser._close()


if __name__ == "__main__":
    sys.exit(main())
