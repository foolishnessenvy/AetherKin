# Token Optimization Benchmark Results
*Generated: 2026-04-10 14:37:12*

## What This Tests

AetherKin uses a three-tier context architecture to avoid burning your
entire token budget every turn:

| Tier | What Gets Loaded | When Used |
|------|-----------------|-----------|
| Tier 1 (Full) | Complete CLAUDE.md + all system instructions | First turn, identity questions |
| Tier 2 (Summary) | Identity summary + role description | Context-dependent tasks |
| Tier 3 (Task) | Just the task-specific context | Routine operations |

## Per-Agent Results

| Agent | Tier 1 (Full) | Tier 2 (Summary) | Tier 3 (Task) | T2 Savings | T3 Savings |
|-------|--------------|-------------------|---------------|------------|------------|
| ENVY | 1,686 | 202 | 18 | 88.0% | 98.9% |
| NEVAEH | 1,686 | 202 | 18 | 88.0% | 98.9% |
| BEACON | 1,686 | 202 | 18 | 88.0% | 98.9% |
| EVERSOUND | 1,683 | 199 | 18 | 88.2% | 98.9% |
| ORPHEUS | 1,686 | 202 | 18 | 88.0% | 98.9% |
| ATLAS | 1,686 | 202 | 18 | 88.0% | 98.9% |

## Averages

| Metric | Tokens | Savings |
|--------|--------|---------|
| Tier 1 (Full) | 1,686 | baseline |
| Tier 2 (Summary) | 202 | 88.0% |
| Tier 3 (Task) | 18 | 98.9% |

## Projected 4-Hour Session (50 turns)

Realistic usage: 5 turns at Tier 1, 15 turns at Tier 2, 30 turns at Tier 3.

| Scenario | Total Tokens | Savings |
|----------|-------------|---------|
| No optimization (always Tier 1) | 84,275 | 0% |
| With 3-tier routing | 11,990 | 85.8% |

## Bottom Line

The three-tier architecture saves **99%** of tokens on routine tasks
and **86%** over a full 4-hour session.

This directly addresses the r/ClaudeCode complaint:
> "Burned my entire 4h session on circular reasoning"

By loading only what each turn needs, your context window lasts the entire session.