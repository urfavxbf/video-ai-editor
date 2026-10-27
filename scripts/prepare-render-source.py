#!/usr/bin/env python3
"""Download an authorized, temporary source file for the queued video render.

The job file contains a short-lived signed URL. This program never prints it.
Only an allowlisted media host is allowed; output paths and render presets are fixed.
"""
import argparse
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

MAX_BYTES = 299 * 1024 * 1024
ALLOWED_HOSTS = {"storage.googleapis.com"}
ALLOWED_PRESETS = {"dudut-premium"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("job_file", type=Path)
    args = parser.parse_args()
    path = args.job_file
    if not path.exists() or path.suffix != ".json" or path.parent.as_posix() != "render-queue":
        raise SystemExit("Expected a JSON job in render-queue/")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("preset") not in ALLOWED_PRESETS:
        raise SystemExit("Unsupported editing preset")
    source = data.get("source_url", "")
    parsed = urlsplit(source)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS or parsed.username or parsed.password:
        raise SystemExit("Media URL host is not allowed")
    # A single supported job writes to an untracked input location; never commit media.
    output = Path("input/50812.mp4")
    output.parent.mkdir(parents=True, exist_ok=True)
    partial = output.with_suffix(".download")
    try:
        with urlopen(Request(source, headers={"User-Agent":"VideoAIEditor/1.0"}), timeout=120) as response:
            total = 0
            with partial.open("wb") as dest:
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    total += len(block)
                    if total > MAX_BYTES:
                        raise ValueError("Input file exceeds configured size limit")
                    dest.write(block)
        if total < 100000:
            raise ValueError("Downloaded input is too small to be valid podcast footage")
        os.replace(partial, output)
    except Exception as exc:
        partial.unlink(missing_ok=True)
        # HTTP exceptions may contain the URL. Never print exception details or source tokens.
        print("Failed to fetch video file. Check that signed media URL is still valid.", file=sys.stderr)
        sys.exit(1)
    print(f"Source media staged successfully: {total / 1048576:.1f} MiB")


if __name__ == "__main__":
    main()
