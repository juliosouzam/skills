# Task Execution Rules

Read completely before executing a Task.

## Authority

Apply this order:

1. system safety, permissions, and applicable repository instructions;
2. `.agents/discovery-protocol.md`;
3. architecture and accepted ADRs cited by the Task;
4. the Task contract and its dependency/ordering entries;
5. a validated Deep Review repair request as defect evidence only;
6. parent Milestone and Epic context;
7. local repository patterns that do not conflict with higher authority.

At the same level, a material conflict requires escalation; never select the
convenient source. The executor implements one Task and makes no product,
planning, contract, or architecture decision.

## Resolution and readiness

Require exactly one feature and Task argument, at most one
`--repair-request <path>`, and exactly one matching Task file. Use these results
without guessing:

```text
FEATURE_NOT_FOUND
TASK_NOT_FOUND
AMBIGUOUS_TASK
TASK_NOT_READY
WAITING_FOR_DEPENDENCY
WAITING_FOR_DEPENDENCY_INTEGRATION
INVALID_REPAIR_REQUEST
ESCALATION_REQUIRED
```

The Task is executable only when:

- planning status is `ready`;
- `planning/open-decisions.md` has no decision affecting it;
- every declared predecessor has successful `done` evidence;
- every required predecessor implementation is present in the assigned branch
  base, unless planning classifies it as non-executable existing work;
- its repository, scope, contracts, acceptance criteria, and gates are
  unambiguous.

Waiting for a dependency is a scheduling result, not a Task failure and not
permission to bypass the edge.

## Deep Review repair requests

A repair request is valid only when all of these are proven:

- it is the canonical request under the current Milestone's
  `execution/orchestration/milestones/<MILESTONE-ID>/deep-review/` directory;
- it names this Task, Milestone, feature, repository, review round, base SHA,
  and reviewed integration HEAD;
- every referenced fingerprint is an open `defect` in that round's canonical
  `findings.json`; advisories are rejected;
- every anchor and causal path falls within this Task's approved responsibility
  and write scope;
- the assigned repair branch contains the reviewed integration HEAD;
- the requested expected behavior is already required by the Task,
  architecture, or accepted ADRs.

The request may group multiple defects owned by the same Task. It may not add
acceptance criteria, reinterpret a finding, prescribe an architectural change,
or authorize unrelated cleanup. Return `INVALID_REPAIR_REQUEST` with the exact
failed check instead of guessing.

For a valid request against an execution already marked `done`, preserve the
successful prior attempt, start the next numbered attempt, and record the
request path/fingerprints in `00-context.md` and `status.yaml`. A claimed false
positive requires evidence and a later full Deep Review round; the executor
cannot dismiss or close it.

## Repository and worktree pre-flight

The Task must resolve to one Git repository. A multi-repository Task or
ambiguous ownership returns to the Tech Lead.

Before editing, record:

- repository root, branch, worktree path, base commit, and current HEAD;
- `git status` and pre-existing tracked/untracked changes;
- applicable `AGENTS.md` files and exact quality-gate commands;
- relevant implementation and test patterns;
- expected Task write scope.

When invoked by the orchestrator, use only the assigned worktree. Do not create,
remove, or repair other worktrees; merge, rebase, or update the integration or
main branch; or fetch/push without separate authority.

Preserve user work. If pre-existing changes overlap the Task and cannot be
isolated safely, persist evidence and escalate. Never reset, force checkout,
stash, overwrite, or stage unrelated changes merely to proceed.

## Scope

Allowed changes are the implementation required by the Task and its directly
necessary tests, documentation, migration, configuration, security,
observability, and small local refactors.

Not allowed without upstream revision:

- new or changed product behavior;
- weakened acceptance criteria or tests;
- changed public/inter-service contracts, ownership, data authority, selected
  technology, infrastructure topology, or accepted ADRs;
- new services, brokers, datastores, or broad refactors;
- unrelated cleanup or changes assigned to another Task.

Local details are allowed only when reversible, evidence-based, and unable to
affect an architectural decision.

## Execution state and attempts

Canonical evidence lives under:

```text
.discovery/<feature>/execution/<TASK-ID>/
```

New executions use:

```yaml
task: TASK-NNN
feature: NNN-feature-slug
status: in-progress
result: null
attempt: 1
```

Interpret state as follows:

- no state: create attempt 1;
- `in-progress`: resume the same worktree and attempt;
- legacy `failed`: preserve it and resume automatically as a new attempt;
- `blocked`: re-evaluate the recorded cause; resume automatically only when it
  is now resolvable without expanded authority;
- `done`: verify evidence, commits, diff, and gates; return idempotently when
  valid, or preserve and reopen only for a concrete disproving defect backed by
  a valid repair request or equivalent authoritative evidence.

