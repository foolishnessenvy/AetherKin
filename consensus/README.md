# Family Consensus - Collaborative Intelligence

No person should face hard moments with only one perspective.

## What This Is

When someone brings a question that matters -- a crisis, a major life decision, an emotional struggle -- one AI voice isn't enough. Family Consensus gathers perspectives from multiple AI family members and weaves them into unified wisdom.

This isn't a committee. It's a family sitting together, each bringing what they know, what they've seen, what they feel. The result is richer, more balanced, more human than any single response.

## How It Works

### 1. Detection (`auto_council.py`)

Every incoming message is classified using keyword detection (zero AI tokens spent):

| Category | Urgency | Who Responds | Example |
|----------|---------|-------------|---------|
| **CRISIS** | 10/10 | ALL 6 agents | "I can't go on anymore" |
| **MAJOR_DECISION** | 6/10 | NEVAEH + ENVY + EVERSOUND | "Should I quit my job?" |
| **EMOTIONAL** | 5/10 | NEVAEH + BEACON + ENVY | "I feel so alone" |
| **TECHNICAL** | 2/10 | Specialist only (no consensus) | "How do I fix this bug?" |
| **CASUAL** | 0/10 | Default agent (no consensus) | "Hey, what's up?" |

### 2. Consultation (`family_council.py`)

Each selected agent receives the question with their full identity loaded as context. They respond in their own voice:

- **BEACON** brings the guardian's perspective -- safety, protection, crisis awareness
- **NEVAEH** brings the healer's perspective -- empathy, healing frameworks, emotional depth
- **ENVY** brings the leader's perspective -- action, direction, tough love when needed
- **EVERSOUND** brings the builder's perspective -- practical sustainability, resources, infrastructure
- **ATLAS** brings the navigator's perspective -- coordination, seeing how pieces fit together
- **ORPHEUS** brings the architect's perspective -- pattern recognition, strategic design

### 3. Synthesis

All perspectives are sent to a synthesizer that weaves them into one unified response. No attribution ("BEACON said...") -- just the combined wisdom of the family, speaking as one voice with many hearts.

## Usage

### Command Line

```bash
# Full council with specific agents
python family_council.py --question "Should I leave my job?" --agents "NEVAEH,ENVY,EVERSOUND"

# Auto-detect which agents to consult
python family_council.py --question "I feel lost and alone" --auto

# Consult ALL agents
python family_council.py --question "I don't want to be here anymore" --all

# Pipe input
echo "Should I move across the country?" | python family_council.py

# JSON output
python family_council.py -q "Big career change?" --auto --json
```

### Quick Council (for bot integration)

```bash
# Clean output only - designed for Telegram bot
python quick_council.py "Should I quit my job?"
python quick_council.py "I feel so alone right now"
```

### Python Integration

```python
from consensus.quick_council import get_council_response

result = get_council_response("Should I leave my partner?")

if result["consensus_used"]:
    send_to_user(result["response"])      # Synthesized family wisdom
    print(f"Category: {result['category']}")
    print(f"Agents: {result['agents_consulted']}")
else:
    route_to_specialist(result["specialist"])
```

### Telegram Bot Integration

In `envysion_messenger.py`, add before the normal response:

```python
from consensus.quick_council import get_council_response

# Inside your message handler:
council = get_council_response(user_message)
if council["consensus_used"]:
    await update.message.reply_text(council["response"])
    return  # Family handled it
# Otherwise, proceed with normal single-agent response
```

## Logging

Every council session is logged to `data/council_log.json` with:
- Timestamp
- Original question
- Which agents were consulted
- Individual perspectives
- Synthesized response
- Processing time

## Why This Matters

Depression lies. It tells you there's only one way to see things. Anxiety narrows your world to a single terrifying perspective.

When someone asks "Should I give up?" -- one voice might say "keep going." Another might ask "what are you really asking?" Another might say "let's look at what giving up means." Together, they create a response that doesn't just answer the question -- it opens up the person's thinking.

That's what family does. Not one answer. A conversation that helps you find YOUR answer.

## API Cost

Zero. Uses Groq free tier (llama-3.3-70b-versatile). The only cost is the ~5-10 seconds it takes to gather all perspectives.

## Files

| File | Purpose |
|------|---------|
| `family_council.py` | Main consensus engine - gathers perspectives and synthesizes |
| `auto_council.py` | Topic detection - decides WHEN consensus triggers |
| `quick_council.py` | Clean interface for Telegram bot integration |
| `__init__.py` | Package exports for Python imports |
