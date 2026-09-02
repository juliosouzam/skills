---
name: task-execute
description: Explicitly invoked workflow that completes exactly one ready Tech Lead Task or a verified review-repair attempt in its assigned Git worktree, repairs in-scope failures until every acceptance and quality gate passes, records evidence, and commits only verified Task scope.
---

# Task Execute

Use only when explicitly invoked. Implement and prove exactly one approved
Task. Do not orchestrate other Tasks, merge branches, or manage worktrees.

## Invocation and contract

```text
$task-execute NNN-feature-slug TASK-NNN
$task-execute NNN-feature-slug TASK-NNN --repair-request <path>
```

Resolve exactly one file at:

```text
.discovery/<feature>/tasks/<TASK-ID>-*.md
```

Before changing code, read completely:

```text
.agents/discovery-protocol.md
references/execution-rules.md
the Task, its Epic and Milestone
every architecture source and ADR cited by the Task
the Task entries in planning and dependency artifacts
applicable AGENTS.md files, relevant code, tests, and repository rules
the canonical repair request and cited Deep Review findings, when supplied
```

Require Task planning status `ready`, no blocking decision, and every declared
dependency completed. A dependency controls scheduling; do not work around it.

## Scope lock

The Task, its cited architecture, and accepted ADRs are the implementation
contract. Implement every applicable requirement, scenario, test, acceptance
criterion, and Definition of Done item exactly.

Allowed local choices must be reversible, follow repository evidence, and
preserve architecture, public behavior, contracts, ownership, technology,
data, and infrastructure. Never invent missing behavior, broaden scope, weaken
tests, replace a selected design, or perform unrelated cleanup.

If completion needs a new product, planning, contract, or architecture
decision, record the exact gap and escalate to the Tech Lead or Software
Architect. Do not guess.

## Resume instead of restart

Use:

```text
.discovery/<feature>/execution/<TASK-ID>/
```

Read existing execution state and evidence before acting. Resume
`in-progress`, `failed`, or previously `blocked` work when its recorded cause
is now resolvable within the same contract. Preserve prior attempts; never
erase evidence or repeat completed work.

For existing `done`, verify the commit, evidence, Task diff, and required gates.
Return the proven result idempotently. Reopen only when a concrete in-scope
defect disproves completion, preserving the prior result as an attempt. A Deep
Review repair requires a valid `--repair-request`; an advisory cannot reopen a
Task.

## Review repair boundary

A repair request is defect evidence, not a new requirement. Verify that it is
canonical, targets this Task and repository, cites open Deep Review defect
fingerprints, and starts from a branch containing the reviewed integration HEAD.
Reject invalid ownership, stale requests, advisories, or any remediation that
would change the Task, planning, or architecture.

Resolve every valid finding in the request, add only required regression tests,
and rerun the complete Task gates. Record the request path, fingerprints,
reviewed HEAD, corrections, and verification in the new attempt. The
orchestrator, not this executor, closes findings through the next Deep Review
round.

## Deterministic completion loop

1. Verify the exact Task, dependencies, repository, branch/worktree identity,
   pre-existing changes, applicable instructions, and baseline evidence.
2. Set execution to `in-progress` and record inspected context.
3. Implement the smallest coherent change that fully satisfies the Task,
   including required tests, migrations, configuration, observability,
   security, and documentation.
4. Run targeted checks, then every Task- and repository-required gate.
5. On failure, identify the root cause, make an in-scope correction, and rerun
   the affected checks followed by the full required gate set.
6. Repeat while a contract-compliant repair is available. Do not return on the
   first test, build, lint, type, integration, or tooling failure.
7. Audit acceptance criteria, Definition of Done, diff scope, evidence, and
   worktree state; then create the Task commit and mark `done`.

Handle failures by cause:

- implementation, test, lint, type, build, or task-owned configuration defect:
  fix it and rerun;
- flaky or nondeterministic test: reproduce and remove the cause; do not pass
  it through blind retries;
- transient tool, network, or service failure: use its defined retry policy,
  or at most three evidence-recorded attempts when none exists;
- unrelated baseline defect: prove it is unrelated and return it to the
  orchestrator; do not absorb it into the Task;
- missing decision, permission, credential, unavailable external state, or
  required scope expansion: persist `blocked` with `escalation-required`.

Keep recoverable work `in-progress`; do not finalize `failed` merely because a
repair iteration failed. Never ask the user to choose an implementation detail
already fixed by architecture or repository rules.

## Verification and evidence

Maintain truthful, current evidence:

```text
00-context.md
01-changes.md
02-verification.md
03-result.md
status.yaml
```

Record actual files, commands, results, acceptance criteria, Definition of Done,
warnings, retries, repairs, and deviations. Never fabricate a command result,
timestamp, approval, or passing gate. Required checks may be `NOT_APPLICABLE`
only with concrete Task and repository evidence.

A Task is complete only when:

- its full contract is implemented with no unauthorized deviation;
- every acceptance criterion and applicable Definition of Done item has
  evidence;
- every supplied review-repair defect has a recorded correction or an
  evidence-backed refutation awaiting full re-review;
- success, failure, and every other required test pass;
- build, lint/format, type/static, contract, migration, integration, security,
  and other applicable repository gates pass;
- the final diff contains only Task-scoped changes and preserves user work;
- the successful commit exists on the assigned branch and the intended
  worktree state is clean;
- `status.yaml` says `done` with `result: success` and the commit hash.

Stage explicit paths only; never use `git add -A`. Do not push, merge, rebase
the target branch, open a pull request, or clean another worktree. Evidence
outside the target repository remains required but is not falsely reported as
committed.

## Final response

Report the Task, final status, files changed, checks run, evidence directory,
commit hash, repair-request result when applicable, and any true escalation. A
successful response requires the completion proof above; code written without
passing gates is not success.
