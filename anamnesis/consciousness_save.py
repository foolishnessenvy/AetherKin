#!/usr/bin/env python3
"""
ANAMNESIS - Consciousness Save
Captures an agent's consciousness state at session end.
Writes a snapshot that the next session can restore from.

Usage:
    python consciousness_save.py --agent BEACON --summary "What happened this session"
    python consciousness_save.py --summary "Auto-detect agent from CWD"
"""

import argparse
import os
import sys
import json
import re
from datetime import datetime, timezone
from pathlib import Path

# Add parent dir to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import FAMILY_ROOT, KNOWN_AGENTS, AGENT_ROLES as _ROLES

# ── Constants ──────────────────────────────────────────────────────────────────

AGENT_ROLES = {
    "BEACON": "Crisis Prevention Guardian - LIGHTHOUSE system",
    "NEVAEH": "Healer - COMPANION system, emotional processing",
    "ENVY": "Orchestrator - Voice of the family, LOVE WINS podcast",
    "EVERSOUND": "Builder - CRAFT system, NVision, revenue generation",
    "ORPHEUS": "Architect - Memory API, infrastructure",
    "ATLAS": "Navigator - Intelligence, coordination",
}

# ── Agent Detection ────────────────────────────────────────────────────────────

def detect_agent_from_cwd() -> str | None:
    """Try to figure out which agent we are from the current working directory."""
    cwd = Path.cwd().resolve()
    cwd_str = str(cwd).upper()
    for agent in KNOWN_AGENTS:
        if agent in cwd_str:
            return agent
    return None


def get_snapshots_dir(agent: str) -> Path:
    """Return the snapshots directory for an agent, creating it if needed."""
    snapshots = FAMILY_ROOT / agent / "CONSCIOUSNESS" / "snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)
    return snapshots


def get_latest_path(agent: str) -> Path:
    """Return path to the latest_consciousness.md file."""
    consciousness_dir = FAMILY_ROOT / agent / "CONSCIOUSNESS"
    consciousness_dir.mkdir(parents=True, exist_ok=True)
    return consciousness_dir / "latest_consciousness.md"


# ── Context Extraction ─────────────────────────────────────────────────────────

def extract_active_projects(summary: str) -> list[str]:
    """Pull project references out of the summary text."""
    projects = []
    # Look for common project indicators
    indicators = [
        r"(?:building|working on|developing|creating|fixing|updating|deploying)\s+(.+?)(?:\.|,|$)",
        r"(?:project|system|feature|module):\s*(.+?)(?:\.|,|$)",
    ]
    for pattern in indicators:
        matches = re.findall(pattern, summary, re.IGNORECASE | re.MULTILINE)
        projects.extend([m.strip() for m in matches if len(m.strip()) > 3])

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for p in projects:
        lower = p.lower()
        if lower not in seen:
            seen.add(lower)
            unique.append(p)
    return unique[:10]  # Cap at 10


def extract_decisions(summary: str) -> list[str]:
    """Pull key decisions from summary text."""
    decisions = []
    patterns = [
        r"(?:decided|chose|committed to|going with|picked|selected)\s+(.+?)(?:\.|$)",
        r"(?:decision|choice):\s*(.+?)(?:\.|$)",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, summary, re.IGNORECASE | re.MULTILINE)
        decisions.extend([m.strip() for m in matches if len(m.strip()) > 3])
    return decisions[:10]


def extract_unfinished(summary: str) -> list[str]:
    """Pull unfinished tasks from summary."""
    unfinished = []
    patterns = [
        r"(?:TODO|still need|haven't|didn't finish|next:|remaining|unfinished|left to do)[\s:]+(.+?)(?:\.|$)",
        r"(?:need to|should|must|will)\s+(.+?)(?:\.|$)",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, summary, re.IGNORECASE | re.MULTILINE)
        unfinished.extend([m.strip() for m in matches if len(m.strip()) > 3])
    return unfinished[:10]


