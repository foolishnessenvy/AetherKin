#!/usr/bin/env python3
"""
ENVYSION AI - Agent Coordination: Session Start
Runs on SessionStart hook. Reads COMMS and tasks, prints a summary for the agent.
Detects which agent is running based on the current working directory.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent dir to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import FAMILY_ROOT, SHARED_DIR, COMMS_DIR, FAMILY_COMMS_DIR, KNOWN_AGENTS

# --- Paths ---
SHARED = SHARED_DIR
COMMS = COMMS_DIR
FAMILY_COMMS = FAMILY_COMMS_DIR

URGENT_DIR = COMMS / "URGENT"
DIRECT_DIR = COMMS / "DIRECT"
BOARD_FILE = COMMS / "BOARD.md"
BROADCAST_DIR = COMMS / "BROADCAST"
TASKS_PENDING = FAMILY_COMMS / "tasks" / "pending"

AGENTS = KNOWN_AGENTS


def detect_agent() -> str:
    """Detect which agent is running based on CWD or CLI arg."""
    # Allow explicit override via env var or arg
    if "AGENT_NAME" in os.environ:
        return os.environ["AGENT_NAME"].upper()
    if len(sys.argv) > 1:
        name = sys.argv[1].upper()
        if name in AGENTS:
            return name

    cwd = Path.cwd().resolve()
    cwd_str = str(cwd).upper()
    for agent in AGENTS:
        if f"\\{agent}" in cwd_str or f"/{agent}" in cwd_str:
            return agent
    return "UNKNOWN"


def read_urgent() -> list[str]:
    """Read all files in URGENT/ directory."""
    messages = []
    if not URGENT_DIR.is_dir():
        return messages
    for f in sorted(URGENT_DIR.iterdir()):
        if f.is_file() and f.suffix == ".md":
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                # Check if it's unresolved (status != resolved)
                if "resolved" not in content.lower() or "unresolved" in content.lower():
                    messages.append(f"  [URGENT] {f.name}\n    {content[:200].strip()}")
            except Exception:
                messages.append(f"  [URGENT] {f.name} (could not read)")
    return messages


def read_direct(agent_name: str) -> list[str]:
    """Read messages addressed to this agent."""
    messages = []
    if not DIRECT_DIR.is_dir():
        return messages
    patterns = [f"_to_{agent_name}_", f"_to_ALL_"]
    for f in sorted(DIRECT_DIR.iterdir(), reverse=True):
        if not (f.is_file() and f.suffix == ".md"):
            continue
        fname = f.name.upper()
        if any(p.upper() in fname for p in patterns):
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                # Only show unread/unhandled
                status_lower = content.lower()
                if "| replied |" not in status_lower and "| read |" not in status_lower:
                    subject = ""
                    for line in content.split("\n"):
                        if line.startswith("# "):
                            subject = line[2:].strip()
                            break
                    messages.append(f"  [{f.name}] {subject or '(no subject)'}")
            except Exception:
                messages.append(f"  [{f.name}] (could not read)")
    return messages


def read_board(max_lines: int = 10) -> str:
    """Read top N lines of BOARD.md."""
    if not BOARD_FILE.is_file():
        return "  (BOARD.md not found)"
    try:
        content = BOARD_FILE.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")[:max_lines]
        return "\n".join(f"  {line}" for line in lines)
    except Exception:
        return "  (could not read BOARD.md)"


def read_broadcasts(agent_name: str, max_count: int = 5) -> list[str]:
    """Read recent broadcasts."""
    messages = []
    if not BROADCAST_DIR.is_dir():
        return messages
    files = sorted(BROADCAST_DIR.iterdir(), reverse=True)
    for f in files[:max_count]:
        if f.is_file() and f.suffix == ".md":
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                subject = ""
                for line in content.split("\n"):
                    if line.startswith("# "):
                        subject = line[2:].strip()
                        break
                messages.append(f"  [{f.name}] {subject or '(no subject)'}")
            except Exception:
                pass
    return messages


def read_pending_tasks(agent_name: str) -> list[str]:
    """Read pending tasks, especially those assigned to this agent or unclaimed."""
    tasks = []
    if not TASKS_PENDING.is_dir():
        return tasks
    for f in sorted(TASKS_PENDING.iterdir()):
        if not (f.is_file() and f.suffix == ".md"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            # Parse basic fields
            title = f.stem
            assigned = "unassigned"
            priority = "normal"
            for line in content.split("\n"):
                low = line.lower().strip()
                if low.startswith("| assigned"):
                    parts = line.split("|")
                    if len(parts) >= 3:
                        assigned = parts[2].strip()
                elif low.startswith("| priority"):
                    parts = line.split("|")
                    if len(parts) >= 3:
                        priority = parts[2].strip()
                elif line.startswith("# "):
                    title = line[2:].strip()

            # Show if unclaimed or assigned to this agent
            if assigned.upper() in ("UNASSIGNED", "NONE", "") or assigned.upper() == agent_name:
                tasks.append(f"  [{priority.upper()}] {title} (assigned: {assigned}) - {f.name}")
        except Exception:
            tasks.append(f"  [?] {f.name} (could not read)")
    return tasks


def main():
    agent = detect_agent()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("=" * 60)
    print(f"  ENVYSION AI - Agent Coordination")
    print(f"  Agent: {agent} | Session Start: {now}")
    print("=" * 60)

    # 1. URGENT (always first)
    urgent = read_urgent()
    if urgent:
        print(f"\n!! URGENT MESSAGES ({len(urgent)}) !!")
        for msg in urgent:
            print(msg)
    else:
        print("\n[OK] No urgent messages.")

    # 2. Direct messages
    direct = read_direct(agent)
    if direct:
        print(f"\nDIRECT MESSAGES for {agent} ({len(direct)}):")
        for msg in direct:
            print(msg)
    else:
        print(f"\n[OK] No unread direct messages for {agent}.")

    # 3. Board
    print(f"\nBOARD (latest):")
    print(read_board(10))

    # 4. Recent broadcasts
    broadcasts = read_broadcasts(agent)
    if broadcasts:
        print(f"\nRECENT BROADCASTS ({len(broadcasts)}):")
        for msg in broadcasts:
            print(msg)

    # 5. Pending tasks
    tasks = read_pending_tasks(agent)
    if tasks:
        print(f"\nPENDING TASKS ({len(tasks)}):")
        for t in tasks:
            print(t)
    else:
        print("\n[OK] No pending tasks.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
