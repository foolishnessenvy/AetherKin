# AetherKin Trust & Verification System

How auto-verification and crisis detection work across the system.

---

## Every Message Is Classified

Every message that enters AetherKin through `aetherkin_messenger.py` (Telegram) is
run through `consensus.auto_council.classify_message()` BEFORE a response is generated.

This is not optional. It is wired into the message handler. Zero tokens are spent --
classification uses keyword-based regex pattern matching, not AI inference.

### Categories

| Category       | Urgency | What Happens                                          |
|----------------|---------|-------------------------------------------------------|
| CRISIS         | 10/10   | Crisis context injected into system prompt. 988 info. |
| MAJOR_DECISION | 6/10    | Multi-agent consensus recommended.                    |
| EMOTIONAL      | 5/10    | Empathetic context injected into system prompt.       |
| TECHNICAL      | 2/10    | Routed to specialist (EVERSOUND).                     |
| CASUAL         | 0/10    | Normal response, no modification.                     |

### The Flow

```
User sends message (Telegram)
        |
        v
classify_message(text)        <-- zero cost, keyword regex
        |
        v
Category determined (CRISIS / EMOTIONAL / MAJOR_DECISION / TECHNICAL / CASUAL)
        |
        v
[CRISIS?] --> inject crisis context into system prompt
              log warning with message preview
              988 Suicide & Crisis Lifeline referenced in response
        |
[EMOTIONAL?] --> inject empathetic context into system prompt
                 log elevated attention note
        |
        v
load_personality(agent) + crisis_context
        |
        v
ask_groq(messages, modified_personality)
        |
        v
Response sent to user
```

## Session Start Crisis Scan

When an agent starts a session (`coordination/session_start.py`), the last 10 direct
messages addressed to that agent are scanned through `classify_message()`.

- CRISIS messages produce a prominent warning banner.
- EMOTIONAL messages produce a note about elevated attention.
- This ensures agents are aware of context before they begin working.

## Verify Mode (--verify flag)

`session_start.py` accepts a `--verify` flag:

```
python coordination/session_start.py BEACON --verify
```

When enabled, the session prints `[VERIFY MODE] Factual claims will be cross-checked`.
This signals to the agent (and any downstream tooling) that factual claims in messages
should be validated through a secondary source (Groq cross-check).

This is an opt-in mode because:
- Crisis detection is always free (keyword-based, zero tokens)
- Factual verification costs tokens (requires Groq inference)
- Most sessions do not need fact-checking
- When they do, --verify makes it explicit

## Autopilot Integration

`autopilot.py` continuously monitors `data/inbox/` and classifies every new file
using `classify_message()`. CRISIS detections are logged with elevated severity.
This means crisis detection runs 24/7 on any incoming content, not just Telegram.

## What This Proves

1. **Every interaction is monitored** -- not a marketing claim, wired into the code
2. **Crisis detection costs nothing** -- pure regex, no API calls
3. **Response modification is automatic** -- crisis/emotional context injected before inference
4. **Verification is opt-in** -- --verify flag for factual cross-checking
5. **Coverage is continuous** -- autopilot scans inbox files even when no user is chatting

## Files Involved

| File                              | Role                                    |
|-----------------------------------|-----------------------------------------|
| `consensus/auto_council.py`       | classify_message() - keyword classifier |
| `aetherkin_messenger.py`          | Telegram bot with inline classification |
| `coordination/session_start.py`   | Session start crisis scan + --verify    |
| `autopilot.py`                    | Continuous inbox monitoring              |
| `coordination/session_end.py`     | Token usage tracking                    |
| `data/token_usage.json`           | Token audit trail                       |
| `data/autopilot_log.json`         | Autopilot activity log                  |
