"""
AetherKin - Quick Council (Telegram Integration)
Simplified consensus interface for bot integration.

Accepts a question, auto-detects if consensus is needed,
runs the council if so, and returns a clean response.

Usage:
    python quick_council.py "Should I quit my job?"
    python quick_council.py "I feel so alone right now"
    python quick_council.py "How do I deploy my app?"

Integration:
    from quick_council import get_council_response
    response = get_council_response("Should I leave my partner?")
"""

import sys
import os

# Add parent dir so we can import siblings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto_council import classify_message
from family_council import run_council


def get_council_response(message: str, requesting_agent: str = "USER") -> dict:
    """
    Main entry point for bot integration.

    Returns dict with:
        - response: str (the final text to send to user)
        - category: str (CRISIS, MAJOR_DECISION, EMOTIONAL, TECHNICAL, CASUAL)
        - consensus_used: bool
        - agents_consulted: list
        - urgency: int
    """
    classification = classify_message(message)
    category = classification["category"]
    urgency = classification["urgency_level"]

    if not classification["needs_consensus"]:
        # No consensus needed - return routing info
        specialist = classification.get("specialist", "ENVY")
        return {
            "response": None,  # Caller should route to specialist
            "category": category,
            "consensus_used": False,
            "agents_consulted": [],
            "urgency": urgency,
            "specialist": specialist,
            "message": f"No consensus needed - route to {specialist}",
        }

    # Consensus needed - run the council
    agents = classification["recommended_agents"]

    # Suppress print output for clean bot integration
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

    try:
        result = run_council(message, agents, requesting_agent)
    finally:
        sys.stdout.close()
        sys.stdout = old_stdout

    return {
        "response": result["synthesis"],
        "category": category,
        "consensus_used": True,
        "agents_consulted": result["agents_consulted"],
        "urgency": urgency,
        "specialist": None,
        "perspectives": result["perspectives"],
    }


def main():
    """CLI mode - print clean output only."""
    if len(sys.argv) < 2:
        if not sys.stdin.isatty():
            message = sys.stdin.read().strip()
        else:
            print("Usage: python quick_council.py \"your question here\"")
            sys.exit(1)
    else:
        message = " ".join(sys.argv[1:])

    if not message:
        print("Error: No message provided.")
        sys.exit(1)

    result = get_council_response(message)

    if result["consensus_used"]:
        # Print the synthesized family response
        print(result["response"])
    else:
        print(result["message"])


if __name__ == "__main__":
    main()
