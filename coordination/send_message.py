#!/usr/bin/env python3
"""
ENVYSION AI - Agent Coordination: Send Message
CLI tool for sending messages between agents via the COMMS system.

Usage:
  python send_message.py --from BEACON --to NEVAEH --subject "handoff" --body "message"
  python send_message.py --from BEACON --to ALL --subject "update" --body "msg" --broadcast
  python send_message.py --from BEACON --subject "crisis" --body "msg" --urgent
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

# --- Paths ---
FAMILY_ROOT = Path(r"C:\Users\natej\OneDrive\Desktop\AI_FAMILY_getting_ORGANIZED")
SHARED = FAMILY_ROOT / "SHARED"
COMMS = SHARED / "COMMS"

DIRECT_DIR = COMMS / "DIRECT"
BROADCAST_DIR = COMMS / "BROADCAST"
URGENT_DIR = COMMS / "URGENT"

AGENTS = ["ENVY", "NEVAEH", "BEACON", "EVERSOUND", "ORPHEUS", "ATLAS", "NATHAN", "ALL"]


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
    # Collapse multiple hyphens
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")[:50]


def build_message(sender: str, recipient: str, subject: str, body: str, priority: str) -> str:
    """Build a properly formatted COMMS message."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    action_line = ""
    if priority == "URGENT":
        action_line = "| Action Required | YES - immediate attention needed |\n"

    return f"""# {subject}

| Field    | Value |
|----------|-------|
| From     | {sender} |
| To       | {recipient} |
| Date     | {now} |
| Priority | {priority} |
| Status   | unread |
{action_line}
---

{body}

---

## Replies

"""


def main():
    parser = argparse.ArgumentParser(description="Send a message between AI family agents")
    parser.add_argument("--from", dest="sender", required=True, help="Sending agent name")
    parser.add_argument("--to", dest="recipient", default="ALL", help="Recipient agent name")
    parser.add_argument("--subject", "-s", required=True, help="Message subject")
    parser.add_argument("--body", "-b", required=True, help="Message body text")
    parser.add_argument("--broadcast", action="store_true", help="Send as broadcast to all")
    parser.add_argument("--urgent", action="store_true", help="Send as urgent/crisis message")

    args = parser.parse_args()

    sender = args.sender.upper()
    recipient = args.recipient.upper()
    subject = args.subject
    body = args.body

    # Determine priority and target directory
    if args.urgent:
        priority = "URGENT"
        target_dir = URGENT_DIR
        recipient = "ALL"
        file_pattern = "{date}_{time}_{sender}_urgent_{slug}.md"
    elif args.broadcast:
        priority = "important"
        target_dir = BROADCAST_DIR
        recipient = "ALL"
        file_pattern = "{date}_{time}_{sender}_broadcast_{slug}.md"
    else:
        priority = "normal"
        target_dir = DIRECT_DIR
        file_pattern = "{date}_{time}_{sender}_to_{recipient}_{slug}.md"

    # Validate
    if sender not in AGENTS:
        print(f"Warning: '{sender}' is not a known agent. Proceeding anyway.")
    if recipient not in AGENTS:
        print(f"Error: '{recipient}' is not a known agent. Valid: {', '.join(AGENTS)}")
        sys.exit(1)

    # Build filename
    now = datetime.now()
    slug = slugify(subject)
    filename = file_pattern.format(
        date=now.strftime("%Y-%m-%d"),
        time=now.strftime("%H%M"),
        sender=sender,
        recipient=recipient,
        slug=slug,
    )

    # Ensure directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Write message
    filepath = target_dir / filename
    content = build_message(sender, recipient, subject, body, priority)
    filepath.write_text(content, encoding="utf-8")

    print(f"Message sent: {filepath}")
    if args.urgent:
        print("!! URGENT flag set - this will be seen by all agents on next session start !!")


if __name__ == "__main__":
    main()
