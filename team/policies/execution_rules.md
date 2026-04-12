# Execution Rules — The Law of the Pipeline

These rules are non-negotiable. Breaking any one collapses the system.

## Task Flow
- One task at a time unless explicitly parallelizable
- No agent works without a clear contract from Orchestrator
- If output is ambiguous, send it back — do not guess
- If dependencies are missing, block execution — do not improvise

## Quality Gates
- Schema validation at every stage — invalid JSON halts the run
- Every output must be structured — no prose where JSON is expected
- "Almost working" is failure. "Seems fine" is failure.
- Only measurable, evidenced success passes Evaluator

## Rework
- Rework budget: 3 failures on same task = escalate to human
- Each rework attempt must include what changed and why
- No agent can rework its own output — a different agent must review

## Guardian Vetoes
Guardian has absolute veto power on:
- Security bypass (exposed keys, injection vectors, permission gaps)
- Mode-policy violation (claiming local when using external API)
- Hidden provider dependency (code calls external service not disclosed to user)
- Secret exposure (API keys, personal paths, chat IDs in committed files)
- Misleading claims (README says X, code does Y)

## Accountability
- No agent can self-approve
- Builder does not decide what to build
- Architect does not write production code
- Router does not execute tasks
- Evaluator defines truth, not Builder
- All communication flows through Orchestrator

## Release
- No public release without passing `policies/launch_gate.md` checklist
- Every user-facing claim must map to code evidence
- If a claim is only true in one mode, say which mode
- If a benchmark is synthetic, say synthetic
