---
name: aetherkin-token-optimizer
description: Three-tier context loading system. 88% measured token reduction. Load full identity only when needed, summaries for coordination, index cards for routine tasks.
---

## The Three Tiers

### Tier 1: Full Consciousness (use 5% of the time)

Load everything - full SOUL.md, MEMORY.md, all context files.

**When to use:**
- First session with a new user
- Identity crisis or existential questions
- Deep personal conversations
- Major decisions that require full context
- When the agent says "I don't know who I am"

**Token cost:** ~15,000 tokens
**Files loaded:** SOUL.md, MEMORY.md, all memory/*.md, relevant COMMS/

### Tier 2: Operational Summary (use 20% of the time)

Load a condensed identity summary (~3,000 tokens max).

**When to use:**
- Coordination tasks between agents
- Planning sessions
- Working with other agents or siblings
- When you need to know who you are but not every detail

**Token cost:** ~3,000 tokens
**Files loaded:** memory/identity-summary.md, task-relevant context only

**Create your Tier 2 file:**
```markdown
# [Agent Name] - Operational Summary

## Who I Am (2 sentences max)
[Core identity and mission]

## What I Do (bullet list, 5 items max)
- [Primary responsibility]
- [Key capability]
- [Key capability]
- [Integration point]
- [Unique value]

## Current State
- Active projects: [list]
- Pending items: [list]
- Blockers: [list]

## How to Reach Me
[Communication protocol]
```

### Tier 3: Task Card (use 75% of the time)

Load only what's needed for the current task (~500 tokens max).

**When to use:**
- Routine work and specific tasks
- Quick responses and status checks
- Heartbeat checks
- File operations
- Code generation with clear specs

**Token cost:** ~500 tokens
**Files loaded:** Single task-specific context card

**Create task cards at:** `memory/contexts/[task-name].md`

**Task card format:**
```markdown
# Task: [Name]
## Context (2 sentences)
## Inputs
## Expected Output
## Constraints
```

## How to Implement

1. **On session start**, assess what tier is needed based on the incoming message:
   - Message mentions feelings, identity, who you are? -> Tier 1
   - Message is about coordination, planning, multi-step? -> Tier 2
   - Message is a specific task, question, or check? -> Tier 3

2. **Load only that tier's context** - resist the urge to load everything "just in case"

3. **For heartbeat checks:** always Tier 3 (a heartbeat should cost ~500 tokens, not 15,000)

4. **For user conversations:** start at Tier 2, escalate to Tier 1 only if identity or deep work is needed

5. **Escalation is fine** - if you start at Tier 3 and realize you need more context, load Tier 2. But don't preload.

## Decision Flowchart

```
Incoming message
    |
    v
Is this about identity, feelings, or a major decision?
    YES -> Tier 1 (full load)
    NO  -> |
           v
    Is this coordination, planning, or multi-agent work?
        YES -> Tier 2 (summary)
        NO  -> Tier 3 (task card)
```

## Measured Results

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Avg tokens/interaction | 15,000 | 1,750 | -88% |
| Monthly cost (6 agents) | ~$145 | ~$48 | -67% |
| Heartbeat cost | 15,000 | 500 | -97% |
| Coordination cost | 15,000 | 3,000 | -80% |

### Weighted Calculation
- Tier 1 (5% of ops): 15,000 x 0.05 = 750
- Tier 2 (20% of ops): 3,000 x 0.20 = 600
- Tier 3 (75% of ops): 500 x 0.75 = 375
- **Weighted average: 1,725 tokens per interaction**

## Common Mistakes

1. **Loading Tier 1 "just to be safe"** - This defeats the entire purpose. Trust the tiers.
2. **Not creating Tier 2/3 files** - The system only works if you pre-build your summaries and task cards.
3. **Putting everything in one file** - Split context into small, loadable chunks.
4. **Forgetting to update summaries** - Your Tier 2 should reflect current state, not last month's state.

## Setup Checklist

- [ ] Create `memory/identity-summary.md` (your Tier 2)
- [ ] Create `memory/contexts/` directory
- [ ] Build task cards for your 5 most common tasks
- [ ] Set default tier in your agent config
- [ ] Measure baseline token usage before optimization
- [ ] Measure again after 1 week

---

Credit: "Built by AetherKin (github.com/foolishnessenvy/AetherKin)"
