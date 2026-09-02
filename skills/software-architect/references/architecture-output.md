# Architecture Output and ADRs

Read this reference only after discovery passes its completion gate and before
writing or revising `02-architecture.md` and ADRs.

## Architecture content

Produce an implementation-ready specification containing all applicable:

1. understanding, scope, requirements, constraints, decisions, and drivers;
2. current state, target state, domains, boundaries, and canonical concepts;
3. components and resources with responsibility, rationale, owned data,
   inputs, outputs, dependencies, interfaces, and failure behavior;
4. end-to-end primary, alternate, failure, recovery, migration, and rollback
   flows;
5. data ownership, source of truth, schemas, lifecycle, consistency,
   migration, retention, backup, restore, deletion, privacy, and audit;
6. APIs, RPCs, events, messages, streams, files, webhooks, tools, integrations,
   providers, consumers, contracts, versions, compatibility, and delivery
   semantics;
7. concurrency, idempotency, retries, cancellation, compensation, recovery,
   and degraded behavior;
8. identity, authorization, tenancy, trust boundaries, secrets, encryption,
   abuse prevention, least privilege, and supply-chain concerns;
9. logs, metrics, traces, correlation, health, dashboards, alerts, audit,
   diagnostics, and incident response;
10. deployment, configuration, environments, capacity, cost, migration,
    rollout, rollback, disaster recovery, and production-readiness gates;
11. alternatives, trade-offs, risks, mitigations, and the complete ADR index;
12. architectural sequencing.

Do not write code or create the engineering backlog.

## Diagrams

Use only diagrams that materially explain the system. Depending on the
architecture, these may include:

- system context for actors and external systems;
- container/component views for boundaries and responsibilities;
- sequence diagrams for distributed, stateful, destructive, or failure-prone
  flows;
- data or event flows for ownership and movement;
- deployment views when runtime topology matters;
- agentic workflow views when models, agents, tools, loops, or human approval
  materially affect behavior.

Diagrams are specifications: labels, direction, ownership, producer/consumer,
state, and error paths must agree with the text and ADRs.

## ADR rule

Create one physical ADR for every architectural decision:

```text
.discovery/<feature>/adrs/ADR-NNN-short-slug.md
```

Each ADR contains:

```markdown
# ADR-NNN — Title

## Status

Proposed | Accepted | Superseded | Deprecated

## Context and constraints

## Architecture drivers

## Alternatives considered

## Decision

## Rationale

## Trade-offs

## Positive consequences

## Negative consequences

## Risks

## Reversibility

## Review conditions

## Affected components, contracts, flows, and downstream work
```

The architecture links every ADR and contains no unrecorded architectural
decision. An active decision in architecture marked `generated` must have an
`Accepted` ADR; `Proposed` is allowed only while discovery remains incomplete.
`Superseded` and `Deprecated` are historical states. Requirements and facts
are not mislabeled as decisions.

## Architectural sequencing

Describe only constraints and opportunities imposed by architecture:

- capability or dependency order;
- foundations required by multiple components;
- independently realizable increments;
- integration and migration boundaries;
- work that architecture permits to proceed in parallel;
- architectural readiness gates for each increment;
- risks or rollback constraints that affect sequencing.

Do not create milestones, epics, tasks, estimates, team assignments, or the
implementation backlog. Do not leave “decisions needed” inside sequencing;
all material decisions must already be resolved.

## Final structure

Use sections proportional to the feature. A typical complete artifact has:

- understanding and drivers;
- requirements and constraints;
- architecture overview;
- domains, boundaries, components, and resources;
- flows, contracts, data, security, resilience, and observability;
- operations, deployment, migration, and production readiness;
- specialized architecture when applicable;
- diagrams;
- ADR index;
- trade-offs and risks;
- architectural sequencing;
- summary of decisions;
- material open decisions: `None`.

Do not create empty sections. The final artifact must allow Tech Lead planning
without reinterpretation or invention.
