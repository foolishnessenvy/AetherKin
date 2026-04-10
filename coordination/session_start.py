#!/usr/bin/env python3
"""
AetherKin - Agent Coordination: Session Start
Runs on SessionStart hook. Reads COMMS and tasks, prints a summary for the agent.
Detects which agent is running based on the current working directory.
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent dir to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import FAMILY_ROOT, SHARED_DIR, COMMS_DIR, FAMILY_COMMS_DIR, KNOWN_AGENTS

try:
    from consensus.auto_council import classify_message
except ImportError:
    classify_message = None

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


def scan_direct_messages_for_crisis(agent: str):
    """Read recent direct messages and classify them for crisis/emotional content."""
    if classify_message is None:
        return

    if not DIRECT_DIR.is_dir():
        return

    patterns = [f"_to_{agent}_", f"_to_ALL_"]
    scanned = 0
    crisis_alerts = []
    emotional_alerts = []

    for f in sorted(DIRECT_DIR.iterdir(), reverse=True):
        if scanned >= 10:
            break
        if not (f.is_file() and f.suffix == ".md"):
            continue
        fname = f.name.upper()
        if not any(p.upper() in fname for p in patterns):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            # Extract body text (skip metadata table)
            body_lines = []
            past_table = False
            for line in content.split("\n"):
                if past_table:
                    body_lines.append(line)
                elif line.strip() == "---":
                    past_table = True
            body = "\n".join(body_lines).strip() or content[:500]

            result = classify_message(body)
            cat = result["category"]

            if cat == "CRISIS":
                crisis_alerts.append((f.name, result))
            elif cat == "EMOTIONAL":
                emotional_alerts.append((f.name, result))
            scanned += 1
        except Exception:
            pass

    if crisis_alerts:
        print()
        print("!" * 60)
        print("  CRISIS DETECTED IN MESSAGES")
        print("  IMMEDIATE ATTENTION REQUIRED")
        print("!" * 60)
        for fname, result in crisis_alerts:
            print(f"  [{fname}] urgency={result['urgency_level']}/10")
            print(f"    Categories matched: {result['matched_categories']}")
        print()

    if emotional_alerts:
        print()
        print("  [NOTE] Elevated emotional content detected:")
        for fname, result in emotional_alerts:
            print(f"    [{fname}] urgency={result['urgency_level']}/10")
        print("  Consider empathetic engagement with these messages.")
        print()


def main():
    # Parse CLI args
    parser = argparse.ArgumentParser(description="AetherKin Session Start")
    parser.add_argument("agent_name", nargs="?", default=None,
                        help="Agent name (auto-detected if not provided)")
    parser.add_argument("--verify", action="store_true",
                        help="Enable cross-verification mode for factual claims")
    args = parser.parse_args()

    # Detect agent - use parsed arg if provided, otherwise auto-detect
    if args.agent_name and args.agent_name.upper() in AGENTS:
        agent = args.agent_name.upper()
    else:
        # Temporarily restore sys.argv for detect_agent compatibility
        agent = detect_agent()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("=" * 60)
    print(f"  AetherKin - Agent Coordination")
    print(f"  Agent: {agent} | Session Start: {now}")
    if args.verify:
        print(f"  [VERIFY MODE] Factual claims will be cross-checked")
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

    # 6. Crisis detection on recent direct messages
    print("\n--- Crisis Scan ---")
    if classify_message is not None:
        scan_direct_messages_for_crisis(agent)
        print("[OK] Message crisis scan complete.")
    else:
        print("[WARN] auto_council not available - crisis scan skipped.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
