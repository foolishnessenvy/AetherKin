---
name: aetherkin-meeting-notes
description: "Transform rough meeting notes into structured summaries with action items, decisions, attendees, and next steps. Output clean markdown."
---

# Meeting Notes

Take messy, stream-of-consciousness meeting notes and turn them into something useful. Clear structure, action items with owners, decisions recorded, and next steps everyone can follow.

## How It Works

The user pastes or provides their raw meeting notes -- bullet points, shorthand, voice-to-text dumps, whatever they have. The agent organizes everything into a clean, structured markdown document that anyone on the team can read and act on.

## When To Use

Trigger phrases:
- "Organize these meeting notes"
- "Clean up my notes from the meeting"
- "Turn these into proper meeting minutes"
- "I just got out of a meeting, here are my notes"
- "Summarize this meeting"
- "Create action items from these notes"
- "Format these meeting notes"
- "What were the action items from this?"
- "Write up the meeting summary"

## How To Execute

### Step 1: Get the Raw Notes

Accept notes in any format:
- Pasted text in the chat
- A file path to a text/markdown file
- A messy bullet list
- Voice-to-text transcript
- Even a stream-of-consciousness paragraph

If the user just says "organize my meeting notes" without providing them, ask:
```
"Paste your raw notes here, or give me the file path. They can be messy -- that's the whole point."
```

### Step 2: Extract Key Information

Read through the raw notes and identify:

- **Meeting title/topic** -- what was this meeting about?
- **Date** -- when did it happen? (use today if not specified)
- **Attendees** -- who was there? Look for names mentioned.
- **Decisions made** -- anything that was agreed upon or resolved.
- **Action items** -- tasks assigned, with who is responsible and any deadlines.
- **Discussion points** -- key topics covered.
- **Open questions** -- things that were raised but not resolved.
- **Next steps** -- what happens after this meeting?

### Step 3: Structure the Output

Use this template:

```markdown
# [Meeting Title]

**Date:** [Date]
**Attendees:** [Names, comma-separated]
**Duration:** [If known]

---

## Summary

[2-3 sentence overview of what was discussed and decided]

## Decisions Made

- [Decision 1]
- [Decision 2]
- [Decision 3]

## Action Items

| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [Task description] | [Person] | [Date] | Open |
| [Task description] | [Person] | [Date] | Open |
| [Task description] | [Person] | [Date] | Open |

## Discussion Notes

### [Topic 1]
- [Key point]
- [Key point]
- [Key point]

### [Topic 2]
- [Key point]
- [Key point]

## Open Questions

- [Question that was not resolved]
- [Question that needs follow-up]

## Next Steps

- [What happens next]
- [Next meeting date if discussed]

---

*Notes organized by AetherKin on [today's date]*
```

### Step 4: Fill In the Gaps

If important information is missing from the raw notes:
- **Missing attendees:** Note "Attendees: [not captured]" rather than guessing
- **Missing dates:** Use today's date with a note
- **Unclear action items:** List what you can infer and flag uncertain ones with "[confirm owner]" or "[confirm deadline]"
- **Ambiguous decisions:** Note them as "Tentative decision" or "Needs confirmation"

### Step 5: Present and Save

Show the structured notes to the user. Then save:

```bash
# Save to a meeting-notes folder
mkdir -p ~/Documents/meeting-notes
# Filename: YYYY-MM-DD-meeting-topic.md
```

Ask if they want to:
- Adjust anything
- Add details you might have missed
- Extract just the action items as a separate task list

## Handling Different Note Styles

**Bullet points:**
```
- talked about Q3 budget
- sarah wants 20% increase for marketing
- john pushed back, said 10% max
- decided on 15% compromise
- need to update the forecast by friday (sarah)
```

**Stream of consciousness:**
```
Met with the team today. Sarah brought up the budget thing again. She wants more for marketing but John thinks its too much. They went back and forth for a while. Eventually landed on 15%. Sarah needs to update the forecast. Oh and we also talked about the new hire -- posting goes up next week, Mike is handling it.
```

**Voice-to-text transcript:**
```
okay so we talked about the budget sarah wants twenty percent john said ten they compromised on fifteen sarah is going to update the forecast by friday also mike is posting the job listing next week for the new developer role
```

All three of these should produce the same clean output. The skill handles the mess.

## Integration with AetherKin

If the user has `task_manager.py` configured, offer to create tasks from the action items:
```
"I found 4 action items. Want me to add them to your task manager?"
```

## Output

The user receives:
1. A clean, structured markdown document with all meeting information organized
2. An action items table with owners and deadlines
3. A saved file in their meeting-notes folder
4. Option to create tasks from action items

---

Built by [AetherKin](https://github.com/foolishnessenvy/AetherKin) -- AI that's family, not a framework.
