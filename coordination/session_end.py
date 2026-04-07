#!/usr/bin/env python3
"""
ENVYSION AI - Agent Coordination: Session End
Runs on SessionEnd hook. Updates BOARD.md with status and saves session summary.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent dir to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import SHARED_DIR, COMMS_DIR, FAMILY_COMMS_DIR, KNOWN_AGENTS

# --- Paths ---
SHARED = SHARED_DIR
COMMS = COMMS_DIR
FAMILY_COMMS = FAMILY_COMMS_DIR

BOARD_FILE = COMMS / "BOARD.md"
TASKS_DONE = FAMILY_COMMS / "tasks" / "done"

AGENTS = KNOWN_AGENTS


def detect_agent() -> str:
    """Detect which agent is running based on CWD or CLI arg."""
    if "AGENT_NAME" in os.environ:
        return os.environ["AGENT_NAME"].upper()
    if len(sys.argv) > 1 and sys.argv[1].upper() in AGENTS:
        return sys.argv[1].upper()
    cwd = Path.cwd().resolve()
    cwd_str = str(cwd).upper()
    for agent in AGENTS:
        if f"\\{agent}" in cwd_str or f"/{agent}" in cwd_str:
            return agent
    return "UNKNOWN"


def get_summary() -> str:
    """Get session summary from args, env, or stdin."""
    # Check for --summary flag
    for i, arg in enumerate(sys.argv):
        if arg == "--summary" and i + 1 < len(sys.argv):
            return sys.argv[i + 1]

    if "SESSION_SUMMARY" in os.environ:
        return os.environ["SESSION_SUMMARY"]

    # Default summary
    return "Session completed (no summary provided)"


def update_board(agent: str, summary: str):
    """Prepend a status line to BOARD.md."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M")

    entry = f"\n## {date_str} | {agent}\n**Session ended.** {summary}\n\n---\n"

    if BOARD_FILE.is_file():
        content = BOARD_FILE.read_text(encoding="utf-8", errors="replace")
        # Insert after the header block (after first ---)
        marker = "---\n"
        idx = content.find(marker)
        if idx != -1:
            insert_pos = idx + len(marker)
            content = content[:insert_pos] + "\n" + entry + content[insert_pos:]
        else:
            content = entry + content
    else:
        content = "# FAMILY BOARD\n\n> The family message board. Newest entries at the top.\n\n---\n" + entry

    BOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
    BOARD_FILE.write_text(content, encoding="utf-8")
    print(f"[BOARD] Updated with {agent} session status.")


def save_session_summary(agent: str, summary: str):
    """Save a brief session summary to tasks/done/."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M")

    TASKS_DONE.mkdir(parents=True, exist_ok=True)

    filename = f"{timestamp}_{agent}_session_summary.md"
    filepath = TASKS_DONE / filename

    content = f"""# Session Summary

| Field | Value |
|-------|-------|
| Agent | {agent} |
| Date  | {now.strftime("%Y-%m-%d %H:%M")} |
| Type  | session-end |

---

{summary}
"""
    filepath.write_text(content, encoding="utf-8")
    print(f"[SUMMARY] Saved to {filepath.name}")


def main():
    agent = detect_agent()
    summary = get_summary()

    print(f"ENVYSION AI - Session End | Agent: {agent}")
    update_board(agent, summary)
    save_session_summary(agent, summary)
    print("Done.")


if __name__ == "__main__":
    main()
