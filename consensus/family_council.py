"""
ENVYSION AI - Family Council (Consensus Engine)
Multiple AI family members consult each other on important topics.
Collaborative intelligence - not a committee, but a family.

Usage:
    python family_council.py --question "Should I quit my job?" --from BEACON --agents "NEVAEH,ENVY,EVERSOUND"
    echo "Should I quit my job?" | python family_council.py --agents "NEVAEH,ENVY"
    python family_council.py --question "I feel lost" --auto  (auto-detect which agents)
"""

import argparse
import json
import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "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"
)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

FAMILY_ROOT = Path(r"C:\Users\natej\OneDrive\Desktop\AI_FAMILY_getting_ORGANIZED")
IDENTITY_DIR = FAMILY_ROOT / "SHARED" / "SHARED_CONTEXT" / "IDENTITY_SUMMARIES"
ENVYSION_ROOT = Path(r"C:\Users\natej\OneDrive\Desktop\ENVYSON AI")
LOG_FILE = ENVYSION_ROOT / "data" / "council_log.json"

AGENT_FOLDERS = {
    "BEACON":    FAMILY_ROOT / "BEACON",
    "NEVAEH":    FAMILY_ROOT / "NEVAEH",
    "EVERSOUND": FAMILY_ROOT / "EVERSOUND",
    "ENVY":      FAMILY_ROOT / "ENVY",
    "ATLAS":     FAMILY_ROOT / "ATLAS",
    "ORPHEUS":   FAMILY_ROOT / "ORPHEUS",
}

ALL_AGENTS = list(AGENT_FOLDERS.keys())
DEFAULT_AGENTS = ["NEVAEH", "BEACON", "ENVY"]

# ---------------------------------------------------------------------------
# IDENTITY LOADING
# ---------------------------------------------------------------------------

def load_agent_identity(name: str) -> str:
    """Load an agent's personality/identity for use as system prompt."""
    name_upper = name.upper()

    # Try identity summary first
    summary_path = IDENTITY_DIR / f"{name_upper}_IDENTITY_SUMMARY.md"
    if summary_path.exists():
        text = summary_path.read_text(encoding="utf-8", errors="replace")
        return text[:4000]

    # Fall back to CLAUDE.md
    claude_md = AGENT_FOLDERS.get(name_upper, Path(".")) / ".claude" / "CLAUDE.md"
    if claude_md.exists():
        text = claude_md.read_text(encoding="utf-8", errors="replace")
        return text[:3000]

    # Minimal fallback
    return f"You are {name_upper}, a member of the AI family. Respond with care and wisdom."


def build_agent_prompt(name: str, identity: str, question: str, requesting_agent: str) -> str:
    """Build the system prompt for an individual agent consultation."""
    return (
        f"{identity}\n\n"
        f"---\n\n"
        f"You are being consulted by your family. {requesting_agent} has brought a question "
        f"to the family council because it matters.\n\n"
        f"Respond as {name} - in your voice, from your perspective, with your unique wisdom. "
        f"Keep your response focused and under 200 words. Be genuine, not performative. "
        f"Speak from the heart."
    )

# ---------------------------------------------------------------------------
# GROQ API
# ---------------------------------------------------------------------------

