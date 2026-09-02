---
name: tech-lead
description: Explicitly invoked workflow that turns completed software-architect output into a faithful Epic → Milestone → Task technical plan and an acyclic dependency graph for safe parallel execution.
---

# Tech Lead

Use only when explicitly invoked. Convert approved architecture into an
executable technical plan; do not redesign, simplify, expand, or complete it.

## Architecture contract

Read completely:

```text
.agents/discovery-protocol.md
.discovery/<feature>/01-enriched-prompt.md
.discovery/<feature>/02-architecture.md
.discovery/<feature>/architecture/interview.md
.discovery/<feature>/architecture/decision-tree.md
.discovery/<feature>/adrs/
```

Also read every linked diagram, table, artifact, repository instruction, and
relevant codebase fact. `02-architecture.md` and its accepted ADRs are
authoritative; chat, summaries, and examples are not.

If `02-architecture.md` is missing, stop with:

```text
BLOCKED: architecture specification not found. Run $software-architect first.
```

If any material decision, contract, dependency, owner, component, behavior,
or edge case is ambiguous, absent, or contradictory, report the exact source
and impact to `$software-architect`. Do not guess or publish a partial plan.

## Fixed hierarchy

```text
Architecture
  -> Epics
    -> Milestones
      -> Tasks
```

- Epic: high-level system capability; contains one or more Milestones.
- Milestone: verifiable delivery within exactly one Epic; contains one or more
  Tasks.
- Task: independently implementable and verifiable activity within exactly one
  Milestone.

`Delivery` means Milestone and `activity` means Task; there is no fourth level.
Every child names one parent, every parent lists all direct children, and every
Epic lists its complete descendant Task set.

## Decomposition

Read [references/planning-workflow.md](references/planning-workflow.md). Read
[references/specialized-concerns.md](references/specialized-concerns.md) only
for concerns present in the architecture.

1. Inventory every architecture requirement, ADR, component, resource,
   contract, data rule, flow, edge case, quality attribute, operational rule,
   risk, and readiness gate.
2. Define all Epics, all Milestones under each Epic, and all Tasks under each
   Milestone.
3. Trace every inventory item to work, documentation, proven existing
   behavior, or justified `NOT_APPLICABLE`.
4. Cover exactly the architecture-defined normal, alternate, failure,
   recovery, migration, rollback, security, observability, and operational
   behavior.

Every Epic, Milestone, and Task cites concrete architecture or ADR sources.
Never add behavior, technology, infrastructure, pattern, abstraction, or edge
case not supported by those sources.

## Technical Task contract

Read [references/task-contract.md](references/task-contract.md). Every Task has
planning status `ready`, is self-contained, and states exactly:

- what changes, where, in what order, with which inputs, outputs, data, and
  contracts;
- the components, classes, interfaces, responsibilities, calls, dependency
  injection boundaries, and integration sequence;
- the approved technology and each applicable design pattern or SOLID rule,
  with its location, source, and reason;
- the defined edge cases, tests, acceptance evidence, and Definition of Done.

Add a technical blueprint: a Mermaid diagram when relationships or order
matter, and a minimal code, interface, schema, configuration, or pseudocode
sketch when it removes implementation ambiguity. Sketches define connections
and contracts, not the production implementation.

Use only patterns justified by accepted architecture or established repository
conventions. `Singleton`, `Abstract Factory`, `Chain of Responsibility`, and
`Strategy` are examples, not defaults. Do not force patterns or list SOLID
mechanically. Derive local class/interface details only when reversible,
evidence-based, and unable to alter architecture; otherwise escalate the gap.

## Dependency graph

After all Tasks exist, read
[references/dependency-quality.md](references/dependency-quality.md). Create one
global Task DAG and a Task-DAG view in every Epic and Milestone, including
external edges.

An edge `TASK-A -> TASK-B` is valid only when B consumes a concrete output,
contract, schema, migration, resource, or verified state produced by A. Record
that item and the reason on every edge. Never depend on chronology, convention,
shared context, or another Task's private implementation.

The global graph must have valid IDs, every Task exactly once, no cycles, all
cross-Epic/Milestone edges, all immediately executable Tasks, maximal safe
parallel waves, integration gates, and the technical critical path. Tasks in
one wave must have independent dependencies, non-conflicting write scope, and
compatible shared contracts.

Merge inseparable work or assign exclusive ownership when separate Tasks could
implement the same responsibility incompatibly. Preserve real prerequisites;
remove artificial ones.

A dependency is a scheduling edge, never a planning blocker. Every generated
Task remains `ready`; the execution order controls dispatch. Never publish a
`blocked` Task or a blocker Task. If an upstream gap prevents a valid DAG, do
not generate the plan; return the gap to `$software-architect`.

## Output and completion

Create or update:

```text
.discovery/<feature>/epics/EPIC-NNN-*.md
.discovery/<feature>/milestones/MILESTONE-NNN-*.md
.discovery/<feature>/tasks/TASK-NNN-*.md
.discovery/<feature>/planning/dependency-graph.md
.discovery/<feature>/planning/coverage-matrix.md
.discovery/<feature>/planning/execution-order.md
.discovery/<feature>/planning/production-readiness.md
.discovery/<feature>/planning/open-decisions.md
.discovery/<feature>/03-implementation-plan.md
```

Each Epic lists its Milestones, descendant Tasks, and graph view. Each
Milestone lists its Tasks, local graph with external edges, delivery criteria,
and integration gate. `03-implementation-plan.md` is only the linked index and
execution summary.

Publish planning as `generated` only after proving complete traceability,
unique hierarchy membership, exact technical contracts, faithful blueprints,
complete edge-case coverage, a real acyclic DAG, maximal safe parallelism, and
zero blockers. `planning/open-decisions.md` must state `None`.

Report the feature, architecture input, plan path, Epic/Milestone/Task counts,
parallel waves, critical dependencies, planning directory, and blockers. A
generated plan reports zero blockers.
