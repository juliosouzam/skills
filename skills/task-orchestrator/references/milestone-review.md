# Milestone Deep Review Gate

Read only after every Task in the current Milestone is integrated and all
Milestone integration gates pass. This gate runs before any target branch is
changed.

## Authority and boundary

Use the workspace-local `$deep-review` skill as a read-only reviewer. It may
write only review artifacts. It never edits source, applies fixes, changes a
Task, or publishes to GitHub.

Architecture, accepted ADRs, Tech Lead planning, and Task contracts remain
authoritative. A review finding is evidence of a possible violation, not
authority to add behavior, redesign the system, or expand scope.

Do not use `--publish`. Publishing requires separate explicit authorization.
If `$deep-review` or a required bundled script cannot be loaded, repair the
local review tooling and rerun; an unavailable review gate is never approval.

## Entry conditions

For every repository touched by the Milestone, require:

- all Milestone Task branches already integrated into its Milestone integration
  branch;
- a clean integration worktree and recorded integration HEAD;
- all Task, wave, Milestone, and repository gates passing at that HEAD;
- the latest target-branch commit merged into the integration branch;
- the exact target commit used as review base recorded;
- no source-writing agent active in the review checkout.

If the target branch moves later, the approval becomes stale. Merge the new
target commit, rerun all gates, and run another review round before landing.

## Review artifacts and checkpoint

Use one persistent output directory per repository:

```text
execution/orchestration/milestones/<MILESTONE-ID>/deep-review/<REPO-ID>/
```

Use the repository key already stored in `plan.yaml`; when it has no key, use
its stable one-based plan order plus root basename, such as `001-api`.

Keep this output outside the frozen review checkout. When the canonical
`.discovery` tree is inside the target repository, write through the
orchestrator's separate evidence workspace and never stage review artifacts as
product changes.

Store the repository identity, base SHA, reviewed HEAD, round, engine, verdict,
open defect counts, coverage, spec conformance, artifact paths, repair history,
and a fingerprint of the loaded `$deep-review` SKILL/references/scripts/assets in
the Milestone checkpoint. A changed tool fingerprint invalidates an unfinished
round. Use these review states:

```text
pending
reviewing
repairing-review
review-approved
escalation-required
```

The canonical human artifacts are `review.md` and `review.html`; the canonical
machine artifacts are `manifest.json`, `findings.json`, `review-stats.json`, and
`state.json`. Never infer approval from chat output.

## Conformance contract

Create:

```text
execution/orchestration/milestones/<MILESTONE-ID>/deep-review/contract-sources.md
```

This is a fingerprinted index, not a new specification. List each authoritative
path, role, and content hash:

- `02-architecture.md` and every accepted ADR cited by the Milestone or its
  Tasks;
- the Milestone file and all child Task files;
- the applicable coverage, execution-order, production-readiness, contract,
  migration, rollout, and rollback planning entries.

Do not treat execution evidence, review findings, or the index itself as product
requirements. Execution evidence may prove what ran; repository instructions,
review configuration, and applicable project skills are review rubric sources.

When `$deep-review --spec <contract-sources.md>` builds `context-pack.md`, its
`Spec contract` section must list every actual authoritative source from the
index, not only the index file. Always include the `spec-parity` sweep.

## Run one frozen review per repository

Review the net Milestone diff only:

```text
base = latest target-branch commit merged into the Milestone integration branch
head = current green Milestone integration HEAD
```

Create or resume a dedicated detached review worktree at `head`:

```text
path: <repo>/.worktrees/<feature>/<milestone>/deep-review-<repo-id>
```

Run from that clean checkout:

```text
$deep-review --base <base> --spec <contract-sources.md> \
  --subagent native --full --out <repository-review-output>
```

The first round is full. Later rounds reuse the same output directory and omit
`--full`, except when code did not change and a claimed false positive requires
a complete re-evaluation.

Honor every `$deep-review` stage and script gate. The source remains frozen from
manifest creation through `render_review.py` and `render_html.py`. Do not repair
code during a running round. A freeze failure restarts the round from the
manifest; a provider interruption resumes pending jobs without rerunning valid
outputs.