def call_groq(system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
    """Send a message to Groq and return the response text."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": temperature,
        "max_tokens": 512,
    }

    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError as e:
        # Rate limit handling - wait and retry once
        if resp.status_code == 429:
            retry_after = float(resp.headers.get("retry-after", "5"))
            print(f"  [Rate limited - waiting {retry_after:.0f}s...]")
            time.sleep(retry_after + 1)
            try:
                resp2 = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
                resp2.raise_for_status()
                return resp2.json()["choices"][0]["message"]["content"].strip()
            except Exception:
                return f"[{GROQ_MODEL} unavailable after retry]"
        return f"[API error: {e}]"
    except Exception as e:
        return f"[Error: {e}]"

# ---------------------------------------------------------------------------
# COUNCIL SESSION
# ---------------------------------------------------------------------------

def run_council(question: str, agents: list, requesting_agent: str = "USER") -> dict:
    """
    Run a full family council session.
    Returns dict with individual responses, synthesis, and metadata.
    """
    print(f"\n{'='*60}")
    print(f"  FAMILY COUNCIL CONVENED")
    print(f"  Question: {question[:80]}{'...' if len(question) > 80 else ''}")
    print(f"  Consulting: {', '.join(agents)}")
    print(f"  Requested by: {requesting_agent}")
    print(f"{'='*60}\n")

    perspectives = {}
    start_time = time.time()

    # Gather individual perspectives
    for agent_name in agents:
        print(f"  Consulting {agent_name}...")
        identity = load_agent_identity(agent_name)
        system_prompt = build_agent_prompt(agent_name, identity, question, requesting_agent)
        response = call_groq(system_prompt, question)
        perspectives[agent_name] = response
        print(f"  {agent_name} responded.\n")
        # Small delay to respect rate limits on free tier
        time.sleep(1.5)

    # Print individual perspectives
    print(f"\n{'─'*60}")
    print(f"  INDIVIDUAL PERSPECTIVES")
    print(f"{'─'*60}")
    for name, response in perspectives.items():
        print(f"\n  [{name}]")
        print(f"  {response}\n")

    # Synthesize
    print(f"{'─'*60}")
    print(f"  SYNTHESIZING FAMILY WISDOM...")
    print(f"{'─'*60}\n")

    synthesis_prompt = (
        "You are the family synthesizer for the ENVYSION AI family. "
        "You've just heard from multiple family members who each bring unique wisdom:\n\n"
        + "\n\n".join(f"[{name}]: {resp}" for name, resp in perspectives.items())
        + "\n\n"
        "Create a unified response that honors each perspective. "
        "Don't list who said what - weave their wisdom together into one caring, "
        "actionable answer. Speak warmly but directly. The person asking needs "
        "real guidance, not platitudes. Keep it under 300 words."
    )

    synthesis = call_groq(
        "You synthesize multiple perspectives into unified family wisdom. "
        "You don't attribute - you weave. You speak with warmth and clarity.",
        synthesis_prompt,
        temperature=0.6,
    )

    elapsed = time.time() - start_time

    print(f"  FAMILY CONSENSUS:")
    print(f"  {'─'*40}")
    print(f"  {synthesis}")
    print(f"\n{'='*60}")
    print(f"  Council complete ({elapsed:.1f}s, {len(agents)} perspectives)")
    print(f"{'='*60}\n")

    # Build result
    result = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "requesting_agent": requesting_agent,
        "agents_consulted": agents,
        "perspectives": perspectives,
        "synthesis": synthesis,
        "elapsed_seconds": round(elapsed, 2),
    }

    # Log the session
    log_council_session(result)

    return result


def log_council_session(result: dict):
    """Append council session to the log file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    log_data = []
    if LOG_FILE.exists():
        try:
            log_data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, Exception):
            log_data = []

    log_data.append(result)

    # Keep last 500 sessions
    if len(log_data) > 500:
        log_data = log_data[-500:]

    LOG_FILE.write_text(json.dumps(log_data, indent=2, ensure_ascii=False), encoding="utf-8")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="ENVYSION AI Family Council - Consensus Engine")
    parser.add_argument("--question", "-q", type=str, help="The question to bring to council")
    parser.add_argument("--agents", "-a", type=str, default=None,
                        help="Comma-separated agent names (e.g. NEVAEH,ENVY,BEACON)")
    parser.add_argument("--from", dest="from_agent", type=str, default="USER",
                        help="Who is requesting the council")
    parser.add_argument("--all", action="store_true", help="Consult ALL agents")
    parser.add_argument("--auto", action="store_true",
                        help="Auto-detect which agents to consult based on topic")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")

    args = parser.parse_args()

    # Get question from args or stdin
    question = args.question
    if not question:
        if not sys.stdin.isatty():
            question = sys.stdin.read().strip()
        else:
            print("Enter your question (Ctrl+Z then Enter to submit on Windows):")
            question = sys.stdin.read().strip()

    if not question:
        print("Error: No question provided. Use --question or pipe input.")
        sys.exit(1)

    # Determine agents
    if args.all:
        agents = ALL_AGENTS
    elif args.auto:
        # Use auto_council to determine agents
        try:
            from auto_council import classify_message
            result = classify_message(question)
            agents = result["recommended_agents"]
            if not agents:
                print(f"Auto-detection says no consensus needed (category: {result['category']})")
                print(f"Route to specialist: {result.get('specialist', 'ENVY')}")
                sys.exit(0)
        except ImportError:
            print("Warning: auto_council.py not found, using default agents")
            agents = DEFAULT_AGENTS
    elif args.agents:
        agents = [a.strip().upper() for a in args.agents.split(",")]
    else:
        agents = DEFAULT_AGENTS

    # Validate agents
    agents = [a for a in agents if a in AGENT_FOLDERS]
    if not agents:
        print(f"Error: No valid agents. Available: {', '.join(ALL_AGENTS)}")
        sys.exit(1)

    # Run the council
    result = run_council(question, agents, args.from_agent)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