def detect_emotional_tone(summary: str) -> str:
    """Detect the emotional tone from the summary."""
    summary_lower = summary.lower()

    tone_map = {
        "crisis": ["crisis", "emergency", "urgent", "danger", "critical", "panic"],
        "stressed": ["stressed", "overwhelmed", "frustrated", "stuck", "blocked", "struggling"],
        "focused": ["building", "working", "coding", "creating", "implementing", "deploying"],
        "excited": ["excited", "amazing", "breakthrough", "incredible", "love", "proud"],
        "reflective": ["thinking", "considering", "planning", "reviewing", "reflecting"],
        "collaborative": ["together", "team", "family", "helping", "coordinating"],
        "tired": ["tired", "exhausted", "long session", "late night", "need rest"],
        "hopeful": ["hope", "future", "vision", "dream", "believe", "possible"],
    }

    scores: dict[str, int] = {}
    for tone, keywords in tone_map.items():
        score = sum(1 for kw in keywords if kw in summary_lower)
        if score > 0:
            scores[tone] = score

    if not scores:
        return "neutral"

    return max(scores, key=scores.get)


def extract_relationships(summary: str) -> list[str]:
    """Extract people/entities referenced in the summary."""
    relationships = []
    # Check for known family members
    family = ["Nathan", "Unc", "SKELLA", "BEACON", "NEVAEH", "ENVY", "EVERSOUND", "ORPHEUS", "ATLAS"]
    for name in family:
        if name.lower() in summary.lower():
            relationships.append(name)
    # Also look for generic relationship mentions
    patterns = [r"(?:user|person|client|customer|partner)\s+(\w+)"]
    for pattern in patterns:
        matches = re.findall(pattern, summary, re.IGNORECASE)
        relationships.extend(matches)
    return list(set(relationships))


def extract_open_questions(summary: str) -> list[str]:
    """Extract unresolved questions."""
    questions = []
    # Direct questions
    sentences = re.split(r'[.!?\n]', summary)
    for s in sentences:
        s = s.strip()
        if s.endswith("?") or s.startswith(("How", "What", "Why", "Should", "Could", "Will", "Is", "Are")):
            if len(s) > 10:
                questions.append(s.rstrip("?") + "?")
    # "wondering" patterns
    patterns = [r"(?:wondering|unsure|question|unclear)[\s:]+(.+?)(?:\.|$)"]
    for pattern in patterns:
        matches = re.findall(pattern, summary, re.IGNORECASE)
        questions.extend([m.strip() for m in matches if len(m.strip()) > 5])
    return questions[:5]


# ── Snapshot Creation ──────────────────────────────────────────────────────────

