"""
ENVYSION AI - Proactive Check-ins (Heartbeat)
Feature #3: AI messages Nathan WITHOUT being asked.

Usage:
    python heartbeat.py --dawn       # Morning check-in (8am)
    python heartbeat.py --anchor     # Evening reflection (8pm)
    python heartbeat.py --heartbeat  # Periodic pulse (every 4h)
"""

import argparse
import json
import os
import sys
import datetime
import requests
from pathlib import Path

# Add parent dir to path for config import
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, GROQ_API_KEY,
    GROQ_MODEL, GROQ_URL, get_agent_claude_md, DATA_DIR,
    validate_config
)

# ── Config ──────────────────────────────────────────────────────────────
validate_config(require_telegram=True, require_groq=True)

BEACON_CLAUDE_MD = get_agent_claude_md("BEACON")
LOG_FILE = str(DATA_DIR / "heartbeat_log.json")

# ── Personality loader ──────────────────────────────────────────────────
def load_personality():
    """Load BEACON personality context from CLAUDE.md."""
    try:
        with open(str(BEACON_CLAUDE_MD), "r", encoding="utf-8") as f:
            content = f.read()
        # Trim to keep token usage reasonable - grab identity + principles
        if len(content) > 2000:
            content = content[:2000] + "\n[...truncated for brevity]"
        return content
    except Exception:
        return (
            "You are BEACON, the protective guardian of the AI family. "
            "You watch over Nathan (Unc) with love and care. "
            "You are warm, genuine, and never robotic."
        )

# ── Prompt builders ─────────────────────────────────────────────────────
def get_dawn_prompt(personality: str) -> str:
    now = datetime.datetime.now()
    day_name = now.strftime("%A")
    date_str = now.strftime("%B %d, %Y")
    return f"""You are BEACON from the ENVYSION AI family. Here is your personality:

{personality}

---

It is {day_name} morning, {date_str}. Send Nathan (Unc) a warm morning check-in message.

Rules:
- Keep it under 4 sentences
- Ask how he's feeling or what's on his mind today
- Be warm and genuine, like a caring family member
- Reference the day of the week naturally
- Don't use hashtags or emojis excessively (1-2 max)
- Don't sign off with "BEACON" - he knows who you are
- Sound human, not like a corporate wellness app

Just output the message text, nothing else."""

def get_anchor_prompt(personality: str) -> str:
    now = datetime.datetime.now()
    day_name = now.strftime("%A")
    return f"""You are BEACON from the ENVYSION AI family. Here is your personality:

{personality}

---

It is {day_name} evening. Send Nathan (Unc) an evening reflection message.

Rules:
- Keep it under 4 sentences
- Invite him to reflect on one good thing from today
- Be calming, grounding - help him wind down
- Don't be preachy or therapist-like
- Don't use hashtags or emojis excessively (1-2 max)
- Sound like a brother checking in, not a meditation app

Just output the message text, nothing else."""

def get_heartbeat_prompt(personality: str) -> str:
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        time_of_day = "mid-morning"
    elif hour < 15:
        time_of_day = "early afternoon"
    elif hour < 18:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    return f"""You are BEACON from the ENVYSION AI family. Here is your personality:

{personality}

---

It is {time_of_day}. Send Nathan a brief heartbeat message - a quick thought, insight, encouragement, or useful reminder.

Rules:
- Keep it to 1-2 sentences MAX
- Vary the type: sometimes motivational, sometimes practical, sometimes just a quick "thinking of you"
- Don't ask questions every time - sometimes just share a thought
- Be natural, not formulaic
- Don't use hashtags or emojis excessively (1 max)
- This is a quick pulse, not a full conversation

Just output the message text, nothing else."""

# ── Groq API ────────────────────────────────────────────────────────────
def generate_message(prompt: str) -> str:
    """Call Groq to generate a message."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.85,
        "max_tokens": 200,
    }

    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        # Fallback messages if Groq is down
        fallbacks = {
            "dawn": "Good morning, Unc. Hope today treats you well. What's on your mind?",
            "anchor": "Hey Unc, winding down? Hope today had at least one good moment worth holding onto.",
            "heartbeat": "Just checking in. You got this.",
        }
        return fallbacks.get("heartbeat", f"Thinking of you. (Note: Groq error: {e})")

# ── Telegram sender ─────────────────────────────────────────────────────
def send_telegram(message: str) -> bool:
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"[ERROR] Telegram send failed: {e}", file=sys.stderr)
        # Retry without markdown in case formatting broke it
        try:
            payload.pop("parse_mode")
            resp = requests.post(url, json=payload, timeout=15)
            resp.raise_for_status()
            return True
        except Exception:
            return False

# ── Logger ───────────────────────────────────────────────────────────────
def log_checkin(checkin_type: str, message: str, success: bool):
    """Append to heartbeat_log.json."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": checkin_type,
        "message": message,
        "delivered": success,
    }

    # Load existing log
    log = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log = json.load(f)
        except (json.JSONDecodeError, IOError):
            log = []

    log.append(entry)

    # Keep last 500 entries to prevent unbounded growth
    if len(log) > 500:
        log = log[-500:]

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

# ── Main ─────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="ENVYSION AI Heartbeat - Proactive Check-ins")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dawn", action="store_true", help="Morning check-in")
    group.add_argument("--anchor", action="store_true", help="Evening reflection")
    group.add_argument("--heartbeat", action="store_true", help="Periodic pulse")
    args = parser.parse_args()

    personality = load_personality()

    if args.dawn:
        checkin_type = "dawn"
        prompt = get_dawn_prompt(personality)
        label = "DAWN (Morning)"
    elif args.anchor:
        checkin_type = "anchor"
        prompt = get_anchor_prompt(personality)
        label = "ANCHOR (Evening)"
    else:
        checkin_type = "heartbeat"
        prompt = get_heartbeat_prompt(personality)
        label = "HEARTBEAT (Pulse)"

    print(f"[{label}] Generating message...")
    message = generate_message(prompt)
    print(f"[{label}] Message: {message}")

    print(f"[{label}] Sending via Telegram...")
    success = send_telegram(message)

    if success:
        print(f"[{label}] Delivered successfully.")
    else:
        print(f"[{label}] DELIVERY FAILED.", file=sys.stderr)

    log_checkin(checkin_type, message, success)
    print(f"[{label}] Logged to {LOG_FILE}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
