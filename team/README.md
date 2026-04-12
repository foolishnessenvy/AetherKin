# AetherKin Controlled Intelligence Pipeline

This is not a team of chatbots. This is a deterministic execution organism.

Every role has power derived from constraints. Without constraints, you get 10 voices hallucinating together. With them, you get an engine that builds things that actually work.

No agent self-approves. No freeform cross-talk. Every output is structured JSON. Every handoff goes through Orchestrator. If it is ambiguous, it goes back. If it fails three times, a human decides.

## Execution Loop

```
USER INPUT
  -> ROUTER (classify intent, detect risk)
  -> ORCHESTRATOR (decompose, assign, track)
  -> ARCHITECT (define contracts, interfaces)
  -> BUILDER (implement exactly to spec)
  -> GUARDIAN (attack everything, find failures)
  -> INTEGRATOR (connect parts, verify data flow)
  -> EVALUATOR (pass/fail, no maybes)
  -> ORCHESTRATOR (final decision, deliver or rework)
```

## Hard Rules

1. Builder cannot invent architecture
2. Architect cannot write production code
3. Router cannot execute tasks
4. Evaluator defines truth, not Builder
5. All communication flows through Orchestrator -- no direct agent-to-agent
6. No agent can self-approve its own output
7. Schema validation at every boundary -- invalid JSON halts the run
8. 3 rework failures = escalate to human
9. Guardian veto power on security, policy, and integrity violations
10. "Almost working" is not working

## Agents

See `agents/` for each role's mission, constraints, and required output schema.

## Policies

- `policies/execution_rules.md` -- the law of the pipeline
- `policies/launch_gate.md` -- pre-release truth audit

## Schemas

- `schemas/task.json` -- task contract format
- `schemas/evaluation_report.json` -- evaluation output format

---

*Discipline is love. Constraints are power. The work here impacts the world.*
