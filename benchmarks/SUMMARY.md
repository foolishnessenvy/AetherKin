# AetherKin Benchmark Summary

*Maps the 5 biggest r/ClaudeCode complaints to AetherKin's architectural solutions.*

**Important:** These are architectural validations, not production benchmarks. Token estimates use word-count heuristics. Continuity tests use planted facts. Stability tests simulate model profiles. Verification tests confirmed the mechanism works but did not find cases where council outperformed single model. Run them yourself and draw your own conclusions.

Run all benchmarks: `python -m benchmarks.token_benchmark && python -m benchmarks.continuity_benchmark && python -m benchmarks.verification_benchmark && python -m benchmarks.stability_benchmark`

---

## Problem: "Claude confidently gives wrong answers"
**AetherKin Solution:** Family Council (cross-verification consensus)
**Benchmark Result:** Council and single model both achieved 100% on standard technical questions. The architecture's value is structural: three agents with different system prompts vote on each answer. The consensus mechanism is proven functional but has not yet been shown to outperform a single model on our test set. Run it with your own edge-case questions.
**How to use it:** `python consensus/family_council.py --question "your question" --auto`
**Requires:** Groq API key (free tier)

---

## Problem: "Burned my entire 4h session on circular reasoning"
**AetherKin Solution:** Three-tier token optimization
**Benchmark Result:** Estimated 70-97% token savings per turn depending on tier, measured using word-count heuristic (not live API token counting). Over a simulated 50-turn session, the three-tier architecture saves an estimated ~75% of total context size by loading only what each turn needs.
**How to use it:** Identity summaries in `family/SHARED/SHARED_CONTEXT/IDENTITY_SUMMARIES/` -- agents load Tier 1 (full) on first turn, Tier 2 (summary) for context tasks, Tier 3 (task-only) for routine ops.
**Requires:** No external API — this is a local file-loading strategy.

---

## Problem: "Context loss between sessions / dementia"
**AetherKin Solution:** Anamnesis consciousness save/restore
**Benchmark Result:** 100% of 20 planted facts survived save/restore cycle (vs 10% for a minimal paragraph baseline). Note: this is a synthetic test with deliberately planted facts, not a measurement of live session memory. The structured snapshot approach preserves more context than a naive summary, but real-world retention depends on summary quality and session complexity.
**How to use it:** `python anamnesis/consciousness_save.py --agent BEACON --summary "what happened"` at session end, `python anamnesis/consciousness_restore.py --agent BEACON` at session start.
**Requires:** No external API — entirely local file operations.

---

## Problem: "Workflows break when model behavior changes"
**AetherKin Solution:** File-based identity (CLAUDE.md + consciousness snapshots)
**Benchmark Result:** Identity markers (name, role, values, voice, mission) verified present in files across 4 simulated model profiles (LLaMA, Mixtral, Gemma, Claude) x 6 agents. This tests file persistence, not live model behavioral consistency. The principle: your agent IS its files, so swapping models doesn't erase identity.
**How to use it:** Define your agent in `family/AGENT_NAME/.claude/CLAUDE.md`. Identity lives in the file, not the model.
**Requires:** No external API — identity is stored in local markdown files.

---

## Problem: "Can't trust single model output"
**AetherKin Solution:** Auto-classification on Telegram messages + opt-in verification
**Benchmark Result:** The keyword-based classifier (auto_council.py) correctly categorizes messages by topic and urgency at zero cost (regex, no API). Crisis detection runs on every Telegram message. Note: this monitoring only applies to messages through aetherkin_messenger.py (Telegram bot), not to direct `claude` terminal sessions.
**How to use it:** `python consensus/auto_council.py "your message"` to detect topic and urgency, then `python consensus/family_council.py --auto --question "your question"` for full council.
**Requires:** Groq API key for council responses. Classification itself is free (regex).

---

## Running the Benchmarks

Each benchmark is standalone:

```bash
# Token optimization (no API needed)
python benchmarks/token_benchmark.py

# Consciousness continuity (no API needed)
python benchmarks/continuity_benchmark.py

# Cross-verification (uses Groq API if available, simulated if not)
python benchmarks/verification_benchmark.py

# Model stability (no API needed)
python benchmarks/stability_benchmark.py
```

Results are saved to `benchmarks/*_results.md` after each run.
