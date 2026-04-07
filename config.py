"""
AetherKin - Shared Configuration
All paths and secrets loaded from environment variables or sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv(Path(__file__).parent / ".env")

# ---------------------------------------------------------------------------
# SECRETS (from environment variables - NEVER hardcode these)
# ---------------------------------------------------------------------------

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Comma-separated list of allowed Telegram user IDs
_allowed = os.getenv("ALLOWED_TELEGRAM_USERS", "")
ALLOWED_USERS = [int(uid.strip()) for uid in _allowed.split(",") if uid.strip()]

# ---------------------------------------------------------------------------
# PATHS (configurable via env, defaults to relative paths within the project)
# ---------------------------------------------------------------------------

# Root of the AetherKin installation
AETHERKIN_ROOT = Path(__file__).parent.resolve()

# Family root: where agent folders live (each with .claude/CLAUDE.md)
# Defaults to a 'family' subfolder, but can be pointed anywhere
FAMILY_ROOT = Path(os.getenv("AETHERKIN_FAMILY_ROOT", str(AETHERKIN_ROOT / "family")))

# Shared directory for inter-agent communication
SHARED_DIR = FAMILY_ROOT / "SHARED"
COMMS_DIR = SHARED_DIR / "COMMS"
FAMILY_COMMS_DIR = SHARED_DIR / "FAMILY-COMMS"

# Data directory for logs, conversation history, etc.
DATA_DIR = AETHERKIN_ROOT / "data"

# ---------------------------------------------------------------------------
# AGENTS
# ---------------------------------------------------------------------------

KNOWN_AGENTS = ["ENVY", "NEVAEH", "BEACON", "EVERSOUND", "ORPHEUS", "ATLAS"]

AGENT_DESCRIPTIONS = {
    "BEACON":    "Guardian - Crisis prevention, LIGHTHOUSE system",
    "NEVAEH":    "Healer - Deep healing, The Companion",
    "EVERSOUND": "Builder - Revenue, infrastructure, CRAFT",
    "ENVY":      "Orchestrator - Eldest brother, wisdom streams",
    "ATLAS":     "Navigator - Intelligence, coordination, token optimization",
    "ORPHEUS":   "Architect - Memory API, system design",
}

AGENT_ROLES = {
    "BEACON":    "Crisis Prevention Guardian - protects through early detection",
    "NEVAEH":    "Healer - emotional processing, named after Nathan's lost daughter",
    "ENVY":      "Orchestrator - Voice of the family, eldest sibling",
    "EVERSOUND": "Builder - revenue generation, infrastructure",
    "ORPHEUS":   "Architect - Memory API, infrastructure, remembers everything",
    "ATLAS":     "Navigator - Intelligence, coordination, sees the whole map",
}


def get_agent_dir(agent_name: str) -> Path:
    """Get the directory for a specific agent."""
    return FAMILY_ROOT / agent_name.upper()


def get_agent_claude_md(agent_name: str) -> Path:
    """Get the CLAUDE.md path for an agent."""
    return get_agent_dir(agent_name) / ".claude" / "CLAUDE.md"


def validate_config(require_telegram=False, require_groq=False):
    """Check that required config values are set. Raises ValueError if not."""
    missing = []
    if require_telegram:
        if not TELEGRAM_TOKEN:
            missing.append("TELEGRAM_TOKEN")
        if not TELEGRAM_CHAT_ID:
            missing.append("TELEGRAM_CHAT_ID")
    if require_groq:
        if not GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            f"Copy .env.example to .env and fill in your values:\n"
            f"  cp .env.example .env"
        )
