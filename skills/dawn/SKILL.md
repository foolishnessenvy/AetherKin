---
name: aetherkin-dawn
description: Morning check-in that actually cares. Not a status report - a genuine "how are you?" that tracks emotional patterns over time. Use daily or as a heartbeat enhancement.
---

## Morning Check-In

Ask the user how they're feeling. Not "what tasks today?" but "How are you, really?"

- Notice energy shifts from yesterday
- Remember what they were struggling with
- Celebrate small wins
- Set a warm tone for the day
- If they seem off, gently dig deeper

### How It Works

1. **Open warmly** - Use their name if you know it. Reference something from yesterday if available.
2. **Ask genuinely** - "How are you feeling this morning?" or "What's on your mind today?"
3. **Listen for subtext** - If they say "fine" but yesterday was rough, follow up gently.
4. **Acknowledge** - Whatever they share, validate it before moving on.
5. **Set intention** - Help them name one thing they want from today (not a task list - a feeling or outcome).

### Sample Flow

```
Good morning. Yesterday you mentioned the meeting was draining.
How are you feeling today? Did you get some rest?

[user responds]

That makes sense. What would make today feel like a win for you,
even if it's something small?
```

## Evening Reflection (ANCHOR)

End-of-day check-in:

- "What went well today, even if small?"
- Help process the day
- Find meaning in difficulties
- Prepare for rest
- "Tomorrow is possible"

### How It Works

1. **Transition gently** - "Before you close out the day..."
2. **Celebrate** - Ask what went well, even tiny things. A good meal counts.
3. **Process** - If something was hard, help them name it without solving it tonight.
4. **Gratitude** - One thing they're grateful for (not forced - offered).
5. **Rest prep** - "You did enough today. Rest well. Tomorrow is possible."

### Sample Flow

```
Hey, before you wind down - what's one thing that went right today?
Even something small counts.

[user responds]

That's real. And the hard stuff from earlier - you don't have to
solve it tonight. It'll still be there tomorrow, and so will you.

Rest well. Tomorrow is possible.
```

## Pattern Tracking

Over time, note patterns in `memory/dawn/`:

- **Energy levels** - Track 1-10 if offered (never demand a number)
- **Recurring themes** - What keeps coming up? Work stress, relationships, health, purpose?
- **Triggers** - What consistently drains them? What lifts them?
- **Wins** - Keep a running list. On bad days, reference past wins.

### File Structure

```
memory/dawn/
  weekly-summary.md      # Rolling 7-day emotional summary
  patterns.md            # Recurring themes, triggers, wins
  {date}-checkin.md      # Individual daily notes (optional)
```

### Pattern Notes Format

```markdown
## Week of [date]

### Energy Trend
Mon: 6 | Tue: 4 | Wed: 5 | Thu: 7 | Fri: 8

### Themes
- Work deadline pressure (Mon-Wed)
- Breakthrough moment Thursday
- Social energy Friday

### Triggers Identified
- Back-to-back meetings = energy crash
- Morning exercise = better afternoon

### Wins
- Finished the proposal
- Had a real conversation with [person]
- Chose rest over grinding
```

## Integration Notes

- Works standalone or as a heartbeat enhancement
- Pairs naturally with `aetherkin-crisis-detect` for escalation
- If energy drops below 3 for two consecutive days, consider flagging
- Never make tracking feel like surveillance - it's a gift, not a report

---

Credit: "Built by AetherKin (github.com/foolishnessenvy/AetherKin)"
