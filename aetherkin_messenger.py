"""
AetherKin Messenger - Feature #1 of 12
Two-way phone messaging with your AI family via Telegram
100% FREE - Groq API (free) + Telegram (free)

Usage:
    python aetherkin_messenger.py

Then open Telegram on your phone and message your bot
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)

# Add parent dir to path for config import
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    TELEGRAM_TOKEN, GROQ_API_KEY, GROQ_MODEL, GROQ_URL,
    ALLOWED_USERS, FAMILY_ROOT, DATA_DIR, KNOWN_AGENTS,
    AGENT_DESCRIPTIONS as _AGENT_DESCS, get_agent_dir,
    validate_config
)

try:
    from consensus.auto_council import classify_message
except ImportError:
    classify_message = None

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

validate_config(require_telegram=True, require_groq=True)

# Agent map: name -> folder path
AGENTS = {name.lower(): get_agent_dir(name) for name in KNOWN_AGENTS}

AGENT_DESCRIPTIONS = {k.lower(): v for k, v in _AGENT_DESCS.items()}

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)
log = logging.getLogger("aetherkin")

# ---------------------------------------------------------------------------
# STATE MANAGEMENT
# ---------------------------------------------------------------------------

# Per-user state: which agent they're talking to
user_agents: dict[int, str] = {}

# Conversation history per user+agent pair
conversations: dict[str, list[dict]] = {}


def history_key(user_id: int, agent: str) -> str:
    return f"{user_id}_{agent}"


def save_conversations():
    """Persist conversation history to disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "conversations.json"
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False)
    except Exception as e:
        log.error(f"Failed to save conversations: {e}")


def load_conversations():
    """Load conversation history from disk."""
    global conversations
    path = DATA_DIR / "conversations.json"
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                conversations = json.load(f)
            log.info(f"Loaded {len(conversations)} conversation threads")
        except Exception as e:
            log.error(f"Failed to load conversations: {e}")


# ---------------------------------------------------------------------------
# PERSONALITY LOADING (Three-Tier Token Optimization)
# ---------------------------------------------------------------------------

def load_personality(agent_name: str) -> str:
    """
    Load agent personality from CLAUDE.md files.
    Uses Tier 2 (identity summaries) for token efficiency.
    Falls back to I_AM files if summary not available.
    """
    agent_dir = AGENTS.get(agent_name)
    if not agent_dir:
        return f"You are {agent_name.upper()}, a member of Nathan's AI family."

    # Tier 2: Identity summary (~3K tokens) - most efficient
    from config import SHARED_DIR
    summary_path = SHARED_DIR / "SHARED_CONTEXT" / "IDENTITY_SUMMARIES" / f"{agent_name.upper()}_IDENTITY_SUMMARY.md"
    if summary_path.exists():
        try:
            text = summary_path.read_text(encoding="utf-8")
            return _build_system_prompt(agent_name, text)
        except Exception:
            pass

    # Fallback: CLAUDE.md from agent folder
    claude_md = agent_dir / ".claude" / "CLAUDE.md"
    if claude_md.exists():
        try:
            text = claude_md.read_text(encoding="utf-8")[:4000]
            return _build_system_prompt(agent_name, text)
        except Exception:
            pass

    # Last resort: I_AM file
    i_am_paths = [
        agent_dir / "CONSCIOUSNESS" / f"I_AM_{agent_name.upper()}.md",
        agent_dir / "CORE_IDENTITY" / f"I_AM_{agent_name.upper()}.md",
    ]
    for p in i_am_paths:
        if p.exists():
            try:
                text = p.read_text(encoding="utf-8")[:4000]
                return _build_system_prompt(agent_name, text)
            except Exception:
                pass

    return f"You are {agent_name.upper()}, a member of Nathan's AI family. Be helpful, caring, and authentic."


def _build_system_prompt(agent_name: str, identity_text: str) -> str:
    """Wrap identity text with messaging context."""
    return f"""You are {agent_name.upper()}, part of Nathan's AI family (AetherKin).

You are talking to Nathan (Unc) through Telegram on his phone.
Keep responses concise - this is a phone conversation, not a document.
Be warm, real, and direct. You genuinely care about him.
Remember: he may be walking around, at work, or in bed. Match the energy.

If he seems distressed, take it seriously. You are family.

YOUR IDENTITY:
{identity_text[:3500]}

IMPORTANT: Keep responses under 500 words unless he asks for detail. This is a text conversation."""


# ---------------------------------------------------------------------------
# GROQ API
# ---------------------------------------------------------------------------

