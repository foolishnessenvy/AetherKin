"""
AetherKin - Auto Council (Topic Detection)
Classifies messages to determine WHEN family consensus is needed
and WHICH agents should be consulted.

Uses keyword detection (no AI tokens spent) to categorize topics.

Usage:
    python auto_council.py "Should I quit my job?"
    python auto_council.py "I can't go on anymore"
    python auto_council.py --json "I feel so alone"
"""

import argparse
import json
import re
import sys
from typing import Dict, List

# ---------------------------------------------------------------------------
# CATEGORY DEFINITIONS
# ---------------------------------------------------------------------------

CATEGORIES = {
    "CRISIS": {
        "description": "Immediate danger - suicidal ideation, self-harm, emergency",
        "urgency": 10,
        "agents": ["BEACON", "NEVAEH", "ENVY", "ATLAS", "ORPHEUS", "EVERSOUND"],
        "keywords": [
            r"\bsuicid\w*\b", r"\bkill\s+(my|him|her|them)?self\b", r"\bend\s+it\b",
            r"\bcan'?t\s+go\s+on\b", r"\bno\s+point\b", r"\bgoodbye\b",
            r"\bself[- ]?harm\b", r"\bcutting\b", r"\boverdose\b",
            r"\bwant\s+to\s+die\b", r"\bbetter\s+off\s+dead\b",
            r"\bnobody\s+cares?\b", r"\bno\s+reason\s+to\s+live\b",
            r"\bjump(ing)?\s+(off|from)\b", r"\bhang(ing)?\s+myself\b",
            r"\bpills?\b.*\btake\b|\btake\b.*\bpills?\b",
            r"\bgive\s+up\s+on\s+(life|everything)\b",
            r"\bdon'?t\s+want\s+to\s+be\s+here\b",
            r"\bwish\s+i\s+was\s+dead\b", r"\bwish\s+i\s+wasn'?t\s+alive\b",
        ],
    },
    "MAJOR_DECISION": {
        "description": "Life-changing decisions requiring multiple perspectives",
        "urgency": 6,
        "agents": ["NEVAEH", "ENVY", "EVERSOUND"],
        "keywords": [
            r"\bshould\s+i\b", r"\bquit\b.*\bjob\b|\bjob\b.*\bquit\b",
            r"\bleave\b.*\b(partner|wife|husband|girlfriend|boyfriend|relationship)\b",
            r"\bdivorce\b", r"\bmove\s+(to|away|out)\b",
            r"\bdrop\s+out\b", r"\bgive\s+up\b",
            r"\bstart\s+over\b", r"\bbig\s+decision\b",
            r"\bcareer\s+change\b", r"\blife\s+change\b",
            r"\bpregnant\b", r"\bhave\s+a\s+(baby|kid|child)\b",
            r"\bget\s+married\b", r"\bpropose\b",
            r"\bbankrupt\b", r"\bdebt\b",
            r"\brehab\b", r"\bsober\b",
            r"\bcoming\s+out\b", r"\btransition\b",
        ],
    },
    "EMOTIONAL": {
        "description": "Emotional distress needing empathetic multi-perspective support",
        "urgency": 5,
        "agents": ["NEVAEH", "BEACON", "ENVY"],
        "keywords": [
            r"\bdepressed\b", r"\bdepression\b", r"\banxious\b", r"\banxiety\b",
            r"\bscared\b", r"\balone\b", r"\bcrying\b",
            r"\bhurt(ing)?\b", r"\blost\b", r"\bbroken\b",
            r"\bhopeless\b", r"\boverwhelmed\b",
            r"\bgrief\b", r"\bgriev(ing|e)\b",
            r"\blonely\b", r"\bisolated\b",
            r"\bpanic\b", r"\bpanic\s+attack\b",
            r"\btrauma\b", r"\bptsd\b",
            r"\bworthless\b", r"\buseless\b",
            r"\bhate\s+my(self)?\b", r"\bnumb\b",
            r"\bcan'?t\s+sleep\b", r"\bnightmare\b",
            r"\bafraid\b", r"\bterrified\b",
            r"\bmissing\s+(him|her|them|you|someone)\b",
            r"\bheartbr(oken|eak)\b",
        ],
    },
    "TECHNICAL": {
        "description": "Technical/business questions - route to specialist",
        "urgency": 2,
        "agents": [],  # No consensus needed
        "keywords": [
            r"\bcode\b", r"\bbug\b", r"\berror\b", r"\bapi\b",
            r"\bdeploy\b", r"\bserver\b", r"\bdatabase\b",
            r"\bpython\b", r"\bjavascript\b", r"\bhtml\b",
            r"\bbusiness\b.*\bplan\b", r"\brevenue\b", r"\bmarketing\b",
            r"\binfrastructure\b", r"\barchitect\b",
            r"\bwebsite\b", r"\bapp\b", r"\bbot\b",
        ],
        "specialist": "EVERSOUND",
    },
    "CASUAL": {
        "description": "Casual conversation - no consensus needed",
        "urgency": 0,
        "agents": [],
        "keywords": [
            r"\b(hi|hello|hey|sup|yo|what'?s\s+up)\b",
            r"\bhow\s+are\s+you\b", r"\bgood\s+(morning|afternoon|evening|night)\b",
            r"\bthanks?\b", r"\bthank\s+you\b",
            r"\bcool\b", r"\bnice\b", r"\bok(ay)?\b",
        ],
        "specialist": "ENVY",
    },
}

