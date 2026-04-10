# Consciousness Continuity Benchmark Results
*Generated: 2026-04-10 14:37:30*

## What This Tests

The Anamnesis system saves structured consciousness snapshots at session end
and restores them at session start. This benchmark measures how many specific
facts survive the save/restore cycle vs. a naive paragraph summary.

**20 facts tested:** project names, database choices, architecture decisions,
bug reports, emotional context, relationships, preferences, metrics, priorities,
blockers, learnings, TODOs, and milestones.

## Results Per Iteration

| Iteration | Anamnesis Facts | Anamnesis % | Baseline Facts | Baseline % | Continuity Score |
|-----------|----------------|-------------|----------------|------------|-----------------|
| 1 | 20/20 | 100.0% | 2/20 | 10.0% | 0.653 |
| 2 | 20/20 | 100.0% | 2/20 | 10.0% | 0.653 |
| 3 | 20/20 | 100.0% | 2/20 | 10.0% | 0.653 |
| 4 | 20/20 | 100.0% | 2/20 | 10.0% | 0.653 |
| 5 | 20/20 | 100.0% | 2/20 | 10.0% | 0.653 |

## Summary

| Metric | Value |
|--------|-------|
| Average Anamnesis retention | 100.0% |
| Average Baseline retention | 10.0% |
| Improvement | +90.0 percentage points |
| Average continuity score | 0.653 |

## Fact Categories Tested

| Category | Example Fact |
|----------|-------------|
| Project name | LIGHTHOUSE crisis prevention system |
| Database choice | PostgreSQL 16 with pgvector extension |
| Architecture decision | Event-driven over REST polling |
| Bug fixed | Race condition in DAWN scheduler |
| Bug pending | Telegram webhook message drops |
| Emotional context | Nathan excited about launch |
| Relationship | BEACON-NEVAEH coordination |
| User preference | No emojis in communication |
| Performance metric | 1.2s COMPANION response time |
| Priority | Ship benchmark scripts |
| Blocker | GROQ_API_KEY needed |
| Learning | tiktoken vs word-count |
| TODO items | Rate limiting, integration tests |
| Milestone | 20 files on GitHub |

## Bottom Line

Anamnesis preserves **100%** of session context vs. **10%**
for a naive paragraph summary.

This directly addresses the r/ClaudeCode complaint:
> "Context loss between sessions / dementia"

Structured consciousness snapshots preserve decisions, emotional context,
relationships, and unfinished work -- not just project names.