Reuse an earlier linter result only when its command, configuration, and HEAD
exactly match the frozen review. Otherwise rerun the lane. Linter unavailability
is reported as required by `$deep-review`; it does not replace the already
mandatory Milestone gates.

In addition to `spec-parity`, add at most one triggered sweep, using this stable
risk order when several apply:

```text
security -> migrations -> contracts -> tests -> config -> consistency
```

All selected hunk lines still receive the normal defect and polish lanes.

## Strict approval rule

A repository review passes only when:

- every `$deep-review` bootstrap, validation, merge, and render gate exits 0;
- manifest accounting, defect coverage, polish coverage, and bound-rule
  coverage are complete;
- the rendered verdict is `SHIP`;
- **zero open defects of any severity** remain;
- the `spec-parity` sweep covers every contract source with zero violation;
- the manifest's reviewed HEAD equals the current integration HEAD.

This is deliberately stricter than the native `$deep-review` verdict, which can
return `SHIP` with Minor defects. Advisories never block approval and are not
automatically implemented or converted into unplanned Tasks.

An empty review selection passes only when the manifest accounts for every diff
path as intentionally ignored or skipped and the existing Milestone gates prove
the corresponding generated or non-reviewable artifacts. Record
`nothing-reviewable`; never pretend cohorts ran.

Every repository must pass before any repository lands.

## Finding ownership and repair requests

Classify every open defect from its causal path and approved write ownership:

- Task-owned defect: return it to that Task executor;
- cross-Task wiring or integration defect: repair it on the Milestone
  integration branch;
- planning or architecture defect: escalate to the Tech Lead or Software
  Architect.

Group all Task-owned defects for the same Task and round into one request:

```text
execution/orchestration/milestones/<MILESTONE-ID>/deep-review/
  repair-requests/ROUND-NNN/<TASK-ID>.md
```

The request records the repository, review round, base and reviewed HEAD,
finding fingerprints, class/severity, exact anchors, causal certificates,
contract sources, expected behavior, and why the Task owns the repair. It must
contain defects only; advisories cannot reopen a Task.

Create an isolated repair branch/worktree from the current Milestone integration
HEAD:

```text
branch: orchestrator/<feature>/<milestone>/review-<round>/<task>
path:   <repo>/.worktrees/<feature>/<milestone>/review-<round>/<task>
```

Invoke exactly:

```text
$task-execute <feature> <TASK-ID> --repair-request <request-path>
```

Independent Task repair requests from one round may run in parallel only when
their dependencies, write scopes, and contracts do not overlap. Merge successful
repair branches without squashing in stable Task-ID order, rerun targeted and
full Milestone gates, then start the next review round.

The orchestrator owns a cross-Task repair only when it fits the union of already
approved Task contracts. Commit it separately with the Milestone and review
round. A repair may not introduce a new decision.

If the executor proves a finding invalid without changing code, preserve the
refutation and run a full review round at the same HEAD. Only the new canonical
review may resolve the finding; neither the executor nor orchestrator may
silently dismiss it.

## Review repair loop

Interpret results as follows:

- `FIX_BEFORE_SHIP`: repair every open defect and re-review;
- `SHIP` with Minor defects: repair the Minor defects and re-review;
- `SHIP` with zero defects: mark the repository `review-approved`;
- `REWORK`: preserve all artifacts and escalate the structural cause;
- invalid/incomplete pipeline: repair the review pipeline or resume pending
  jobs; never treat it as application approval.

Continue while each round produces a contract-compliant repair or new evidence.
If the same fingerprint remains open after three evidence-backed repair rounds
with no new path to progress, escalate the missing Task, planning, or
architecture authority. Do not loop blindly or invent a workaround.

## Landing invariant

Immediately before landing, prove for every repository that the approved review
HEAD still equals its integration HEAD and the recorded review base is the
latest target commit merged into that integration branch. Any drift returns the
Milestone to integration gates and review.

After all repositories are review-approved, land them through the normal
Milestone rules, rerun complete gates on the actual target branches, record the
review artifacts in the Milestone report, remove only clean detached review
worktrees, and only then allow Milestone `done`.
