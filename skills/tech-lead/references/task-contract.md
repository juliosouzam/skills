# Executable Task Contract

Read before writing any task.

## Required structure

Each task must contain:

```markdown
---
status: ready
epic: EPIC-NNN
milestone: MILESTONE-NNN
---

# TASK-NNN — Title

## Parent hierarchy

Exactly one Epic and exactly one Milestone.

## Objective

One verifiable technical result.

## Architecture Sources

Concrete requirement, ADR, component, flow, contract, risk, or readiness IDs.

## Component and responsibility

Why this component owns the result.

## Context and boundaries

Exact scope, out of scope, expected repository areas, and results assigned to
other tasks.

## Inputs, outputs, contracts, and data

Only architecture-defined or repository-established details.

## Preconditions and dependencies

Real task IDs, the concrete predecessor output consumed, and why it must exist
first. Dependencies are execution-order edges, not a `blocked` planning state.

## Implementation requirements

What must be built, configured, migrated, documented, or instrumented without
writing the production implementation in the task. State the ordered steps,
approved technologies, exact participating components, classes, interfaces,
responsibilities, calls, dependency-injection boundaries, and integration
sequence when applicable.

## Technical blueprint

Use an architecture-faithful Mermaid diagram when relationships or order
matter. Use a minimal code, interface, schema, configuration, or pseudocode
sketch when it removes implementation ambiguity. Name each applicable design
pattern or SOLID constraint, its location, source, and reason. Do not force a
pattern, copy a catalog, or invent an architecture decision.

## Parallel safety

Expected write scope, shared contracts or resources, and why the Task can run
in its assigned wave without relying on another Task's private implementation
or producing an incompatible implementation of the same responsibility.

## Required scenarios

Success, failure, boundary, concurrency, retry, migration, security, or other
behavior required by the architecture.

## Error handling, security, and observability

Applicable behavior and evidence.

## Tests

Business-rule success and failure tests plus applicable unit, integration,
contract, migration, end-to-end, resilience, performance, or security tests.

## Acceptance criteria

Objective and verifiable outcomes.

## Definition of Done

All applicable implementation and quality gates.

## Documentation

Required updates.
```

## Context isolation

The executor must not need another task body or chat history to understand the
contract. Cite upstream artifacts instead of copying unrelated context. State
which repository areas may change when knowable and which areas are excluded.

## Granularity

Split a task when it contains independently implementable or verifiable
results. Keep tightly coupled changes together when separating them would
create artificial dependencies or incomplete behavior.

Avoid generic tasks such as “implement service” or “add observability.” Avoid
artificial tasks such as “create file” or “create class.”

## Definition of Ready

A task is `ready` only when objective, ownership, architecture sources, scope,
inputs, outputs, contracts, dependencies, scenarios, tests, acceptance
criteria, and Definition of Done are complete and no material decision is
missing.

## Definition of Done

Every executable task requires, when applicable:

- implementation fully satisfying the task and architecture;
- business-rule success and failure tests;
- required unit, integration, contract, migration, end-to-end, failure,
  resilience, security, and performance tests;
- all required tests passing;
- build passing;
- lint, formatting, type-check, and static analysis passing;
- contracts, migrations, observability, security, documentation, deployment,
  and rollback requirements complete;
- acceptance evidence recorded;
- no architecture deviation or unrelated change.

If a gate is not applicable, the task must contain an evidence-based reason.
Never omit a gate to make a task executable. Never create a test merely to
increase coverage; every test validates business behavior, a contract, a
failure, a safety property, or another explicit technical requirement.
