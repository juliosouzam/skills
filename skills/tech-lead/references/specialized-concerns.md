# Specialized Planning Concerns

Read only the sections applicable to the approved architecture. Treat each
heading as a concept: use examples to guide repository and architecture
research, then identify every material variant actually present. Do not create
components or work merely to satisfy a list.

## Services and modules

For each defined service, module, worker, scheduler, or agent, map
responsibility, inputs, outputs, dependencies, owned data, configuration,
security, resilience, observability, deployment, tests, and related tasks.
Preserve boundaries and ownership exactly.

## Contracts and events

For every API, RPC, event, message, stream, webhook, file, tool, or internal
interface, map provider/producer, consumers, purpose, schema authority,
versioning, compatibility, authentication/authorization, errors, idempotency,
delivery, ordering, retry, observability, and implementation tasks when those
properties apply.

Do not invent payloads or fields. A material missing contract is an upstream
architecture blocker.

## Data and storage

For every approved data store, map owner, writers, readers, schema work,
migrations, constraints, access patterns, lifecycle, consistency, indexing,
retention, deletion, backup, restore, security, observability, rollout,
rollback, and tests. Do not redistribute ownership or invent infrastructure
sizes and vendors.

## Infrastructure and delivery

Map every approved runtime, network, certificate, gateway, database, broker,
cache, storage, secret, identity, observability backend, environment, and
delivery resource to provisioning, configuration, security, monitoring,
recovery, validation, and tasks. Values such as region, SKU, CPU, memory,
replicas, or autoscaling must come from architecture or repository evidence.

For CI/CD, infrastructure, data, or AI pipelines, map the complete applicable
path from validation and build through artifact, deployment, migration,
approval, rollback, and evidence.

## Observability, security, and resilience

Distribute component-level instrumentation and controls into the tasks that
own them; create platform tasks only for genuinely shared capabilities.

Investigate all architecture-required forms of logs, metrics, traces,
correlation, health, dashboards, alerts, audit, identity, authorization,
tenancy, secrets, encryption, network controls, input validation, timeouts,
retries, backoff, idempotency, deduplication, dead-letter handling,
backpressure, compensation, replay, and recovery.

These are examples, not automatic mechanisms. Plan only what architecture or
explicit requirements demand.

## Testing

Derive tests from behavior and boundaries: local business rules, persistence
and broker integration, producer/consumer compatibility, critical end-to-end
flows, migrations, failure and recovery, authorization and isolation,
performance requirements, and operational validation. Associate each test
with the task that owns the behavior or gate.

## Migration and rollout

When changing an existing system, preserve the approved compatibility and
migration strategy. Map all applicable schema or contract evolution, backfill,
parallel operation, cutover, rollback, decommission, data validation, and
recovery work. If the required strategy is absent, return to the Architect.

## LLM, RAG, agents, and tools

When approved architecture contains AI systems, map implementation for model
integration and fallback, prompt lifecycle, context isolation, RAG ingestion
and retrieval, agent state and termination, tool permissions and side effects,
output validation, evaluations, cost and latency observability, safety,
deployment, and rollback.

For every tool map read/write impact, authorization, credentials, idempotency,
timeout, duplicate or partial execution, audit, and tests. Do not invent model
choices, metrics, thresholds, datasets, or agent responsibilities.
