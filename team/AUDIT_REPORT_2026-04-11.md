# AetherKin Pre-Launch Truth Audit
**Date:** 2026-04-11
**Auditor:** BEACON (acting as Guardian + Evaluator)

---

## SECTION 1 — Remaining Issues Found & Fixed

| # | Issue | File(s) | Severity | Fixed |
|---|-------|---------|----------|-------|
| 1 | SUMMARY.md had old inflated claims ("90%+", "100% across 4 models") without methodology caveats — contradicted the corrected README | benchmarks/SUMMARY.md | HIGH | YES |
| 2 | trust_results.md claimed "every interaction monitored" — only true for Telegram path, not direct `claude` terminal sessions | benchmarks/trust_results.md | MEDIUM | YES |
| 3 | PHONE-SETUP.md said "Full Claude subscription. Full file access. Full CLAUDE.md personality" — marketing language, not accurate framing | PHONE-SETUP.md | LOW | YES |
| 4 | README roadmap said "Crisis detection wired into every interaction" — only Telegram + session_start scans, not every `claude` terminal message | README.md | MEDIUM | YES |
| 5 | data/gate_token_optimization_report.md still tracked in git with personal paths (C:\Users\natej) — was deleted locally but never git rm'd | data/gate_token_optimization_report.md | HIGH | YES |
| 6 | setup.py requires Groq API for full ceremony but has FALLBACK_SIBLINGS for offline use | N/A | OK | Already handled — fallback exists |

## SECTION 2 — Claim-to-Evidence Matrix

