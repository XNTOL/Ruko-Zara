#!/usr/bin/env python3
"""Wake a sleeping free host before a demo or recording (ARCHITECTURE §12).

Usage:
  python scripts/warmup.py
  python scripts/warmup.py https://your-app.onrender.com
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request


def main() -> int:
    base = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")
    url = f"{base}/healthz"
    print(f"Pinging {url} …")
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(f"OK {resp.status}: {body}")
            return 0 if resp.status == 200 else 1
    except urllib.error.URLError as exc:
        print(f"Failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
