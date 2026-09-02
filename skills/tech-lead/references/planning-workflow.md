# Planning Workflow

Read before decomposing architecture.

## Ingest architecture as one contract

Read all text, tables, diagrams, ADRs, flows, risks, sequencing constraints,
and production-readiness gates. A relationship shown only in a diagram is
still authoritative. Do not plan from the summary alone.

Build an inventory grouped by concept, using representative examples only to
guide a complete search:

- requirements, constraints, decisions, and ADRs;
- domains, boundaries, components, resources, and ownership;
- data, contracts, integrations, and flows;
- infrastructure, delivery, migration, operations, and cross-cutting
  requirements;
- risks, edge cases, and readiness gates.

For every inventory item record its architecture source and implementation
disposition before creating tasks.

## Traceability

Preserve existing identifiers. When architecture lacks stable identifiers,
create reference-only IDs such as `ARCH-COMP-001` or `ARCH-FLOW-002` without
changing architecture content.

Every epic, milestone, task, coverage row, and readiness gate must answer why
it exists using concrete architecture sources. No task may exist as an
unapproved improvement.

## Decomposition hierarchy

Use:

```text
Architecture
  -> Epics
    -> Milestones
      -> Tasks
```

An epic is a coherent technical capability. It contains ID, objective,
architecture sources, scope, out-of-scope boundaries when knowable,
components, dependencies, milestones, a complete task roll-up, and completion
criteria.

A milestone is a technically verifiable delivery within exactly one epic, not
a date. It contains ID, parent epic, objective, architecture sources, expected
result, tasks, real dependencies, completion criteria, integration gate, and
risks.

A task belongs to exactly one milestone and produces one coherent result that
can be implemented and verified without hidden context. Split independent
results; do not split by file, class, function, or layer unless that unit is
itself a real deliverable.

`Delivery` is a synonym for milestone and `activity` is a synonym for task;
do not create additional hierarchy levels.

## Full lifecycle

For each architecture item investigate all implementation work needed across
its lifecycle, such as build, integration, provisioning, configuration,
migration, validation, instrumentation, deployment, rollout, operation,
recovery, rollback, and documentation. These are concepts to search for, not a
fixed list of automatic tasks.

Do not omit work because it is operational, cross-cutting, small, or implicit.
Do not create work that architecture and repository evidence do not require.

## Planning artifacts

The detailed backlog lives in `epics/`, `milestones/`, `tasks/`, and
`planning/`. `03-implementation-plan.md` links them and summarizes:

- architecture inventory and coverage;
- epic, milestone, and task counts;
- dependency graph and critical path;
- immediate and parallel waves;
- integration and readiness gates;
- quality requirements;
- blockers, which must be zero when generated.

Do not put full task bodies into the implementation-plan index.

## Forbidden reinterpretation

Do not change selected technologies, patterns, protocols, boundaries,
ownership, consistency, communication style, data authority, or product
behavior. A necessary missing decision is an upstream blocker, not a Tech Lead
choice or planning task.
