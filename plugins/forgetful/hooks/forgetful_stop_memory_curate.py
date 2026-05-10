#!/usr/bin/env python3
"""Stop hook gate for Forgetful memory curation.

This is the readable source version of the inline hook command in hooks.json.
The hook itself is intentionally deterministic: it either stops, or asks Codex
to run the memory-curate skill in a continuation turn.
"""

from __future__ import annotations

import json
import subprocess
import sys


SKIP_MARKERS = (
    "Forgetful memory curation:",
    "No durable memory to save.",
    "Saved to memory:",
)

CURATION_PROMPT = (
    "Run $memory-curate for this completed turn. Files changed in the repo, so "
    "check whether any durable decisions, project knowledge, preferences, or "
    "implementation patterns should be saved. Only persist durable reusable "
    "knowledge with importance >= 7. Query Forgetful for duplicates before "
    "writing. Prefer updating, linking, or marking obsolete over duplicate "
    "creation. If nothing qualifies, reply exactly: Forgetful memory curation: "
    "No durable memory to save."
)


def main() -> int:
    data = json.load(sys.stdin)

    if data.get("stop_hook_active"):
        print(
            json.dumps(
                {
                    "continue": False,
                    "stopReason": "Forgetful memory curation already ran for this stop",
                }
            )
        )
        return 0

    last_message = data.get("last_assistant_message") or ""
    if any(marker in last_message for marker in SKIP_MARKERS):
        print(
            json.dumps(
                {
                    "continue": False,
                    "stopReason": "Forgetful memory curation already handled",
                }
            )
        )
        return 0

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        text=True,
        capture_output=True,
        timeout=2,
    )

    if status.returncode != 0 or not status.stdout.strip():
        print(
            json.dumps(
                {
                    "continue": False,
                    "stopReason": "No git working tree changes detected for Forgetful memory curation",
                }
            )
        )
        return 0

    print(json.dumps({"decision": "block", "reason": CURATION_PROMPT}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
