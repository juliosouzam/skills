# Dependency, Parallelization, and Quality Review

Read after all tasks are drafted and before publishing planning.

## Dependency graph

For every dependency, verify:

- both task IDs exist;
- the predecessor produces a concrete input required by the successor;
- the dependency is not merely conventional ordering or shared epic context;
- no cycle exists;
- contract definition precedes dependent integration only when technically
  necessary;
- migration, rollout, and compatibility constraints are represented;
- shared exclusive resources or overlapping write areas are explicit.

Remove artificial dependencies by splitting results, narrowing context, or
making contracts independently available. Do not remove real prerequisites to
create superficial parallelism.

## Parallel execution

Compute a valid topological order and identify:

1. every task that can start immediately;
2. every maximal set of mutually independent tasks;
3. integration points and gates between waves;
4. the technical critical path without dates or duration estimates;
5. the reason for every task that must remain sequential.

`planning/dependency-graph.md` records the proven graph.
`planning/execution-order.md` records immediate tasks, parallel waves,
integration gates, and sequential constraints.

A dependency means “must be complete first”; it is not a reason to mark a
well-defined future task `blocked`. Generated planning contains only ready
tasks and no avoidable block.

## Coverage matrix

Map every architecture inventory item to one of:

```text
Covered
Documentation Only
Already Existing
Not Applicable
```

Every `Covered` item links its milestones, epics, tasks, tests, or readiness
gates. `Decision Required` and `Architecture Conflict` are stopping
diagnostics, never final generated-plan classifications.

## Production readiness

Map each architecture readiness criterion to concrete implementation,
validation, evidence, ownership, and release gates. Search all applicable
forms of security, observability, resilience, backup/restore, migration,
rollout, rollback, capacity, incident response, and operational documentation.
Examples do not create requirements by themselves.

## Final audit

Do not mark planning `generated` unless:

- architecture inventory coverage is complete;
- all IDs and links resolve;
- every task belongs to its intended epic and milestone;
- every task has isolated context and a complete contract;
- dependencies are real and acyclic;
- parallel waves match the graph;
- business and failure behavior has meaningful tests;
- all applicable quality gates appear in each task;
- no task changes architecture;
- no material architecture item disappeared;
- no task is `blocked` or unresolved `draft`;
- no blocking decision or conflict remains.

If any check fails, revise planning within Tech Lead authority or return the
issue upstream. Do not publish partial planning.
