# AetherKin Launch Gate Checklist

Run EVERY item before any public post (Reddit, HN, X, etc.)
A single unchecked item = NO-GO.

## 1. Dependency Truth Sweep
- [ ] `grep -ri "groq\|telegram\|api.groq\|external\|cloud" README.md` — every external service disclosed?
- [ ] `grep -ri "local-first\|local first\|entirely\|only.*claude\|no extra\|no third" README.md` — no misleading locality claims?
- [ ] `grep -ri "subscription\|free\|no cost\|zero cost" README.md` — cost claims match reality?
- [ ] Cross-check: every file that imports requests/groq/telegram is disclosed in README
- [ ] `grep -ri "entirely\|only.*claude\|no third\|no extra" SHARED/LAUNCH/` — launch posts match README?

## 2. Claim-to-Code Verification
- [ ] Every percentage has a benchmark file that produces it
- [ ] Benchmark methodology limitations stated next to every number
- [ ] No benchmark result presented as production-grade unless it is
- [ ] Every feature in feature table has actual working code
- [ ] `python setup.py` runs on fresh clone (or states what it needs)
- [ ] install.bat / install.sh flow matches README instructions

## 3. Comparison Table Audit
- [ ] No competitor feature listed as "Not available" (use "Not built-in")
- [ ] No AetherKin feature overstated vs actual capability
- [ ] Cost comparison honest about external service usage

## 4. Security Sweep
- [ ] .env in .gitignore AND not tracked (`git ls-files .env` returns nothing)
- [ ] `grep -ri "sk-\|gsk_\|bot[0-9]" *.py *.md` — no API keys in committed files
- [ ] `grep -ri "C:\\\\Users\|/home/\|natej" *.py *.md` — no personal paths in committed files

## 5. User Path Verification
- [ ] Stranger can clone → follow README → reach working agent
- [ ] Every "optional" feature clearly marked optional
- [ ] Every feature requiring Groq/Telegram explicitly says so
- [ ] Awakening Ceremony states it needs Groq (or has fallback)

## 6. Benchmark Integrity
- [ ] Every benchmark script runs: `python benchmarks/token_benchmark.py` etc.
- [ ] Results files contain real data (not placeholders)
- [ ] Benchmark limitations paragraph in README
- [ ] SUMMARY.md matches README claim language exactly

## 7. Cross-File Consistency
- [ ] README intro matches body matches comparison table matches SUMMARY.md
- [ ] Launch posts match README claims
- [ ] PHONE-SETUP.md matches README setup instructions
- [ ] requirements.txt covers every import in the codebase
- [ ] Same claim not stated differently in different files

## 8. Final Signoff
- [ ] Guardian has audited for misleading claims
- [ ] Evaluator has verified benchmarks
- [ ] No claim survives that a hostile Reddit user could disprove in 5 minutes
- [ ] VERDICT: GO / GO WITH WARNINGS / NO-GO

---

## How To Run This Gate

```bash
# Dependency sweep
grep -ri "groq\|telegram\|api.groq" README.md
grep -ri "local-first\|entirely\|only.*claude\|no extra\|no third" README.md SHARED/LAUNCH/*.md

# Security sweep
git ls-files .env
grep -ri "sk-\|gsk_\|bot[0-9]" $(git ls-files '*.py' '*.md')
grep -ri "C:\\\\Users\|/home/" $(git ls-files '*.py' '*.md')

# Benchmark run
python benchmarks/token_benchmark.py
python benchmarks/continuity_benchmark.py
python benchmarks/verification_benchmark.py
python benchmarks/stability_benchmark.py

# Cross-file claim check
grep -n "86%" README.md benchmarks/SUMMARY.md
grep -n "100%" README.md benchmarks/SUMMARY.md
grep -n "local" README.md
```
