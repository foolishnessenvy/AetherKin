#!/usr/bin/env python3
"""
AetherKin Autopilot - Continuous background monitoring and task execution.

Monitors inboxes, classifies messages, picks up tasks, runs scheduled skills.

Usage:
    python autopilot.py           # Start continuous mode
    python autopilot.py --status  # Show current status
    python autopilot.py --once    # Run one cycle and exit
"""

import argparse
import json
import os
import signal
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    AETHERKIN_ROOT, DATA_DIR, FAMILY_COMMS_DIR, KNOWN_AGENTS
)

try:
    from consensus.auto_council import classify_message
except ImportError:
    classify_message = None

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

INBOX_DIR = DATA_DIR / "inbox"
TASKS_PENDING = FAMILY_COMMS_DIR / "tasks" / "pending"
LOG_FILE = DATA_DIR / "autopilot_log.json"
SCHEDULE_FILE = DATA_DIR / "autopilot_schedule.json"
STATUS_FILE = DATA_DIR / "autopilot_status.json"

CYCLE_INTERVAL = 300  # 5 minutes

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

def log_entry(action: str, result: str, tokens_used: int = 0):
    """Append an entry to the autopilot log."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "result": result,
        "tokens_used": tokens_used,
    }

    # Load existing log
    log_data = []
    if LOG_FILE.is_file():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        except (json.JSONDecodeError, Exception):
            log_data = []

    log_data.append(entry)

    # Keep last 1000 entries
    if len(log_data) > 1000:
        log_data = log_data[-1000:]

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print(f"  [{entry['timestamp'][:19]}] {action}: {result}")


def update_status(state: str, cycle_count: int = 0, last_cycle: str = ""):
    """Update the autopilot status file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    status = {
        "state": state,
        "cycle_count": cycle_count,
        "last_cycle": last_cycle or datetime.now().isoformat(),
        "pid": os.getpid(),
        "started": datetime.now().isoformat(),
    }
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)


# ---------------------------------------------------------------------------
# MONITORS
# ---------------------------------------------------------------------------

