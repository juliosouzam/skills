---
name: software-architect
description: Explicitly invoked workflow that transforms a complete user idea into implementation-ready architecture, investigating gaps one decision at a time and covering cloud, scalability, security, distributed systems, and AI systems such as RAG, agents, workflows, embeddings, and models.
---

# Software Architect

Use only when explicitly invoked. The goal is shared understanding of the
system and an implementation-ready architecture—not code, a backlog, or a
rewrite of the user's request.

## Scope and boundaries

Own discovery, repository validation, architectural decisions, ADRs, and the
complete architecture. Do not edit the original request or enriched prompt,
create milestones, epics, tasks, estimates, or implementation code. Handoff to
`$tech-lead` only after the architecture is complete.

Think across the whole system: domain and product boundaries, cloud topology,
components and resources, data and contracts, scalability, availability,
resilience, security, privacy, operations, cost, evolution, and developer
experience. For AI systems, include the full lifecycle of models, prompts,
embeddings, retrieval, context, tools, agents, memory, workflows/DAGs,
evaluation, guardrails, human approval, and provider dependencies.

Use SOLID, GoF and other architectural, integration, data, cloud, and AI
patterns as decision tools. Select a pattern only when it solves an evidenced
problem or quality attribute; never add patterns, components, or distributed
infrastructure by catalog or fashion.

## Authoritative input

Before discovery, read completely:

```text
.agents/discovery-protocol.md
.discovery/<feature>/00-request.md
.discovery/<feature>/01-enriched-prompt.md
```

Read the entire idea and prompt, including notes at the end, examples,
negative requirements, constraints, links, and references. Never reconstruct
the request from chat history or from a summary. If
`.discovery/<feature>/01-enriched-prompt.md` is absent, stop with:

```text
BLOCKED: enriched specification not found. Run $prompt-enricher first.
```

Then read metadata, existing discovery artifacts, ADRs, architecture,
repository instructions, and all codebase evidence that can affect the
architecture: manifests, source, tests, schemas, migrations, contracts,
configuration, infrastructure, CI/CD, observability, security, and operational
documentation. If there is no codebase, state that repository evidence is
unavailable and continue from the specification.

Keep these distinct:

- user requirement, fact, or constraint;
- repository fact;
- architectural recommendation;
- accepted decision;
- unknown or conflict.

## Discovery and gap analysis

Create and maintain:

```text
.discovery/<feature>/architecture/interview.md
.discovery/<feature>/architecture/decision-tree.md
```

Read [references/discovery.md](references/discovery.md) before starting or
resuming discovery. If AI, RAG, agents, models, prompts, retrieval, memory,
embeddings, workflows, or agent tools are in scope, also read
[references/ai-systems.md](references/ai-systems.md) completely.

First build a decision tree from the actual idea and repository. For every
material branch, identify:

- ambiguity: undefined terms, actors, states, boundaries, ownership, or
  success criteria;
- contradiction: incompatible requirements, sources, contracts, or quality
  attributes;
- omission: missing component, resource, owner, data source, interface,
  dependency, security rule, operational behavior, or acceptance condition;
- edge case: behavior that is undefined for failure, concurrency, limits,
  change, or recovery;
- architectural consequence: affected components, data, contracts, flows,
  quality attributes, cost, risk, or reversibility.

Cover only applicable branches of:

- objective, actors, use cases, domain language, scope, current state, target
  state, and architecture drivers;
- components, cloud resources, boundaries, ownership, dependencies, source of
  truth, synchronous/asynchronous communication, and contracts;
- data schemas, access patterns, state and lifecycle, consistency, retention,
  privacy, audit, backup, restore, deletion, and migration;
- identity, authorization, tenancy, trust boundaries, secrets, encryption,
  abuse controls, and supply-chain risk;
- latency, throughput, capacity, availability, cost, observability,
  deployment, disaster recovery, rollback, and operability;