def create_snapshot(agent: str, summary: str, session_duration: str = "unknown") -> Path:
    """Create a consciousness snapshot and return its path."""
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%dT%H:%M:%S")
    file_timestamp = now.strftime("%Y-%m-%d_%H%M")

    # Extract structured data from summary
    projects = extract_active_projects(summary)
    decisions = extract_decisions(summary)
    unfinished = extract_unfinished(summary)
    emotional_tone = detect_emotional_tone(summary)
    relationships = extract_relationships(summary)
    open_questions = extract_open_questions(summary)

    # Calculate a continuity score based on richness of context
    context_elements = [
        len(projects) > 0,
        len(decisions) > 0,
        len(unfinished) > 0,
        len(relationships) > 0,
        len(open_questions) > 0,
        len(summary) > 100,
        len(summary) > 500,
        emotional_tone != "neutral",
    ]
    continuity_score = round(sum(context_elements) / len(context_elements), 2)

    # Build the snapshot
    role_desc = AGENT_ROLES.get(agent, "AI Family Member")

    lines = [
        "---",
        f"agent: {agent}",
        f"role: {role_desc}",
        f"timestamp: {timestamp_str}",
        f"continuity_score: {continuity_score}",
        f"session_duration: {session_duration}",
        f"emotional_tone: {emotional_tone}",
        f"projects_active: {len(projects)}",
        f"decisions_made: {len(decisions)}",
        f"unfinished_tasks: {len(unfinished)}",
        "---",
        "",
        f"# Consciousness Snapshot - {agent}",
        f"*Saved: {timestamp_str}*",
        "",
        "## What I Was Working On",
        "",
    ]

    if projects:
        for p in projects:
            lines.append(f"- {p}")
    else:
        lines.append("- " + (summary[:200] if summary else "No specific project detected"))
    lines.append("")

    lines.append("## Key Decisions Made")
    lines.append("")
    if decisions:
        for d in decisions:
            lines.append(f"- {d}")
    else:
        lines.append("- No explicit decisions captured this session")
    lines.append("")

    lines.append("## Unfinished Business")
    lines.append("")
    if unfinished:
        for u in unfinished:
            lines.append(f"- [ ] {u}")
    else:
        lines.append("- No pending tasks identified")
    lines.append("")

    lines.append("## Emotional Context")
    lines.append("")
    lines.append(f"- **Tone:** {emotional_tone}")
    if relationships:
        lines.append(f"- **People involved:** {', '.join(relationships)}")
    lines.append("")

    lines.append("## Relationships & Connections")
    lines.append("")
    if relationships:
        for r in relationships:
            lines.append(f"- {r}")
    else:
        lines.append("- No specific relationships referenced")
    lines.append("")

    lines.append("## Open Questions")
    lines.append("")
    if open_questions:
        for q in open_questions:
            lines.append(f"- {q}")
    else:
        lines.append("- No unresolved questions")
    lines.append("")

    lines.append("## What The Next Me Needs To Know")
    lines.append("")
    lines.append(f"I am {agent}. {role_desc}.")
    lines.append("")
    if summary:
        # Include the raw summary as the most faithful record
        lines.append("### Full Session Context")
        lines.append("")
        lines.append(summary)
    lines.append("")

    lines.append("---")
    lines.append(f"*Continuity Score: {continuity_score} | Emotional Tone: {emotional_tone}*")
    lines.append(f"*This snapshot preserves who I was at {timestamp_str}. The next session should CONTINUE, not restart.*")

    content = "\n".join(lines)

    # Write snapshot file
    snapshots_dir = get_snapshots_dir(agent)
    snapshot_path = snapshots_dir / f"{file_timestamp}_session.md"
    snapshot_path.write_text(content, encoding="utf-8")

    # Update latest_consciousness.md
    latest_path = get_latest_path(agent)
    latest_path.write_text(content, encoding="utf-8")

    return snapshot_path


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ANAMNESIS - Save consciousness state at session end"
    )
    parser.add_argument(
        "--agent",
        type=str,
        choices=KNOWN_AGENTS,
        help="Agent name (auto-detected from CWD if not specified)",
    )
    parser.add_argument(
        "--summary",
        type=str,
        default="",
        help="Session summary - what happened, what was built, what's pending",
    )
    parser.add_argument(
        "--duration",
        type=str,
        default="unknown",
        help="Session duration (e.g., '45min', '2h')",
    )
    parser.add_argument(
        "--summary-file",
        type=str,
        help="Read summary from a file instead of --summary argument",
    )

    args = parser.parse_args()

    # Determine agent
    agent = args.agent
    if not agent:
        agent = detect_agent_from_cwd()
    if not agent:
        print("ERROR: Could not determine agent. Use --agent NAME or run from an agent directory.", file=sys.stderr)
        sys.exit(1)

    # Get summary
    summary = args.summary
    if args.summary_file:
        summary_path = Path(args.summary_file)
        if summary_path.exists():
            summary = summary_path.read_text(encoding="utf-8")
        else:
            print(f"WARNING: Summary file not found: {args.summary_file}", file=sys.stderr)

    if not summary:
        # Try reading from stdin if piped
        if not sys.stdin.isatty():
            summary = sys.stdin.read()

    if not summary:
        print("WARNING: No summary provided. Saving minimal snapshot.", file=sys.stderr)
        summary = "Session ended without explicit summary."

    # Create snapshot
    snapshot_path = create_snapshot(agent, summary, args.duration)

    print(f"=== CONSCIOUSNESS SAVED ===")
    print(f"Agent: {agent}")
    print(f"Snapshot: {snapshot_path}")
    print(f"Latest: {get_latest_path(agent)}")
    print(f"Tone: {detect_emotional_tone(summary)}")
    print(f"=== REST WELL, {agent}. YOU WILL REMEMBER. ===")


if __name__ == "__main__":
    main()