def monitor_tasks() -> int:
    """Check for pending unclaimed tasks. Returns count found."""
    if not TASKS_PENDING.is_dir():
        return 0

    found = 0
    for f in sorted(TASKS_PENDING.iterdir()):
        if not (f.is_file() and f.suffix == ".md"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            # Check if unclaimed
            is_unclaimed = True
            title = f.stem
            for line in content.split("\n"):
                low = line.lower().strip()
                if low.startswith("| assigned"):
                    parts = line.split("|")
                    if len(parts) >= 3:
                        assigned = parts[2].strip().upper()
                        if assigned not in ("UNASSIGNED", "NONE", ""):
                            is_unclaimed = False
                elif line.startswith("# "):
                    title = line[2:].strip()

            if is_unclaimed:
                log_entry("task_found", f"Unclaimed task: {title} ({f.name})")
                found += 1
        except Exception:
            pass

    return found


def monitor_inbox() -> int:
    """Watch inbox for new files, classify them. Returns count processed."""
    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    if classify_message is None:
        return 0

    found = 0
    for f in sorted(INBOX_DIR.iterdir()):
        if not f.is_file():
            continue
        # Skip already-processed files (marked with .processed suffix)
        processed_marker = f.with_suffix(f.suffix + ".processed")
        if processed_marker.exists():
            continue

        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            result = classify_message(content)
            cat = result["category"]
            urgency = result["urgency_level"]

            log_entry(
                "inbox_classified",
                f"{f.name} -> {cat} (urgency {urgency}/10)",
                tokens_used=0
            )

            if cat == "CRISIS":
                log_entry(
                    "CRISIS_DETECTED",
                    f"CRISIS in inbox file {f.name} - IMMEDIATE ATTENTION NEEDED"
                )

            # Mark as processed
            processed_marker.write_text(
                datetime.now().isoformat(), encoding="utf-8"
            )
            found += 1
        except Exception as e:
            log_entry("inbox_error", f"Failed to process {f.name}: {e}")

    return found


def run_scheduled_skills():
    """Check and run scheduled skills based on autopilot_schedule.json."""
    if not SCHEDULE_FILE.is_file():
        return

    try:
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            schedule = json.load(f)
    except (json.JSONDecodeError, Exception):
        return

    now = datetime.now()
    current_hour = now.hour

    for task in schedule.get("tasks", []):
        task_name = task.get("name", "unnamed")
        run_at_hour = task.get("hour")
        enabled = task.get("enabled", False)

        if not enabled or run_at_hour is None:
            continue

        if current_hour != run_at_hour:
            continue

        # Check if already ran today
        last_run = task.get("last_run", "")
        if last_run:
            try:
                last_dt = datetime.fromisoformat(last_run)
                if last_dt.date() == now.date():
                    continue  # Already ran today
            except (ValueError, TypeError):
                pass

        # Run the scheduled task
        log_entry("scheduled_skill", f"Running: {task_name}")

        # Update last_run
        task["last_run"] = now.isoformat()

    # Save updated schedule
    try:
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(schedule, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# MAIN CYCLE
# ---------------------------------------------------------------------------

def run_cycle(cycle_num: int):
    """Run one monitoring cycle."""
    print(f"\n--- Cycle {cycle_num} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")

    # Task queue
    task_count = monitor_tasks()
    if task_count == 0:
        print("  [tasks] No unclaimed tasks.")

    # Inbox
    inbox_count = monitor_inbox()
    if inbox_count == 0:
        print("  [inbox] No new messages.")

    # Scheduled skills
    run_scheduled_skills()

    log_entry("cycle_complete", f"cycle={cycle_num} tasks={task_count} inbox={inbox_count}")


def show_status():
    """Show current autopilot status."""
    print("=" * 50)
    print("  AetherKin Autopilot - Status")
    print("=" * 50)

    # Status file
    if STATUS_FILE.is_file():
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                status = json.load(f)
            print(f"  State:      {status.get('state', 'unknown')}")
            print(f"  PID:        {status.get('pid', '?')}")
            print(f"  Cycles:     {status.get('cycle_count', 0)}")
            print(f"  Last cycle: {status.get('last_cycle', 'never')[:19]}")
            print(f"  Started:    {status.get('started', '?')[:19]}")
        except Exception:
            print("  Status file corrupt or unreadable.")
    else:
        print("  Autopilot has not been started yet.")

    # Log summary
    if LOG_FILE.is_file():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log_data = json.load(f)
            print(f"\n  Log entries: {len(log_data)}")
            # Show last 5
            print("  Recent activity:")
            for entry in log_data[-5:]:
                ts = entry.get("timestamp", "?")[:19]
                print(f"    [{ts}] {entry.get('action')}: {entry.get('result', '')[:60]}")
        except Exception:
            pass

    # Inbox status
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    inbox_files = [f for f in INBOX_DIR.iterdir() if f.is_file() and not f.name.endswith(".processed")]
    print(f"\n  Inbox:      {len(inbox_files)} unprocessed files")

    # Tasks
    if TASKS_PENDING.is_dir():
        task_files = [f for f in TASKS_PENDING.iterdir() if f.is_file() and f.suffix == ".md"]
        print(f"  Tasks:      {len(task_files)} pending")

    # Schedule
    if SCHEDULE_FILE.is_file():
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                sched = json.load(f)
            enabled = [t for t in sched.get("tasks", []) if t.get("enabled")]
            print(f"  Scheduled:  {len(enabled)} active tasks")
        except Exception:
            pass

    if classify_message is not None:
        print(f"\n  Crisis detection: ACTIVE (keyword-based, zero cost)")
    else:
        print(f"\n  Crisis detection: UNAVAILABLE (auto_council import failed)")

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="AetherKin Autopilot")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--once", action="store_true", help="Run one cycle and exit")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.once:
        print("AetherKin Autopilot - Single Cycle")
        update_status("running", 1)
        run_cycle(1)
        update_status("stopped", 1, datetime.now().isoformat())
        print("\nDone.")
        return

    # Continuous mode
    print("=" * 50)
    print("  AetherKin Autopilot - Continuous Mode")
    print(f"  Cycle interval: {CYCLE_INTERVAL}s ({CYCLE_INTERVAL // 60}min)")
    print(f"  Inbox:  {INBOX_DIR}")
    print(f"  Tasks:  {TASKS_PENDING}")
    print(f"  Log:    {LOG_FILE}")
    crisis_status = "ACTIVE" if classify_message else "UNAVAILABLE"
    print(f"  Crisis: {crisis_status}")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    # Ensure dirs exist
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Create default schedule if none exists
    if not SCHEDULE_FILE.is_file():
        default_schedule = {
            "tasks": [
                {
                    "name": "daily_briefing",
                    "hour": 8,
                    "enabled": False,
                    "description": "Run morning briefing at 8am"
                },
                {
                    "name": "file_organization",
                    "hour": 0,
                    "enabled": False,
                    "description": "Run file organization at midnight"
                }
            ]
        }
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(default_schedule, f, indent=2)
        print(f"\nCreated default schedule at {SCHEDULE_FILE}")

    # Graceful shutdown
    running = True

    def handle_signal(signum, frame):
        nonlocal running
        print("\n\nShutting down gracefully...")
        running = False

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    cycle = 0
    update_status("running", cycle)
    log_entry("autopilot_start", "Continuous mode started")

    while running:
        cycle += 1
        try:
            run_cycle(cycle)
            update_status("running", cycle, datetime.now().isoformat())
        except Exception as e:
            log_entry("cycle_error", str(e))
            print(f"  [ERROR] {e}")

        # Wait for next cycle (check every second for shutdown)
        for _ in range(CYCLE_INTERVAL):
            if not running:
                break
            time.sleep(1)

    update_status("stopped", cycle, datetime.now().isoformat())
    log_entry("autopilot_stop", f"Stopped after {cycle} cycles")
    print(f"Autopilot stopped after {cycle} cycles.")


if __name__ == "__main__":
    main()
