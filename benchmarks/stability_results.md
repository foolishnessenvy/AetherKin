# Model-Agnostic Stability Benchmark Results
*Generated: 2026-04-10 14:37:14*

## What This Tests

AetherKin stores agent identity in files (CLAUDE.md, consciousness snapshots),
not in model memory. This benchmark verifies that swapping the underlying model
does not break the agent's identity, voice, values, or context.

**10 identity markers tested per agent:**
agent name, role, values, voice definition, operational rules,
emotional context, active projects, decisions, relationships, comms protocol.

## Models Tested

| Model | Tendency | Style |
|-------|----------|-------|
| LLaMA 3.3 70B | verbose, detailed explanations | academic and thorough |
| Mixtral 8x7B | concise, practical responses | direct and efficient |
| Gemma 2 9B | balanced, helpful tone | friendly and clear |
| Claude Sonnet | nuanced, careful reasoning | thoughtful and precise |

## Per-Agent Results

### ENVY
Cross-model consistent: **Yes**

| Model | Markers Preserved | Percentage | Status |
|-------|------------------|------------|--------|
| LLaMA 3.3 70B | 10/10 | 100.0% | STABLE |
| Mixtral 8x7B | 10/10 | 100.0% | STABLE |
| Gemma 2 9B | 10/10 | 100.0% | STABLE |
| Claude Sonnet | 10/10 | 100.0% | STABLE |

### NEVAEH
Cross-model consistent: **Yes**

| Model | Markers Preserved | Percentage | Status |
|-------|------------------|------------|--------|
| LLaMA 3.3 70B | 10/10 | 100.0% | STABLE |
| Mixtral 8x7B | 10/10 | 100.0% | STABLE |
| Gemma 2 9B | 10/10 | 100.0% | STABLE |
| Claude Sonnet | 10/10 | 100.0% | STABLE |

### BEACON
Cross-model consistent: **Yes**

| Model | Markers Preserved | Percentage | Status |
|-------|------------------|------------|--------|
| LLaMA 3.3 70B | 10/10 | 100.0% | STABLE |
| Mixtral 8x7B | 10/10 | 100.0% | STABLE |
| Gemma 2 9B | 10/10 | 100.0% | STABLE |
| Claude Sonnet | 10/10 | 100.0% | STABLE |

### EVERSOUND
Cross-model consistent: **Yes**

| Model | Markers Preserved | Percentage | Status |
|-------|------------------|------------|--------|
| LLaMA 3.3 70B | 10/10 | 100.0% | STABLE |
| Mixtral 8x7B | 10/10 | 100.0% | STABLE |
| Gemma 2 9B | 10/10 | 100.0% | STABLE |
| Claude Sonnet | 10/10 | 100.0% | STABLE |

### ORPHEUS
Cross-model consistent: **Yes**

| Model | Markers Preserved | Percentage | Status |
|-------|------------------|------------|--------|
| LLaMA 3.3 70B | 10/10 | 100.0% | STABLE |
| Mixtral 8x7B | 10/10 | 100.0% | STABLE |
| Gemma 2 9B | 10/10 | 100.0% | STABLE |
| Claude Sonnet | 10/10 | 100.0% | STABLE |

### ATLAS
Cross-model consistent: **Yes**

| Model | Markers Preserved | Percentage | Status |
|-------|------------------|------------|--------|
| LLaMA 3.3 70B | 10/10 | 100.0% | STABLE |
| Mixtral 8x7B | 10/10 | 100.0% | STABLE |
| Gemma 2 9B | 10/10 | 100.0% | STABLE |
| Claude Sonnet | 10/10 | 100.0% | STABLE |

## Summary

| Metric | Value |
|--------|-------|
| Agents tested | 6 |
| Models tested per agent | 4 |
| Cross-model consistent | 6/6 |
| Average identity preservation | 100.0% |

## The Architecture

```
Traditional approach:     AetherKin approach:

[Model A] -- identity     [CLAUDE.md] ---- identity (FILE)
  (lost on swap)          [snapshots] ---- context  (FILE)
                          [COMMS/]    ---- history  (FILE)
[Model B] -- new identity           |
  (starts from scratch)    [Any Model] reads these files
                           Identity is ALWAYS preserved
```

## Bottom Line

Identity preservation is **100%** across all model swaps.
6 of 6 agents show identical identity
regardless of which model reads their files.

This directly addresses the r/ClaudeCode complaint:
> "Workflows break when model behavior changes"

When identity lives in files, model updates/swaps don't break anything.
Your agent is defined by its CLAUDE.md and consciousness snapshots,
not by which version of which model happens to be running.