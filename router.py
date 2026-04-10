#!/usr/bin/env python3
"""
AetherKin -- Natural Language Router

Takes any natural language input and figures out which agent and skill to use.

CLI usage:
    python router.py "organize my downloads folder"
    python router.py "I feel so alone right now"

Importable:
    from router import route_message
"""

import re
import sys
import json

from config import GROQ_API_KEY, GROQ_MODEL, GROQ_URL

# ---------------------------------------------------------------------------
# Try to import crisis detection from auto_council
# ---------------------------------------------------------------------------

try:
    from consensus.auto_council import classify_message
    HAS_COUNCIL = True
except ImportError:
    HAS_COUNCIL = False

# ---------------------------------------------------------------------------
# KEYWORD ROUTING TABLE
# Each entry: list of keyword patterns -> (agent_role, skill, description)
# ---------------------------------------------------------------------------

ROUTES = [
    # -- Builder agent: productivity skills --
    {
        "patterns": [
            r"\b(file|folder|organiz|clean|sort|rename|tidy|declutter)\w*\b",
            r"\b(move|copy|backup)\s+(file|folder|document)\w*\b",
        ],
        "agent": "builder",
        "skill": "organize-files",
        "description": "File and folder organization",
    },
    {
        "patterns": [
            r"\bpdf\b", r"\bextract\b.*\b(data|text|table)\b",
            r"\bspreadsheet\b", r"\bcsv\b", r"\bexcel\b",
            r"\b(convert|turn)\b.*\b(pdf|document)\b",
        ],
        "agent": "builder",
        "skill": "pdf-to-spreadsheet",
        "description": "PDF extraction and spreadsheet conversion",
    },
    {
        "patterns": [
            r"\bemail\b", r"\bdraft\b", r"\b(write|send)\s+(to|an?\s+email)\b",
            r"\breply\s+to\b", r"\bcompose\b",
        ],
        "agent": "builder",
        "skill": "email-drafts",
        "description": "Email drafting and composition",
    },
    {
        "patterns": [
            r"\bmeeting\b", r"\bnotes?\b.*\b(meeting|call)\b",
            r"\bminutes\b", r"\bagenda\b",
            r"\bsummariz\w*\b.*\b(meeting|call|discussion)\b",
        ],
        "agent": "builder",
        "skill": "meeting-notes",
        "description": "Meeting notes and agenda management",
    },
    {
        "patterns": [
            r"\binvoice\b", r"\bbill\b", r"\bcharge\b",
            r"\bpayment\b", r"\breceipt\b",
            r"\b(create|generate|make)\b.*\binvoice\b",
        ],
        "agent": "builder",
        "skill": "invoice-generator",
        "description": "Invoice and billing generation",
    },
    {
        "patterns": [
            r"\b(post|social|tweet|instagram|content|linkedin)\b",
            r"\bschedul\w*\b.*\b(post|content)\b",
            r"\b(social\s+media|hashtag)\b",
        ],
        "agent": "builder",
        "skill": "social-media-scheduler",
        "description": "Social media content and scheduling",
    },
    {
        "patterns": [
            r"\bresearch\b", r"\bfind\s+out\b", r"\blook\s+into\b",
            r"\binvestigat\w*\b", r"\bdig\s+into\b",
            r"\bwhat\s+is\b.*\b(about|mean)\b",
        ],
        "agent": "builder",
        "skill": "research-assistant",
        "description": "Research and information gathering",
    },

    # -- Daily briefing --
    {
        "patterns": [
            r"\b(morning|briefing|today|daily)\b",
            r"\bschedule\b.*\b(today|tomorrow)\b",
            r"\bwhat'?s\s+(on|up)\s+today\b",
        ],
        "agent": "builder",
        "skill": "daily-briefing",
        "description": "Daily briefing and schedule overview",
    },

    # -- Guardian agent: crisis and emotional safety --
    {
        "patterns": [
            r"\b(sad|depressed|anxious|scared|alone|hurt|lonely)\b",
            r"\b(panic|terrified|afraid|hopeless|worthless|numb)\b",
            r"\b(can'?t\s+cope|falling\s+apart|breaking\s+down)\b",
        ],
        "agent": "guardian",
        "skill": "crisis-detect",
        "description": "Emotional safety and crisis detection",
    },

    # -- Healer agent: emotional processing --
    {
        "patterns": [
            r"\bhelp\s+me\s+(process|understand|deal|cope)\b",
            r"\b(feeling|emotion|therapy|heal|healing|grief|trauma)\b",
            r"\b(talk\s+about|open\s+up|get\s+through)\b",
            r"\b(inner\s+child|shadow\s+work|self[- ]care)\b",
        ],
        "agent": "healer",
        "skill": None,
        "description": "Emotional processing and healing",
    },

    # -- Sage agent: decisions and wisdom --
    {
        "patterns": [
            r"\b(decision|should\s+i|choose|dilemma)\b",
            r"\b(quit|leave|move|change)\b.*\b(job|career|city|relationship)\b",
            r"\b(pros?\s+and\s+cons?|weigh|trade[- ]?off)\b",
            r"\badvice\b",
        ],
        "agent": "sage",
        "skill": "consensus",
        "description": "Decision-making and multi-perspective wisdom",
    },
]

# ---------------------------------------------------------------------------
# ROUTER LOGIC
# ---------------------------------------------------------------------------