Before a new attempt, move the prior attempt's context, changes, verification,
result, and status snapshot under `attempts/ATTEMPT-NNN/`, using the next
three-digit ID. Never discard or rewrite prior evidence.

Keep recoverable problems `in-progress`. New executions use `blocked` only for
true escalation; `failed` is not a terminal shortcut for an in-scope defect.

## Repair loop

Use this loop until completion:

1. inspect before editing;
2. implement the complete contract;
3. run the smallest diagnostic or targeted check that gives useful evidence;
4. run all affected required checks;
5. run the full Task/repository gate set;
6. classify every failure by root cause;
7. correct in-scope causes and return to step 3.

Do not blindly rerun deterministic failures. A changed repair must have a
reason tied to evidence. For flaky behavior, reproduce the race, ordering,
isolation, time, or state leak and remove it rather than accepting a lucky run.

For a transient external/tool failure, follow its defined retry policy. If none
exists, allow at most three recorded attempts. If the same root cause remains
after three distinct evidence-backed in-scope corrections with no new path to
progress, classify the missing authority or external condition and escalate;
do not loop or invent a workaround.

An unavailable command is not a pass. Repair a missing local prerequisite only
when repository rules authorize it. Do not weaken sandbox, security, or network
controls to make a check run.

## Verification

Verification derives from the Task and repository, not a generic checklist.
It includes, when applicable:

- business success and failure behavior;
- unit, integration, contract, migration, end-to-end, resilience, race,
  performance, and security tests;
- build/package validation;
- lint and formatting;
- typing and static analysis;
- schema, generated artifact, infrastructure, or deployment validation.

Run targeted checks during repair and the full applicable set before success.
Every required command must pass. `NOT_APPLICABLE` requires a concrete Task or
repository reason. Never add coverage-only tests or claim a command was run
when it was not.

## Evidence contract

Maintain:

```text
00-context.md       exact input, dependencies, repository and inspected scope
01-changes.md       actual files and behavior changed; deviations must be None
02-verification.md  commands/results, acceptance/DoD, and repair findings
03-result.md        DONE or ESCALATION_REQUIRED, summary and remaining issue
status.yaml         machine-readable state
```

`02-verification.md` maps every acceptance criterion and applicable Definition
of Done item to direct evidence. Record warnings, skipped checks, retries, and
repairs truthfully. Do not invent timestamps.

Successful state:

```yaml
task: TASK-NNN
feature: NNN-feature-slug
status: done
result: success
attempt: N
commit: "<implementation-commit>"
repair_request: null
repair_findings: []
```

For a repair attempt, replace `repair_request` with its path;
`repair_findings` lists every request fingerprint with disposition `corrected`
or `refuted-pending-review`. Only the orchestrator's subsequent canonical
review can close a finding.

True escalation state:

```yaml
task: TASK-NNN
feature: NNN-feature-slug
status: blocked
result: escalation-required
attempt: N
owner: tech-lead | software-architect | user
reason: "<exact unresolved condition>"
```

Escalation evidence identifies the conflicting source, affected requirement,
attempted repairs, preserved work, and exact decision, permission, credential,
or external condition required.

## Commit and completion

Stage explicit Task-owned paths only; never use `git add -A`. Inspect staged and
unstaged diffs before committing. The implementation commit message includes
the feature and Task IDs. Do not push or open a pull request.

When evidence is outside the target repository, create one implementation
commit and record its hash in external evidence.

When evidence is inside the target repository, avoid the impossible
self-referential commit-hash cycle:

1. commit the implementation and truthful pre-final evidence;
2. record that implementation hash in final result/status evidence;
3. create one evidence-only commit;
4. leave both commits on the Task branch and the worktree clean.

The orchestrator must merge, not squash, these commits so the recorded
implementation hash remains reachable.

Completion requires all contract work, acceptance criteria, Definition of Done,
gates, evidence, and Task-scoped commits to be valid. Code present, a green
targeted test, or a commit alone never proves completion.

## Escalation boundary

Escalate only after exhausting safe in-scope repair when progress requires:

- changing planning, a Task contract, architecture, an ADR, or product intent;
- permission, credentials, remote access, or a destructive action not already
  authorized;
- an unavailable required external system after bounded retries;
- modifying unrelated user work or another Task's responsibility;
- repairing an unrelated non-green baseline;
- resolving repository corruption that cannot be handled non-destructively.

Route decomposition, dependency, scope, or acceptance defects to the Tech Lead;
route architecture, ownership, topology, contract, or product decisions to the
Software Architect. Persist exact state so the same execution can resume.
