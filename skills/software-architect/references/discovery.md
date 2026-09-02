# Architecture Discovery

Use this reference before starting or resuming the Software Architect
interview.

## Evidence order

Read the enriched prompt first, then inspect applicable persisted artifacts,
repository instructions, code, tests, manifests, schemas, migrations,
contracts, configuration, infrastructure, CI/CD, observability, security, and
operational documentation.

Ask only for material intent that evidence cannot establish. When sources
conflict, record the sources, statements, impact, and required resolution;
never choose silently.

Keep these categories distinguishable:

- user requirement or constraint;
- accepted user decision;
- repository fact;
- architectural recommendation;
- accepted architectural decision;
- unknown or conflict.

## Decision-tree coverage

Build a tree of all applicable concepts rather than dumping a fixed component
catalog. For each concept, use a few representative examples to guide
investigation, then search for every material variant in the specification and
repository.

Cover when applicable:

- objective, actors, domain language, use cases, boundaries, current state,
  and target state;
- architecture drivers, constraints, selected technologies, and prohibited
  choices;
- responsibilities, ownership, source of truth, states, lifecycle, and
  transitions;
- components, resources, dependencies, synchronous and asynchronous
  contracts, producers, consumers, and external systems;
- data schemas, access patterns, retention, privacy, migration, backup,
  restore, and deletion;
- identity, authorization, tenancy, trust boundaries, secrets, audit, and
  abuse controls;
- observability, operability, capacity, cost, deployment, rollback, recovery,
  and production readiness;
- risks, trade-offs, difficult-to-reverse choices, compatibility, and
  evolution.

Do not add a concept or component merely to fill this list. Classify a branch
`NOT_APPLICABLE` with a reason when evidence shows it does not apply.

## Scenario matrix

For every material flow or state transition, investigate all applicable forms
of these scenario concepts:

- normal completion and boundary inputs;
- validation or authorization failure;
- dependency unavailable, degraded, slow, or changed;
- partial completion and crash between side effects;
- first, repeated, duplicate, concurrent, and out-of-order execution;
- stale, invalid, deleted, or ownership-changed state;
- permission revocation during execution;
- timeout, cancellation, retry, retry storm, compensation, and recovery;
- restart, replay, poison input/message, backlog, and slow consumer;
- schema, contract, application, or infrastructure version skew;
- migration, partial deployment, rollback, backup restore, and regional loss;
- capacity or rate limit exceeded;
- cross-user or cross-tenant isolation failure;
- external-provider failure or behavioral change.

Do not assume every example applies. Do not omit a material scenario because
it is absent from the happy path.

For each scenario establish:

1. precondition and actor;
2. state and data before execution;
3. expected behavior and side effects;
4. owner of each effect;
5. externally visible result;
6. detection and observability;
7. retry, recovery, compensation, or manual action;
8. idempotency, consistency, security, and audit implications.

## Distributed-system decisions

When distribution or asynchronous communication exists, establish from
requirements and evidence:

- communication and delivery semantics;
- ordering and duplicate behavior;
- timeouts, bounded retries, backoff, jitter, and overload behavior;
- idempotency, deduplication, replay, poison-message, and dead-letter handling;
- source of truth, consistency, replication, conflict resolution, and
  cross-component transactions;
- recovery after process, dependency, zone, or region failure.

Mechanisms such as brokers, outbox, saga, cache, circuit breaker, CQRS, event
sourcing, or multi-region deployment are possible implementations, not
automatic requirements. Choose them only after the required properties are
known.

## Question protocol

When a material unresolved branch depends on the user:

1. choose the decision that unlocks the most dependent branches;
2. ask exactly one main question;
3. explain affected behaviors, components, data, contracts, or risks;
4. recommend the simplest option that preserves requirements;
5. present only material alternatives and trade-offs;
6. wait for the answer;
7. persist the answer and resolution;
8. re-read and re-evaluate the complete tree and repository evidence.

Use a concrete scenario when abstract wording could hide behavior. Never turn
the scenario into a requirement without acceptance. Do not ask facts the
repository already establishes.

## Completion review

Before architecture generation, verify that every applicable branch and
scenario is `RESOLVED` or justified `NOT_APPLICABLE`; every component,
resource, owner, contract, dependency, and failure behavior is defined; and no
material decision is deferred. Otherwise continue the interview or stop.