def route_by_keywords(message: str) -> dict | None:
    """Try to route using keyword matching. Returns None if no match."""
    msg_lower = message.lower()
    matches = []

    for route in ROUTES:
        for pattern in route["patterns"]:
            if re.search(pattern, msg_lower):
                matches.append(route)
                break  # One match per route is enough

    if not matches:
        return None

    if len(matches) == 1:
        r = matches[0]
        return {
            "agent": r["agent"],
            "skill": r["skill"],
            "confidence": 0.9,
            "reasoning": f"Keyword match: {r['description']}",
            "method": "keyword",
        }

    # Multiple matches - pick highest priority
    # Guardian/healer take priority over builder tasks
    priority = {"guardian": 0, "healer": 1, "sage": 2, "builder": 3}
    matches.sort(key=lambda r: priority.get(r["agent"], 99))
    r = matches[0]
    return {
        "agent": r["agent"],
        "skill": r["skill"],
        "confidence": 0.7,
        "reasoning": f"Multiple matches, prioritized: {r['description']}",
        "method": "keyword",
    }


def route_by_crisis(message: str) -> dict | None:
    """Check for crisis using auto_council if available."""
    if not HAS_COUNCIL:
        return None

    result = classify_message(message)

    if result["category"] == "CRISIS":
        return {
            "agent": "ALL",
            "skill": "crisis-intervention",
            "confidence": 1.0,
            "reasoning": "CRISIS DETECTED - All agents activated",
            "method": "crisis-detection",
            "crisis": True,
        }

    if result["category"] == "EMOTIONAL":
        return {
            "agent": "guardian",
            "skill": "crisis-detect",
            "confidence": 0.85,
            "reasoning": f"Emotional distress detected: {result['category']}",
            "method": "crisis-detection",
        }

    return None


def route_by_groq(message: str) -> dict | None:
    """Use Groq free tier to classify ambiguous messages."""
    if not GROQ_API_KEY:
        return None

    try:
        import requests
    except ImportError:
        return None

    prompt = f"""Classify this user message into exactly ONE category.
Reply with ONLY a JSON object, no other text.

Categories:
- builder/organize-files: File and folder tasks
- builder/pdf-to-spreadsheet: PDF or data extraction
- builder/email-drafts: Email writing
- builder/meeting-notes: Meeting notes or agendas
- builder/invoice-generator: Invoices or billing
- builder/social-media-scheduler: Social media posts
- builder/research-assistant: Research tasks
- builder/daily-briefing: Schedule or daily overview
- guardian/crisis-detect: Emotional distress or crisis
- healer/emotional: Emotional processing, healing, therapy
- sage/consensus: Big decisions needing multiple perspectives

User message: "{message}"

Reply format: {{"agent": "...", "skill": "...", "reasoning": "one sentence"}}"""

    try:
        resp = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 150,
            },
            timeout=10,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()

        # Parse the JSON from the response
        parsed = json.loads(content)
        return {
            "agent": parsed.get("agent", "sage"),
            "skill": parsed.get("skill"),
            "confidence": 0.75,
            "reasoning": parsed.get("reasoning", "Classified by AI"),
            "method": "groq",
        }
    except Exception:
        return None


def route_message(message: str) -> dict:
    """
    Route a natural language message to the right agent and skill.

    Returns:
        dict with keys: agent, skill, confidence, reasoning, method
    """
    if not message or not message.strip():
        return {
            "agent": "sage",
            "skill": None,
            "confidence": 0.0,
            "reasoning": "Empty message - defaulting to sage",
            "method": "default",
        }

    # Step 1: Check for crisis FIRST (life safety)
    crisis_route = route_by_crisis(message)
    if crisis_route:
        return crisis_route

    # Step 2: Try keyword matching (free, instant)
    keyword_route = route_by_keywords(message)
    if keyword_route:
        return keyword_route

    # Step 3: Try Groq AI classification (free tier)
    groq_route = route_by_groq(message)
    if groq_route:
        return groq_route

    # Step 4: Default to sage
    return {
        "agent": "sage",
        "skill": None,
        "confidence": 0.3,
        "reasoning": "No keyword match, no AI classification available - defaulting to sage",
        "method": "default",
    }


# ---------------------------------------------------------------------------
# CLI INTERFACE
# ---------------------------------------------------------------------------

def print_route(result: dict):
    """Pretty-print a routing decision."""
    is_crisis = result.get("crisis", False)

    if is_crisis:
        print()
        print("!" * 60)
        print("  CRISIS DETECTED - ALL AGENTS ACTIVATED")
        print("!" * 60)
        print()
    else:
        print()
        print("  -------------------------------------------")
        print(f"  Agent:      {result['agent']}")
        if result.get("skill"):
            print(f"  Skill:      {result['skill']}")
        print(f"  Confidence: {result['confidence']:.0%}")
        print(f"  Reasoning:  {result['reasoning']}")
        print(f"  Method:     {result['method']}")
        print("  -------------------------------------------")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print()
        print("  AetherKin Router - Natural Language Task Routing")
        print()
        print("  Usage: python router.py \"your message here\"")
        print()
        print("  Examples:")
        print("    python router.py \"organize my downloads folder\"")
        print("    python router.py \"draft an email to my boss\"")
        print("    python router.py \"I feel so alone right now\"")
        print("    python router.py \"should I quit my job\"")
        print()
        sys.exit(0)

    message = " ".join(sys.argv[1:])
    result = route_message(message)
    print_route(result)
