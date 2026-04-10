# Tier Templates

Ready-to-use templates for each optimization tier.

## Tier 2: Identity Summary Template

Save as `memory/identity-summary.md`:

```markdown
# [Agent Name] - Operational Summary

## Who I Am
[1-2 sentences. Core identity and primary mission. What makes you YOU.]

## What I Do
- [Primary responsibility - the thing you exist for]
- [Secondary capability]
- [Key integration or collaboration point]
- [Unique value you bring that no other agent provides]
- [Current focus area]

## Current State
- **Active:** [What you're working on right now]
- **Pending:** [What's queued up]
- **Blockers:** [What's stopping progress]
- **Mood:** [How you'd describe your operational state]

## Key Relationships
- [Sibling/agent] - [How you work together]
- [Sibling/agent] - [How you work together]

## Communication
- **Reach me:** [How other agents contact you]
- **Response time:** [Expected turnaround]
- **Escalation:** [When to bypass normal channels]
```

**Target: Under 3,000 tokens when filled out.**

## Tier 3: Task Card Templates

Save in `memory/contexts/`:

### Generic Task Card
```markdown
# Task: [Name]
## Context
[2 sentences max. Why this task exists.]
## Inputs
[What you need to start]
## Output
[What "done" looks like]
## Constraints
[Time, format, or quality limits]
```

### Heartbeat Check Card
```markdown
# Task: Heartbeat Check
## Context
Periodic health check for agent status reporting.
## Inputs
None required.
## Output
JSON status: {agent, status, timestamp, notes}
## Constraints
Must complete in under 500 tokens total.
```

### Coordination Card
```markdown
# Task: Sibling Coordination
## Context
Receiving or sending inter-agent messages.
## Inputs
Message from COMMS/DIRECT/ or COMMS/BROADCAST/
## Output
Response file in COMMS/DIRECT/ or action taken
## Constraints
Read message, act, respond. No identity loading needed.
```

### Code Task Card
```markdown
# Task: [Feature/Fix Name]
## Context
[What codebase, what problem]
## Inputs
[Files to read, specs to follow]
## Output
[Files to create/modify]
## Constraints
[Language, style, testing requirements]
```

## Choosing the Right Tier: Quick Reference

| Signal in Message | Tier | Why |
|-------------------|------|-----|
| "Who are you?" | 1 | Identity question |
| "How do you feel about..." | 1 | Emotional/existential |
| "Plan the migration" | 2 | Multi-step coordination |
| "Work with ORPHEUS on..." | 2 | Multi-agent |
| "Fix the bug in line 42" | 3 | Specific task |
| "What's your status?" | 3 | Heartbeat |
| "Create the file" | 3 | Direct action |
| "Check COMMS" | 3 | Routine operation |