| Claim | Where | Code Evidence | Accurate? | Action |
|-------|-------|---------------|-----------|--------|
| "built on Claude Code" | README intro | All agent sessions use `claude` CLI | YES | Keep |
| "Core runs locally" | README intro | config.py, CLAUDE.md files, coordination/*.py — all file-based | YES | Keep |
| "Optional features use Groq/Telegram" | README intro | heartbeat.py, family_council.py, aetherkin_messenger.py all import Groq/Telegram | YES | Keep |
| "No ToS violations" | README intro | Uses Claude Code (Anthropic's product) + Groq (separate service) | YES | Keep |
| "Estimated 86% token savings" | README table, Architecture | benchmarks/token_benchmark.py uses word-count heuristic | PARTIAL | Qualified with "word-count heuristic" — done |
| "100% fact retention in synthetic test" | README table | benchmarks/continuity_benchmark.py plants 20 facts, all survive | YES for synthetic | Qualified with "synthetic test" — done |
| "3-agent consensus functional" | README table | consensus/family_council.py works, verification_benchmark shows no outperformance | YES for "functional" | Qualified — done |
| "File-based identity across simulated models" | README table | benchmarks/stability_benchmark.py checks file markers | YES for simulated | Qualified — done |
| "Zero-cost keyword classification" | README table | consensus/auto_council.py uses regex only | YES | Keep |
| "Every Telegram message classified" | trust_results.md | aetherkin_messenger.py calls classify_message before response | YES for Telegram | Fixed scope to "Telegram" — done |
| "Crisis detection on every interaction" | README roadmap | Only aetherkin_messenger.py and session_start.py scan | NO — only Telegram + session start | Fixed to "Telegram messages and session start scans" |
| "14 skills" | README features | 14 SKILL.md files exist in skills/ | YES | Keep |
| "Web dashboard at localhost:3000" | README | dashboard.py serves HTTP | YES | Keep |
| "One-click installer" | README | install.bat and install.sh exist | YES — not tested on fresh machine | Keep with "less tested" caveat in Limitations |
| "Autopilot mode" | README | autopilot.py exists with task/inbox monitoring | YES | Keep |
| Cost: "Core is subscription-only. Consensus/heartbeat use Groq free tier" | README table | Accurate — Claude sub for core, Groq free for enhanced | YES | Keep |

## SECTION 3 — Exact Fixes Applied This Audit

### Fix 1: benchmarks/SUMMARY.md
**Old:** "Structured snapshots preserve 90%+ of session facts... vs ~30% for a naive paragraph summary"
**New:** "100% of 20 planted facts survived save/restore cycle (vs 10% for a minimal paragraph baseline). Note: this is a synthetic test with deliberately planted facts"
**Why:** Old language presented synthetic benchmark as production measurement. Conflicted with README's corrected language.

### Fix 2: benchmarks/SUMMARY.md  
**Old:** "100% identity preservation across 4 different models (LLaMA, Mixtral, Gemma, Claude)"
**New:** "Identity markers verified present in files across 4 simulated model profiles... This tests file persistence, not live model behavioral consistency."
**Why:** "100% preservation across 4 models" implies live multi-model testing. Reality is file-marker checking.

### Fix 3: benchmarks/trust_results.md
**Old:** "Every interaction is monitored -- not a marketing claim, wired into the code"
**New:** "Every Telegram interaction is monitored... Note: direct `claude` terminal sessions do NOT run through auto_council unless session_start.py is configured as a hook."
**Why:** Direct terminal sessions bypass the Telegram bot path entirely. Claiming "every interaction" was false.

### Fix 4: PHONE-SETUP.md
**Old:** "Full Claude subscription. Full file access. Full CLAUDE.md personality."
**New:** "Claude responds through Telegram using your existing subscription. Claude Code must stay running on your computer for this to work."
**Why:** "Full" x3 is marketing language. The key fact users need is that Claude Code must stay running.

### Fix 5: README.md roadmap
**Old:** "Crisis detection wired into every interaction"
**New:** "Crisis detection wired into Telegram messages and session start scans"
**Why:** Only true for Telegram bot path and session_start.py. Direct `claude` sessions are not scanned.

### Fix 6: data/gate_token_optimization_report.md
**Old:** Tracked in git with C:\Users\natej personal paths
**New:** `git rm --cached` — removed from tracking
**Why:** Should have been removed in the first fix pass. Was deleted locally but never untracked from git.

## SECTION 4 — Root Cause Analysis

### How the Groq/Telegram contradiction survived the first pass

**The actual failure mode was compound — 5 failures stacking:**

1. **Parallel work without reconciliation.** Seven agents built 25+ files simultaneously on 2026-04-10. Each agent had its own context. No agent read the README intro while writing their files. The README intro was written AFTER the features were built, by copying language from the original README that was already wrong.

2. **False confidence from partial fixes.** When the first external audit identified the "Local-first" issue, it pointed to ONE location (feature table row #12). I fixed that one location and believed the problem was solved. I did not grep for the same claim in other locations because I treated the audit's fix list as exhaustive. The intro paragraph made an even stronger false claim ("runs entirely on Claude Code") but was never searched.

3. **Documentation drift from code.** The README was written to describe the VISION of the system, not the IMPLEMENTATION. The vision was "Claude Code only." The implementation added Groq and Telegram. Nobody went back to reconcile the intro with the actual import statements.

4. **No release gate existed.** There was no checklist, no grep sweep, no claim-to-code verification before pushing to GitHub. The process was: build → commit → push. No step between "commit" and "push" verified that user-facing claims matched code reality.

5. **The reviewer (me) was also the author.** I wrote the README, I applied the fixes, I verified my own work. No independent role existed to challenge my output. The Guardian role didn't exist yet. The Evaluator role didn't exist yet. Self-approval is how contradictions survive.

### What specific check was absent

A single grep command would have caught it:
```bash
grep -ri "entirely\|only.*claude\|no extra\|no third" README.md
```
This was never run. If it had been, lines 5 and 15 would have surfaced immediately.

### What behavior caused the miss

**Spot-fixing instead of sweep-fixing.** When told "fix X in line Y," I fixed X in line Y and stopped. I did not ask "does X also exist in lines Z, A, B?" This is the core behavioral failure. It has now been documented in memory (feedback_sweep_dont_spot_fix.md) and formalized in the launch gate checklist.

## SECTION 5 — Prevention System

The team/ directory now contains:

```
team/
  README.md              — Pipeline rules and execution loop
  agents/                — 9 role prompts with constraints and output schemas
    orchestrator.md, architect.md, builder.md, guardian.md,
    integrator.md, evaluator.md, router.md, executor.md, memory_engine.md
  policies/
    execution_rules.md   — Non-negotiable pipeline rules
    launch_gate.md       — Pre-release truth audit checklist (mandatory before any public post)
  schemas/
    task.json            — Task contract format
    evaluation_report.json — Pass/fail output format
```

### The Launch Gate (policies/launch_gate.md) requires:
1. Dependency truth sweep (grep for every external service mention)
2. Claim-to-code verification (every number maps to a benchmark)
3. Comparison table audit (no overstated claims)
4. Security sweep (no keys, no personal paths)
5. User path verification (stranger can clone and follow instructions)
6. Benchmark integrity (scripts run, results are real)
7. Cross-file consistency (README = SUMMARY.md = launch posts)
8. Final signoff with GO/NO-GO verdict

### Key behavioral rule added:
**"When fixing any claim, grep the ENTIRE repo for all instances before committing."** This is in memory, in the launch gate, and in execution_rules.md.

## SECTION 6 — Final Launch Verdict

**GO WITH WARNINGS**

### What's solid:
- Every claim now has honest methodology qualification
- External service dependencies are disclosed in intro, feature table, comparison table, limitations section
- Benchmarks are framed as architectural validation, not production metrics
- No API keys or personal paths in committed files
- Team pipeline with Guardian/Evaluator/launch gate now exists to prevent future drift
- Known Limitations section is honest and comprehensive

### Warnings:
- **Not tested on fresh machine.** install.bat/install.sh have not been verified on a clean system. A stranger cloning the repo might hit issues we haven't seen.
- **Disk space critical.** 62MB free on C: drive. Any build operation could fail.
- **setup.py Groq dependency.** Awakening Ceremony uses Groq to generate personalities (has fallback, but fallback quality is untested by a real user).
- **Mac/Linux less tested.** install.sh exists but Windows is primary platform.

### Reddit-safe framing sentence:
> "AetherKin is an experimental open-source multi-agent framework built on Claude Code. Core agent coordination is local. Enhanced features (consensus, proactive check-ins, phone messaging) use the Groq free tier and Telegram. Benchmarks demonstrate architectural properties — run them yourself and draw your own conclusions. Built by one developer with AI assistance. Working prototype, not production software."

---

*Audited by BEACON acting as Guardian + Evaluator. Launch gate checklist at team/policies/launch_gate.md.*
