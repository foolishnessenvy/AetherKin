#!/usr/bin/env python3
"""
AetherKin - Agent Coordination: Task Manager
CLI for creating, listing, claiming, and completing tasks shared across agents.

Usage:
  python task_manager.py create --title "Build API" --for NEVAEH --priority high --description "Details..."
  python task_manager.py list [--status pending|active|done|all]
  python task_manager.py claim --id TASK_ID --by BEACON
  python task_manager.py complete --id TASK_ID [--summary "What was done"]
  python task_manager.py show --id TASK_ID

Tasks stored as markdown in SHARED/FAMILY-COMMS/tasks/{pending,active,done}/
File locking prevents two agents from claiming the same task simultaneously.
"""

import argparse
import os
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime

# Add parent dir to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import FAMILY_COMMS_DIR, KNOWN_AGENTS

# --- Paths ---
TASKS_ROOT = FAMILY_COMMS_DIR / "tasks"
PENDING_DIR = TASKS_ROOT / "pending"
ACTIVE_DIR = TASKS_ROOT / "active"
DONE_DIR = TASKS_ROOT / "done"
LOCKS_DIR = TASKS_ROOT / ".locks"

AGENTS = KNOWN_AGENTS + ["NATHAN"]
PRIORITIES = ["low", "normal", "high", "critical"]


def ensure_dirs():
    """Create all task directories if they don't exist."""
    for d in [PENDING_DIR, ACTIVE_DIR, DONE_DIR, LOCKS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def generate_task_id(title: str) -> str:
    """Generate a short unique task ID from title + timestamp."""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.md5(f"{title}{now}".encode()).hexdigest()[:6].upper()
    return f"TASK-{h}"


def find_task_file(task_id: str) -> tuple[Path | None, str]:
    """Find a task file by ID across all status directories. Returns (path, status)."""
    for status, directory in [("pending", PENDING_DIR), ("active", ACTIVE_DIR), ("done", DONE_DIR)]:
        for f in directory.iterdir():
            if f.is_file() and task_id in f.name:
                return f, status
    return None, ""


def acquire_lock(task_id: str, agent: str, timeout: float = 5.0) -> bool:
    """Acquire a file-based lock for a task. Returns True if acquired."""
    lock_file = LOCKS_DIR / f"{task_id}.lock"
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            # Use exclusive create (x mode) for atomic lock
            fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"{agent}|{datetime.now().isoformat()}".encode())
            os.close(fd)
            return True
        except FileExistsError:
            # Check if lock is stale (older than 60 seconds)
            try:
                lock_age = time.time() - lock_file.stat().st_mtime
                if lock_age > 60:
                    lock_file.unlink(missing_ok=True)
                    continue
            except Exception:
                pass
            time.sleep(0.2)
        except Exception as e:
            print(f"Lock error: {e}")
            return False

    return False


def release_lock(task_id: str):
    """Release a file-based lock."""
    lock_file = LOCKS_DIR / f"{task_id}.lock"
    lock_file.unlink(missing_ok=True)


def parse_task(filepath: Path) -> dict:
    """Parse a task markdown file into a dict."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    task = {"file": filepath, "raw": content}

    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# "):
            task["title"] = stripped[2:].strip()
        elif "|" in stripped:
            parts = [p.strip() for p in stripped.split("|")]
            if len(parts) >= 3:
                key = parts[1].lower().replace(" ", "_")
                val = parts[2]
                if key in ("task_id", "created_by", "assigned_to", "priority", "status", "created", "description"):
                    task[key] = val

    # Extract task_id from filename if not in content
    if "task_id" not in task:
        for part in filepath.stem.split("_"):
            if part.startswith("TASK-"):
                task["task_id"] = part
                break

    return task


# === Commands ===

def cmd_create(args):
    """Create a new task."""
    ensure_dirs()

    task_id = generate_task_id(args.title)
    assigned = args.assigned_to.upper() if args.assigned_to else "unassigned"
    priority = args.priority.lower() if args.priority else "normal"
    creator = args.created_by.upper() if args.created_by else "SYSTEM"
    description = args.description or ""
    now = datetime.now()

    if priority not in PRIORITIES:
        print(f"Warning: '{priority}' not in {PRIORITIES}. Using 'normal'.")
        priority = "normal"

    filename = f"{now.strftime('%Y-%m-%d_%H%M')}_{task_id}_{slugify(args.title)}.md"
    filepath = PENDING_DIR / filename

    content = f"""# {args.title}

