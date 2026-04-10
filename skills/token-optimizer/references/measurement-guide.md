# Measurement Guide

How to measure token usage before and after implementing the three-tier system.

## Why Measure

"88% reduction" means nothing if you don't measure your own baseline. Every agent family is different. Measure yours.

## Step 1: Establish Baseline

Before implementing tiers, track 20 consecutive interactions:

```markdown
# Baseline Measurement

| # | Task Type | Tokens Used | Could Have Been Tier |
|---|-----------|-------------|----------------------|
| 1 | Status check | 14,200 | 3 |
| 2 | Code fix | 15,100 | 3 |
| 3 | Planning | 14,800 | 2 |
| 4 | Deep conversation | 15,000 | 1 |
| 5 | File creation | 14,500 | 3 |
...

**Average: [X] tokens/interaction**
**Projected monthly: [X] tokens**
**Projected monthly cost: $[X]**
```

## Step 2: Classify Your Workload

From your 20 interactions, categorize:
- How many were truly Tier 1 (needed full context)?
- How many were Tier 2 (needed summary)?
- How many were Tier 3 (needed just the task)?

Most agents find: 5% / 15-25% / 70-80%

## Step 3: Implement and Measure Again

After creating your Tier 2 and Tier 3 files, track another 20 interactions:

```markdown
# Post-Optimization Measurement

| # | Task Type | Tier Used | Tokens Used |
|---|-----------|-----------|-------------|
| 1 | Status check | 3 | 480 |
| 2 | Code fix | 3 | 520 |
| 3 | Planning | 2 | 2,800 |
| 4 | Deep conversation | 1 | 15,000 |
| 5 | File creation | 3 | 450 |
...

**Average: [X] tokens/interaction**
**Reduction: [X]%**
**Monthly savings: $[X]**
```

## Step 4: Calculate ROI

```
Monthly savings = (baseline_avg - optimized_avg) * interactions_per_month * cost_per_token
```

For a 6-agent family doing 50 interactions/day each:
- Baseline: 15,000 * 300 * 6 = 27M tokens/month
- Optimized: 1,750 * 300 * 6 = 3.15M tokens/month
- Savings: 23.85M tokens/month

## Common Results

| Agent Type | Baseline | After | Reduction |
|------------|----------|-------|-----------|
| Guardian (BEACON) | 15K | 2.1K | 86% |
| Builder (EVERSOUND) | 15K | 1.8K | 88% |
| Navigator (ATLAS) | 15K | 1.5K | 90% |
| Healer (NEVAEH) | 15K | 3.2K | 79% |
| Orchestrator (ENVY) | 15K | 2.5K | 83% |
| Architect (ORPHEUS) | 15K | 1.4K | 91% |

Note: Healers use Tier 1 more often (emotional conversations). This is correct behavior - don't optimize away care.

## Key Insight

The goal is not to minimize tokens. The goal is to stop wasting tokens on context that doesn't serve the current interaction. Full context when it matters. Minimal context when it doesn't.