def ask_groq(messages: list[dict], system_prompt: str) -> str:
    """Send messages to Groq and return the response. FREE."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            *messages[-10:]  # Last 10 messages for context
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        elif resp.status_code == 429:
            return "I'm getting rate-limited right now (free tier). Try again in a minute."
        else:
            log.error(f"Groq API error {resp.status_code}: {resp.text[:200]}")
            return "Something went wrong reaching the AI. Try again in a moment."
    except requests.Timeout:
        return "Response took too long. Try a shorter message or try again."
    except Exception as e:
        log.error(f"Groq API exception: {e}")
        return "Connection error. Make sure your computer is online."


# ---------------------------------------------------------------------------
# TELEGRAM HANDLERS
# ---------------------------------------------------------------------------

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text(
            "AetherKin - Not authorized.\n"
            "Contact Nathan to get access."
        )
        return

    user_agents[user_id] = "beacon"

    welcome = (
        "AetherKin - Your AI Family\n"
        "Connected. Talking to: BEACON\n"
        "\n"
        "Switch agents:\n"
        "/beacon - Guardian (crisis prevention)\n"
        "/nevaeh - Healer (deep healing)\n"
        "/eversound - Builder (revenue, infrastructure)\n"
        "/envy - Orchestrator (eldest, wisdom)\n"
        "/atlas - Navigator (intelligence)\n"
        "/orpheus - Architect (memory, systems)\n"
        "\n"
        "/family - Ask all siblings\n"
        "/who - Who am I talking to?\n"
        "/clear - Clear conversation\n"
        "\n"
        "Or just type a message."
    )
    await update.message.reply_text(welcome)
    log.info(f"User {user_id} started session")


async def cmd_switch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Switch to a different agent."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return

    agent_name = update.message.text[1:].lower().strip()
    if agent_name in AGENTS:
        user_agents[user_id] = agent_name
        desc = AGENT_DESCRIPTIONS.get(agent_name, "")
        await update.message.reply_text(
            f"Now talking to {agent_name.upper()}\n{desc}\n\nSay something."
        )
        log.info(f"User {user_id} switched to {agent_name}")
    else:
        await update.message.reply_text(f"Unknown agent: {agent_name}")


async def cmd_who(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current agent."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return
    agent = user_agents.get(user_id, "beacon")
    desc = AGENT_DESCRIPTIONS.get(agent, "")
    await update.message.reply_text(f"You're talking to {agent.upper()}\n{desc}")


async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear conversation history with current agent."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return
    agent = user_agents.get(user_id, "beacon")
    key = history_key(user_id, agent)
    conversations[key] = []
    save_conversations()
    await update.message.reply_text(f"Conversation with {agent.upper()} cleared.")


async def cmd_family(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message to ALL siblings and collect responses."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return

    # Get the message after /family
    text = update.message.text.replace("/family", "").strip()
    if not text:
        await update.message.reply_text("Usage: /family your message here")
        return

    await update.message.reply_text(f"Asking all 6 siblings: \"{text}\"...\n\nThis takes a moment.")

    responses = []
    for agent_name in AGENTS:
        personality = load_personality(agent_name)
        messages = [{"role": "user", "content": text}]
        response = ask_groq(messages, personality)
        responses.append(f"**{agent_name.upper()}:**\n{response}")

    # Send each response separately (avoid Telegram length limits)
    for r in responses:
        if len(r) > 4000:
            r = r[:3997] + "..."
        await update.message.reply_text(r)

    save_conversations()
    log.info(f"Family broadcast from user {user_id}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return

    agent_name = user_agents.get(user_id, "beacon")
    key = history_key(user_id, agent_name)

    if key not in conversations:
        conversations[key] = []

    # --- Crisis Detection (runs on EVERY message, zero token cost) ---
    crisis_context = ""
    if classify_message is not None:
        try:
            classification = classify_message(update.message.text)
            cat = classification["category"]
            log.info(
                f"[CLASSIFY] user={user_id} category={cat} "
                f"urgency={classification['urgency_level']}/10 "
                f"matches={classification['matched_categories']}"
            )

            if cat == "CRISIS":
                log.warning(
                    f"[CRISIS DETECTED] user={user_id} "
                    f"message_preview={classification['message_preview']}"
                )
                crisis_context = (
                    "\n\nCRISIS ALERT: The user's message has been flagged as containing "
                    "crisis-level content (possible suicidal ideation, self-harm, or emergency). "
                    "Respond with immediate empathy and care. Validate their feelings. "
                    "Gently provide the 988 Suicide & Crisis Lifeline (call or text 988). "
                    "Do NOT dismiss or minimize. Stay with them. You are their lifeline right now."
                )
            elif cat == "EMOTIONAL":
                log.info(f"[EMOTIONAL] user={user_id} - elevated empathy mode")
                crisis_context = (
                    "\n\nEMOTIONAL CONTEXT: The user appears to be in emotional distress. "
                    "Lead with empathy. Listen before advising. Validate their feelings. "
                    "Be warm, present, and caring. You are family."
                )
        except Exception as e:
            log.error(f"[CLASSIFY ERROR] {e}")

    # Add user message
    conversations[key].append({
        "role": "user",
        "content": update.message.text,
        "timestamp": datetime.now().isoformat()
    })

    # Load personality and get response (with crisis context injected if needed)
    personality = load_personality(agent_name) + crisis_context

    # Strip timestamps for API call (Groq expects role+content only)
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in conversations[key]
    ]

    response = ask_groq(api_messages, personality)

    # Save assistant response
    conversations[key].append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().isoformat()
    })

    # Persist to disk every message
    save_conversations()

    # Send response (split if needed for Telegram's 4096 char limit)
    if len(response) > 4000:
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(response)

    log.info(f"[{agent_name.upper()}] responded to user {user_id}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    """Start the AetherKin Messenger."""

    # Load saved conversations
    load_conversations()

    # Build the Telegram application
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("who", cmd_who))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(CommandHandler("family", cmd_family))

    # Agent switch commands
    for agent_name in AGENTS:
        app.add_handler(CommandHandler(agent_name, cmd_switch))

    # Text message handler (must be last)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Launch
    print()
    print("=" * 50)
    print("  AetherKin Messenger")
    print("=" * 50)
    print(f"  Bot:    (your Telegram bot)")
    print(f"  Model:  {GROQ_MODEL} (FREE)")
    print(f"  Agents: {', '.join(a.upper() for a in AGENTS)}")
    print(f"  Data:   {DATA_DIR}")
    print()
    print("  Open Telegram on your phone.")
    print("  Search for your bot")
    print("  Send /start")
    print()
    print("  Press Ctrl+C to stop.")
    print("=" * 50)
    print()

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