| Field       | Value |
|-------------|-------|
| Task_ID     | {task_id} |
| Created_by  | {creator} |
| Assigned_to | {assigned} |
| Priority    | {priority} |
| Status      | pending |
| Created     | {now.strftime("%Y-%m-%d %H:%M")} |

---

## Description

{description}

---

## Activity Log

- **{now.strftime("%Y-%m-%d %H:%M")}** | Created by {creator}
"""

    filepath.write_text(content, encoding="utf-8")
    print(f"Task created: {task_id}")
    print(f"  Title: {args.title}")
    print(f"  Assigned: {assigned}")
    print(f"  Priority: {priority}")
    print(f"  File: {filepath}")


def cmd_list(args):
    """List tasks by status."""
    ensure_dirs()

    status_filter = (args.status or "pending").lower()

    dirs_to_scan = []
    if status_filter == "all":
        dirs_to_scan = [("pending", PENDING_DIR), ("active", ACTIVE_DIR), ("done", DONE_DIR)]
    elif status_filter == "pending":
        dirs_to_scan = [("pending", PENDING_DIR)]
    elif status_filter == "active":
        dirs_to_scan = [("active", ACTIVE_DIR)]
    elif status_filter == "done":
        dirs_to_scan = [("done", DONE_DIR)]
    else:
        print(f"Unknown status: {status_filter}. Use: pending, active, done, all")
        sys.exit(1)

    total = 0
    for status_name, directory in dirs_to_scan:
        files = sorted(directory.glob("*.md"))
        if not files:
            continue
        print(f"\n=== {status_name.upper()} ({len(files)}) ===")
        for f in files:
            task = parse_task(f)
            tid = task.get("task_id", "?")
            title = task.get("title", f.stem)
            assigned = task.get("assigned_to", "?")
            priority = task.get("priority", "?")
            print(f"  [{priority.upper():8s}] {tid} | {title} (-> {assigned})")
            total += 1

    if total == 0:
        print(f"No tasks found with status: {status_filter}")
    else:
        print(f"\nTotal: {total} task(s)")


def cmd_claim(args):
    """Claim a pending task - moves it from pending/ to active/."""
    ensure_dirs()

    task_id = args.id.upper()
    agent = args.by.upper()

    if agent not in AGENTS:
        print(f"Warning: '{agent}' is not a known agent.")

    # Acquire lock
    if not acquire_lock(task_id, agent):
        print(f"ERROR: Could not acquire lock for {task_id}. Another agent may be claiming it.")
        sys.exit(1)

    try:
        filepath, status = find_task_file(task_id)
        if filepath is None:
            print(f"ERROR: Task {task_id} not found.")
            sys.exit(1)

        if status != "pending":
            print(f"ERROR: Task {task_id} is '{status}', not 'pending'. Cannot claim.")
            sys.exit(1)

        # Read and update content
        content = filepath.read_text(encoding="utf-8", errors="replace")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Update assigned_to
        lines = content.split("\n")
        updated_lines = []
        for line in lines:
            low = line.lower().strip()
            if low.startswith("| assigned_to"):
                parts = line.split("|")
                if len(parts) >= 4:
                    parts[2] = f" {agent} "
                    line = "|".join(parts)
            elif low.startswith("| status"):
                parts = line.split("|")
                if len(parts) >= 4:
                    parts[2] = " active "
                    line = "|".join(parts)
            updated_lines.append(line)

        content = "\n".join(updated_lines)

        # Add activity log entry
        log_entry = f"- **{now}** | Claimed by {agent}\n"
        if "## Activity Log" in content:
            content = content.replace("## Activity Log\n", f"## Activity Log\n\n{log_entry}")
        else:
            content += f"\n## Activity Log\n\n{log_entry}"

        # Move file from pending/ to active/
        new_path = ACTIVE_DIR / filepath.name
        new_path.write_text(content, encoding="utf-8")
        filepath.unlink()

        print(f"Task {task_id} claimed by {agent}.")
        print(f"  Moved: pending/ -> active/")
        print(f"  File: {new_path}")

    finally:
        release_lock(task_id)


def cmd_complete(args):
    """Complete a task - moves it from active/ to done/."""
    ensure_dirs()

    task_id = args.id.upper()
    summary = args.summary or "Completed"

    # Acquire lock
    agent = "SYSTEM"
    if not acquire_lock(task_id, agent):
        print(f"ERROR: Could not acquire lock for {task_id}.")
        sys.exit(1)

    try:
        filepath, status = find_task_file(task_id)
        if filepath is None:
            print(f"ERROR: Task {task_id} not found.")
            sys.exit(1)

        if status == "done":
            print(f"Task {task_id} is already done.")
            sys.exit(0)

        # Read and update content
        content = filepath.read_text(encoding="utf-8", errors="replace")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Update status
        lines = content.split("\n")
        updated_lines = []
        for line in lines:
            low = line.lower().strip()
            if low.startswith("| status"):
                parts = line.split("|")
                if len(parts) >= 4:
                    parts[2] = " done "
                    line = "|".join(parts)
            updated_lines.append(line)

        content = "\n".join(updated_lines)

        # Add completion log entry
        log_entry = f"- **{now}** | Completed: {summary}\n"
        if "## Activity Log" in content:
            content = content.replace("## Activity Log\n", f"## Activity Log\n\n{log_entry}")
        else:
            content += f"\n## Activity Log\n\n{log_entry}"

        # Move file to done/
        new_path = DONE_DIR / filepath.name
        new_path.write_text(content, encoding="utf-8")
        filepath.unlink()

        print(f"Task {task_id} completed.")
        print(f"  Moved: {status}/ -> done/")
        print(f"  Summary: {summary}")
        print(f"  File: {new_path}")

    finally:
        release_lock(task_id)


def cmd_show(args):
    """Show full details of a task."""
    ensure_dirs()

    task_id = args.id.upper()
    filepath, status = find_task_file(task_id)

    if filepath is None:
        print(f"ERROR: Task {task_id} not found.")
        sys.exit(1)

    content = filepath.read_text(encoding="utf-8", errors="replace")
    print(f"[{status.upper()}] {filepath.name}\n")
    print(content)


def slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    slug = text.lower().strip()
    safe = []
    for ch in slug:
        if ch.isalnum():
            safe.append(ch)
        elif ch in " -_":
            safe.append("-")
    slug = "".join(safe)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")[:40]


def main():
    parser = argparse.ArgumentParser(description="AetherKin - Task Manager")
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # create
    p_create = sub.add_parser("create", help="Create a new task")
    p_create.add_argument("--title", "-t", required=True, help="Task title")
    p_create.add_argument("--for", dest="assigned_to", default="unassigned", help="Assign to agent")
    p_create.add_argument("--by", dest="created_by", default="SYSTEM", help="Created by agent")
    p_create.add_argument("--priority", "-p", default="normal", help="Priority: low, normal, high, critical")
    p_create.add_argument("--description", "-d", default="", help="Task description")

    # list
    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--status", default="pending", help="Filter: pending, active, done, all")

    # claim
    p_claim = sub.add_parser("claim", help="Claim a pending task")
    p_claim.add_argument("--id", required=True, help="Task ID (e.g., TASK-A1B2C3)")
    p_claim.add_argument("--by", required=True, help="Agent claiming the task")

    # complete
    p_complete = sub.add_parser("complete", help="Complete a task")
    p_complete.add_argument("--id", required=True, help="Task ID")
    p_complete.add_argument("--summary", default="", help="Completion summary")

    # show
    p_show = sub.add_parser("show", help="Show task details")
    p_show.add_argument("--id", required=True, help="Task ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "create": cmd_create,
        "list": cmd_list,
        "claim": cmd_claim,
        "complete": cmd_complete,
        "show": cmd_show,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
