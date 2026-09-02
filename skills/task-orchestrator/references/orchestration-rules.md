# Task Orchestration Rules

Read completely before orchestrating a feature.

## Authority

Apply this order:

1. system safety, permissions, and applicable repository instructions;
2. `.agents/discovery-protocol.md`;
3. approved architecture and ADRs cited by affected Tasks;
4. Tech Lead hierarchy, dependency graph, execution order, and gates;
5. individual Task contracts;
6. Task execution evidence;
7. local repository patterns that do not conflict with higher authority.

The orchestrator executes the plan; it does not repair planning or architecture.
At the same authority level, a material conflict is escalated with exact
evidence rather than resolved by preference.

Read [milestone-review.md](milestone-review.md) completely only after the
current Milestone is integrated and green, before review or landing.

## Compile the executable plan

Persist:

```text
execution/orchestration/plan.yaml
execution/orchestration/status.yaml
```

`plan.yaml` records:

```yaml
feature: NNN-feature-slug
target_branch: main
plan_fingerprint: "..."
milestones:
  - id: MILESTONE-NNN
    epic: EPIC-NNN
    order: 1
    dependencies: []
    tasks: [TASK-NNN]
    waves:
      - id: WAVE-NNN
        tasks: [TASK-NNN]
    repositories:
      - path: "..."
```

Fingerprint metadata, the implementation plan, every Epic/Milestone/Task,
dependency graph, execution order, open decisions, and referenced planning
gates. Do not copy Task bodies into the snapshot.

Compile in this order:

1. prove each Task occurs once and has exactly one Milestone and Epic;
2. validate every Task edge and the global Task DAG;
3. for each cross-Milestone Task edge `A -> B`, add
   `milestone(A) -> milestone(B)`;
4. deduplicate Milestone edges and prove the aggregate graph is acyclic;
5. topologically sort Milestones, using declared Tech Lead order and then ID as
   stable tie-breakers;
6. within each Milestone, topologically layer its Tasks into maximal safe waves;
7. verify every external Task dependency belongs to a completed earlier
   Milestone and every same-wave Task is independent in dependencies, write
   scope, exclusive resources, and contracts.

If the aggregate graph cycles, the Task plan requires Milestone interleaving
and is incompatible with Milestone-at-a-time execution. Escalate the exact Task
edges to the Tech Lead. Never move a Task, remove an edge, or change a contract.

## Persistent checkpoint

Use this conceptual state:

```yaml
feature: NNN-feature-slug
status: in-progress
plan_fingerprint: "..."
current_milestone: MILESTONE-NNN
current_wave: WAVE-NNN
milestones:
  - id: MILESTONE-NNN
    status: pending
    base_commits: {}
    waves: []
    repositories: []
    review: null
escalation: null
```

Allowed orchestration/Milestone states are:

```text
pending
in-progress
repairing
reviewing
repairing-review
review-approved
landing
done
escalation-required
```

Write after every material transition: worktree creation, Task result, repair,
merge, gate, review round, main movement, cleanup, or escalation. Record actual
command results without invented timestamps.

Write reports under:

```text
execution/orchestration/milestones/<MILESTONE-ID>/report.md
execution/orchestration/milestones/<MILESTONE-ID>/waves/<WAVE-ID>.md
```

Reports contain branches, worktrees, base and Task commits, merge/integration
commits, conflicts, repairs, review rounds/verdicts/artifacts, commands,
results, landing commits, and cleanup.

## Resume and reconcile

On every invocation or continuation:

1. recompute the plan fingerprint;
2. read the checkpoint and all current-Milestone Task evidence;
3. inspect Git worktrees, branches, commits, ancestry, and repository state;
4. reconcile recorded state with observable state before acting;
5. resume the earliest incomplete transition; never replay a completed one.

If authoritative planning changed, identify the exact diff and escalate for
Tech Lead review. Do not silently execute a changed contract.

Interpret Task execution state as follows:

- missing: pending;
- `in-progress`: resume the same worktree;
- legacy `failed`: preserve its attempt and resume automatically;
- `blocked`: read the cause; resume if it is now solvable within the existing
  contract, otherwise mark the Milestone `escalation-required`;
- `done`: require success evidence, valid commits, clean Task scope, and proof
  of integration before treating it as complete.

An agent/runtime interruption is resumable. Verify no previous process still
owns the worktree, then invoke a replacement Task agent in the same worktree.
Never create duplicate Task executions to hide uncertain state.

## Repository baseline

Before each Milestone in every target repository:

1. identify the repository and target branch selected by the user or `main`;
2. read repository instructions and discover exact gates from CI, manifests,
   scripts, and Task contracts;
3. capture the target commit and validate it in a clean dedicated baseline
   worktree, preserving any dirty user worktree untouched;
4. run the full required baseline gates;
5. inspect existing worktrees and branches before creating new ones;
6. fetch only with explicit remote authorization.

Diagnose a non-green baseline. Repair local tooling/configuration only when
authorized and non-product-changing. A code defect unrelated to the current
Milestone is not absorbed into its Tasks; persist it as an escalation. Never
weaken a gate or modify user work to manufacture a green baseline.

## Branch and worktree ownership

Use one Milestone integration branch/worktree per touched repository:

```text
branch: orchestrator/<feature>/<milestone>/integration
path:   <repo>/.worktrees/<feature>/<milestone>/integration
```

Use one isolated Task branch/worktree:

```text
branch: orchestrator/<feature>/<milestone>/<wave>/<task>
path:   <repo>/.worktrees/<feature>/<milestone>/<wave>/<task>
```

The Milestone branch starts at the verified baseline. Every wave's Task
branches start at the current green Milestone integration commit. Never run two
Task agents in one worktree or create a future-Milestone worktree.

If a deterministic branch/worktree already exists, verify its repository,
feature, Milestone, Task, base, checkpoint, and commits. Resume it when all
match. For an unrelated collision, preserve it and select the lowest available
`-rNNN` suffix for both recorded branch and path. Never delete or overwrite
unknown work.

Keep worktrees under an ignored repository-local directory. Use Git worktree
commands and repository-local exclude metadata where appropriate; do not add
product files solely for orchestration.

## Run and repair Tasks

Launch one Task agent per Task in the current wave, up to available capacity.
Its directive invokes exactly:

```text
$task-execute <feature> <TASK-ID>
```

Each agent operates only in its assigned worktree, implements one Task, follows
its contract, creates scoped commits/evidence, and never merges, rebases,
changes planning, or manages another worktree.

On a recoverable result, do not stop the orchestration:

- incomplete implementation, failing Task gate, or incomplete evidence:
  resume the same Task executor;
- agent/runtime failure: replace the agent and resume the same state;
- transient external/tool failure: apply the Task's bounded retry rule;
- prerequisite absent from the Task base: repair orchestration order/base, not
  application behavior;
- true missing decision/permission/external state: preserve the Task and mark
  the Milestone escalation without advancing.

Let all already-launched independent Tasks reach a safe persisted result while
one Task is repaired. Successful sibling Tasks may be integrated into the
Milestone branch and preserved, but no dependent wave or later Milestone starts
until the current Milestone can continue.

## Pre-integration Task gate

Before merging a Task branch, prove:

- execution status is `done` with `result: success`;
- recorded implementation and evidence commits exist on the assigned branch;
- evidence matches actual diff and commands;
- every acceptance/DoD item and required gate passed;
- commits contain only Task scope and no unauthorized merge;
- the worktree has no uncommitted Task changes.

If any proof fails, resume `$task-execute`; never edit its result from the
orchestrator. Merge Task branches without squashing so evidence-recorded commit
hashes remain reachable.

## Milestone integration and conflict repair

Merge Task branches into the Milestone integration branch in compiled order,
never completion order. Before each merge, verify the expected base, branch tip,
and commits.

For every conflict:

1. read all affected Task contracts and architecture sources;
2. inspect complete files, history, and nearby tests;
3. preserve the behavior and contracts of every Task;
4. regenerate derived files through their canonical generator when authorized;
5. add only regression tests required to prove the combined behavior;
6. commit the resolution separately with feature and Milestone identity;
7. record files, rationale, tests, and commit.

Never use wholesale `ours`/`theirs`, delete one Task's behavior, disable code,
weaken assertions, skip gates, change scope, or revise an ADR. If approved
contracts cannot coexist, preserve the branch and escalate the exact conflict.

When a merged result fails:

- a Task-owned defect returns to that Task executor when it can be isolated;
- a cross-Task wiring or integration defect is repaired on the Milestone branch
  within the union of approved contracts;
- an environment/transient defect follows the bounded retry rule;
- a planning/architecture conflict escalates.

After every repair, run targeted checks and then the complete affected wave
gate set. The next wave branches only from a green integration commit.

## Milestone gates and landing

After all waves, run the union of every Task gate and all repository-required
tests, build/package, lint/format, typing/static, contract, migration,
integration, race, security, performance, and end-to-end checks that apply.
Unavailable required gates are not passes.

Before landing, detect target-branch movement. Merge the new target commit into
the Milestone integration branch, resolve under the same rules, and rerun all
gates. If the target branch is checked out with user changes that prevent a
safe merge, preserve the validated Milestone branch and escalate instead of
stashing or modifying that work. Do not rebase or force-update shared history.

After the target branch is synchronized and every integration branch is green,
run the mandatory gate in [milestone-review.md](milestone-review.md). Every
repository must be `review-approved` for its exact current integration HEAD
before landing. Any repair or target-branch drift invalidates approval, requires
all affected gates, and starts another review round.

For a multi-repository Milestone:

1. make every integration branch green before changing any target branch;
2. land repositories in the stable order recorded in `plan.yaml`;
3. use auditable merge commits;
4. rerun the full gate set on every actual target branch;
5. if a later landing fails, repair it within contract or create traceable
   revert commits in reverse landing order to restore verified baselines;
6. preserve all Task and integration branches for resume.

Never reset, force-push, or discard commits to hide a failed landing.

## Completion and cleanup

A Milestone is complete only when every Task and integration commit is present
exactly once in each intended target branch, every repository's last reviewed
HEAD is approved under [milestone-review.md](milestone-review.md), all actual
target branches pass, reports/checkpoints are current, and no approved behavior
is missing.

Only then:

1. checkpoint the verified landing, gates, and review artifacts;
2. prove each removable worktree is clean and contains no untracked work, then
   remove its Task, review-repair, Deep Review, integration, and baseline
   worktrees with Git worktree commands;
3. prune worktree metadata;
4. delete only merged temporary branches after proving reachability;
5. verify no completed-Milestone worktree remains;
6. mark the Milestone `done`;
7. start the next Milestone automatically.

Never clean an uncommitted, unmerged, unexplained, or escalation-preserved
worktree. Never push or open a pull request without separate authorization.

Final orchestration is `done` only after all Milestones are complete and final
full gates pass on every target branch.

## Escalation

Do not escalate a recoverable implementation, test, merge, worktree, or tooling
problem. Exhaust safe repairs first. Escalate only for:

- invalid or changed planning, hierarchy, dependency, Task scope, or acceptance
  criteria;
- a required architecture, ADR, contract, ownership, topology, or product
  decision;
- missing permission, credential, remote access, or authorization for a
  destructive action;
- a required external system unavailable after bounded retries;
- user changes that cannot be isolated without risking loss;
- unrelated non-green baseline code;
- a Deep Review `REWORK` or the same open defect surviving three
  evidence-backed repair rounds without progress;
- repository damage that has no non-destructive repair.

Persist `status: escalation-required`, the owner, exact source, impact,
attempted repairs, current branches/worktrees/commits, and the minimum action
needed to resume. Do not start a later Milestone and do not invent a workaround.
