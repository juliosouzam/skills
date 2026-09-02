---
name: task-orchestrator
description: Explicitly invoked workflow that executes every approved Task one Milestone at a time, using dependency-safe worktrees, automatic in-scope repair, a mandatory Deep Review gate, deterministic integration, and resumable evidence until all Milestones are green on main.
---

# Task Orchestrator

Use only when explicitly invoked. One invocation manages the complete Tech Lead
plan through all Milestones; it does not require confirmation between Tasks,
waves, or successful Milestones.

## Invocation and authority

```text
$task-orchestrator NNN-feature-slug
```

Read completely:

```text
.agents/discovery-protocol.md
references/orchestration-rules.md
.discovery/<feature>/metadata.yaml
.discovery/<feature>/03-implementation-plan.md
.discovery/<feature>/epics/
.discovery/<feature>/milestones/
.discovery/<feature>/tasks/
.discovery/<feature>/planning/dependency-graph.md
.discovery/<feature>/planning/execution-order.md
.discovery/<feature>/planning/open-decisions.md
```

Also follow every applicable `AGENTS.md` and repository rule. Require generated
planning, zero open decisions, every Task `ready`, and a complete acyclic Task
graph.

The Tech Lead owns scope, hierarchy, dependencies, and contracts. The
orchestrator never edits architecture, ADRs, Epics, Milestones, Tasks, or
planning. It owns execution snapshots, branches, worktrees, Task agents,
integration repairs, merges, verification, evidence, resume, and cleanup.
`$task-execute` remains the only workflow that implements an individual Task.

## Compile deterministic Milestones

Persist an executable snapshot and checkpoint under:

```text
.discovery/<feature>/execution/orchestration/
```

Build a Milestone DAG from the Task DAG: for every cross-Milestone Task edge,
add the corresponding Milestone edge. Use a stable topological order, preserving
the Tech Lead order and then IDs for ties. Within each Milestone, compile maximal
safe Task waves from its induced DAG.

Validate that every Task appears once, belongs to one Milestone, every external
dependency is integrated by an earlier Milestone, wave members are independent,
and the aggregate Milestone graph has no cycle. If the Task graph requires
Milestones to interleave, return the exact conflict to the Tech Lead; do not
change hierarchy or dependencies.

Fingerprint every authoritative planning input. On resume, reconcile the
fingerprint, checkpoint, Git state, Task evidence, commits, and actual ancestry
before doing new work.

## Execute one Milestone at a time

Never overlap Milestones and never create a future-Milestone worktree. For the
current Milestone:

1. Verify the current `main` baseline and discover the exact required gates in
   every target repository.
2. Create or resume one Milestone integration branch/worktree per repository
   from the verified baseline.
3. For the next Task wave, create or resume one isolated branch/worktree per
   Task from the current Milestone integration commit.
4. Run one `$task-execute <feature> <TASK-ID>` agent per independent Task.
5. Reconcile every result. Resume and repair incomplete or recoverable Tasks in
   their existing worktrees until they prove `done`.
6. Merge successful Task branches into the Milestone integration branch in the
   compiled order; resolve conflicts semantically and run wave gates.
7. Start the next wave only after the current wave is integrated and green.
8. After all Tasks are integrated, synchronize any `main` drift and run the
   full Milestone and repository gates.
9. Read [references/milestone-review.md](references/milestone-review.md). Run a
   frozen `$deep-review` for every repository, repair all defects, and repeat
   until every current integration HEAD is review-approved.
10. Recheck `main`; any drift invalidates approval and returns to step 8.
    Otherwise merge the Milestone and rerun complete gates on actual `main`.
11. Record proof, clean only merged worktrees/branches, mark the Milestone
    `done`, and advance automatically.

Task branches for later waves start from the latest green Milestone integration
commit, so completed predecessor behavior is present without partially merging
the Milestone into `main`.

## Repair without interrupting recoverable flow

Do not stop at the first Task, test, merge, worktree, tooling, or integration
problem. Diagnose its root cause and route it deterministically:

- Task-owned defect or incomplete evidence: resume `$task-execute` in the same
  Task worktree;
- Task-owned Deep Review defect: create a review repair worktree from the
  current integration HEAD and invoke `$task-execute` with the canonical repair
  request;
- merge conflict or cross-Task integration defect: fix it on the Milestone
  integration branch within the approved contracts;
- failing targeted or full gate caused by the Milestone: fix, add only required
  regression coverage, and rerun affected plus full gates;
- transient command, network, or service failure: apply the recorded bounded
  retry policy;
- stale but valid worktree/branch: verify identity and resume it;
- unrelated name collision: preserve it and create a new recorded deterministic
  path; never delete unknown work;
- `main` drift: integrate the new baseline into the Milestone branch, resolve,
  and rerun all gates.

Keep other independent Tasks in the current wave running while one is repaired.
Do not start a dependent wave or later Milestone early. Never weaken a test,
skip a gate, choose conflict sides wholesale, discard work, or change an
approved decision merely to keep moving.

## Milestone completion gate

A Milestone is `done` only when:

- every child Task is proven `done` with valid evidence and reachable commits;
- every Task commit is integrated exactly once;
- all conflicts and integration repairs are committed and evidenced;
- all applicable Task, Milestone, and repository gates pass on the integration
  branch and actual `main`;
- every repository has a complete `$deep-review` report for its current
  integration HEAD with `SHIP`, zero open defects of any severity, and complete
  spec conformance;
- every touched repository contains the verified Milestone result;
- the checkpoint is current and only merged temporary worktrees/branches were
  cleaned.

Do not advance on partial implementation, a green branch not merged to `main`,
missing evidence, unavailable gates, or failing checks. Final orchestration is
`done` only when every Milestone passes this gate and final `main` is green.

## Escalation boundary

Pause only after exhausting safe in-scope repair when continuation requires a
new product, architecture, planning, hierarchy, dependency, or contract
decision; missing permission or credentials; an unauthorized destructive or
remote action; an unavailable required external system after bounded retries;
unisolatable user changes; a review-proven structural `REWORK`; the same review
defect surviving three evidence-backed repair rounds without progress; or
repository damage that cannot be repaired non-destructively.

Persist the exact state, attempts, worktrees, commits, and required upstream
action. Preserve all unfinished work so the same invocation can resume. These
boundaries are not permission to invent a workaround.

Never push, open pull requests, rewrite public history, force-update branches,
or delete unmerged work unless separately authorized.

## Final response

Report the feature, final status, Milestones and waves completed/resumed, Task
and integration commits, conflicts and repairs, Deep Review verdicts/artifacts,
final-main gates, cleaned or preserved worktrees, evidence path, and any true
escalation.