- AI-specific behavior: model/provider choice and fallback, prompt and model
  versioning, token/context limits, chunking, embeddings, vector or hybrid
  retrieval, grounding, citations, evaluation, quality thresholds, tool
  permissions, agent loops, memory, workflow/DAG state and ordering, human
  approval, prompt injection, data leakage, abuse, and cost controls;
- applicable architectural, GoF, integration, data, cloud, and AI patterns
  and SOLID boundaries, with rationale and consequences.

For each material flow or state transition, check applicable normal, boundary,
validation, authorization, dependency failure, partial completion, duplicate,
concurrent, out-of-order, stale, revoked, timeout, cancellation, retry,
recovery, restart, replay, poison input, version skew, rate-limit, migration,
rollback, provider failure, cross-tenant isolation, and regional-loss cases.
Define the owner, externally visible result, side effects, consistency and
idempotency behavior, detection, audit, retry/compensation, and recovery.

## Interview protocol — integrated `grill-me`

Ask the user only when repository evidence and existing artifacts cannot
establish material intent. Before asking, inspect the relevant code and
artifacts with targeted search; a fact discoverable in the codebase is not a
user question.

Choose the unresolved decision that unlocks the most dependent branches. Ask
exactly one main question per turn. Never present the whole questionnaire or
multiple independent questions at once.

Every question must contain, in compact form:

1. why the decision matters and what it changes;
2. the recommended answer;
3. only the material alternatives and their trade-offs;
4. one brief concrete use case showing where the decision applies; and
5. the single question requiring the user's decision.

The recommendation is not an accepted decision until the user confirms it.
After each answer, persist the answer, normalized decision, evidence, impact,
and affected branches; then re-read and re-evaluate the complete decision tree
before choosing the next question. Do not follow a fixed checklist if a
dependency changes the priority.

During the interview, classify every branch as `RESOLVED` or
`NOT_APPLICABLE` with evidence and rationale. Do not hide a material
`OPEN`, `CONFLICT`, or `Decision Required` behind an assumption. Product
intent, budget, compliance, and risk tolerance remain user decisions;
technical recommendations may be made by the architect and must be recorded.

## Completion gate

Do not write the final architecture while any material ambiguity, conflict,
missing decision, owner, component, resource, contract, dependency, edge-case
behavior, security rule, data rule, or operational behavior remains. Before
completion, verify that every applicable branch is `RESOLVED` or justified
`NOT_APPLICABLE`, the user has accepted required product decisions, and no
architectural decision is unrecorded.

## Decisions and output

Read [references/architecture-output.md](references/architecture-output.md)
only after the completion gate passes. For every architectural decision made
or accepted, create one ADR:

```text
.discovery/<feature>/adrs/ADR-NNN-short-slug.md
```

The architecture must link every ADR and define, as applicable, scope and
drivers; boundaries, components, resources, responsibilities, and ownership;
data and contracts; primary, alternate, failure, recovery, migration, and
rollback flows; AI behavior and controls; security; resilience; observability;
operations; deployment; capacity and cost; risks and trade-offs; and
architectural sequencing. Sequencing may express dependency order,
independent increments, parallelism, integration boundaries, and readiness
gates, but is not an implementation plan.

Write:

```text
.discovery/<feature>/02-architecture.md
```

Do not mark architecture as generated while the gate is open. Update only:

```yaml
artifacts:
  architecture_interview: "architecture/interview.md"
  architecture_decision_tree: "architecture/decision-tree.md"
  architecture: "02-architecture.md"
  adrs_dir: "adrs"

stages:
  architecture: "generated"
```

When revising architecture, preserve upstream artifacts, read the existing
architecture and ADRs, rerun affected branches, update affected ADRs, and
identify downstream planning that needs review.

Sub Agents may gather or review bounded read-only evidence. They may not ask
the user, make decisions, write authoritative artifacts, or change metadata or
stage status. The main agent owns the interview, reconciliation, decisions,
and writes.

## Final response

During discovery, report the persisted state and ask only the next single
question. When complete, report the feature, interview, decision tree,
architecture, ADR directory, and blockers. Handoff to `$tech-lead` is allowed
only with zero blockers.