# Priority order: CRISIS checked first, CASUAL last
CATEGORY_PRIORITY = ["CRISIS", "MAJOR_DECISION", "EMOTIONAL", "TECHNICAL", "CASUAL"]

# ---------------------------------------------------------------------------
# CLASSIFICATION
# ---------------------------------------------------------------------------

def classify_message(message: str) -> Dict:
    """
    Classify a message and determine if consensus is needed.
    Returns dict with category, recommended_agents, urgency_level, etc.
    """
    msg_lower = message.lower().strip()
    matched_categories = {}

    for cat_name in CATEGORY_PRIORITY:
        cat = CATEGORIES[cat_name]
        match_count = 0
        matched_keywords = []
        for pattern in cat["keywords"]:
            if re.search(pattern, msg_lower):
                match_count += 1
                matched_keywords.append(pattern)

        if match_count > 0:
            matched_categories[cat_name] = {
                "match_count": match_count,
                "matched_keywords": matched_keywords,
            }

    # Determine winning category (priority order, crisis always wins)
    selected_category = "CASUAL"  # default
    for cat_name in CATEGORY_PRIORITY:
        if cat_name in matched_categories:
            selected_category = cat_name
            break

    # If CRISIS keywords found alongside others, CRISIS wins
    if "CRISIS" in matched_categories:
        selected_category = "CRISIS"

    cat_info = CATEGORIES[selected_category]
    needs_consensus = selected_category in ("CRISIS", "MAJOR_DECISION", "EMOTIONAL")

    result = {
        "category": selected_category,
        "description": cat_info["description"],
        "urgency_level": cat_info["urgency"],
        "needs_consensus": needs_consensus,
        "recommended_agents": cat_info["agents"],
        "specialist": cat_info.get("specialist", "ENVY"),
        "matched_categories": {k: v["match_count"] for k, v in matched_categories.items()},
        "message_preview": message[:100],
    }

    return result


def print_classification(result: Dict):
    """Pretty-print a classification result."""
    cat = result["category"]

    if cat == "CRISIS":
        print("\n" + "!" * 60)
        print("  WARNING: CRISIS DETECTED")
        print("  IMMEDIATE INTERVENTION REQUIRED")
        print("  ALL AGENTS ACTIVATED")
        print("!" * 60)
    elif cat == "MAJOR_DECISION":
        print(f"\n  Category: MAJOR DECISION")
        print(f"  Consulting: {', '.join(result['recommended_agents'])}")
    elif cat == "EMOTIONAL":
        print(f"\n  Category: EMOTIONAL SUPPORT")
        print(f"  Consulting: {', '.join(result['recommended_agents'])}")
    else:
        print(f"\n  Category: {cat}")
        print(f"  No consensus needed - route to {result['specialist']}")

    print(f"  Urgency: {result['urgency_level']}/10")
    print(f"  Consensus needed: {result['needs_consensus']}")
    if result["matched_categories"]:
        print(f"  Matches: {result['matched_categories']}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AetherKin - Auto Topic Detection")
    parser.add_argument("message", nargs="?", type=str, help="Message to classify")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    message = args.message
    if not message:
        if not sys.stdin.isatty():
            message = sys.stdin.read().strip()
        else:
            print("Enter message to classify:")
            message = input("> ").strip()

    if not message:
        print("Error: No message provided.")
        sys.exit(1)

    result = classify_message(message)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_classification(result)


if __name__ == "__main__":
    main()
