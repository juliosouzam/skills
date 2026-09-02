# AI, LLM, RAG, and Agent Architecture

Read only when models, prompts, RAG, agents, memory, or tools are in scope.

Treat each item below as a concept to investigate across every applicable
variant in the request and repository. Examples are non-prescriptive.

## Responsibility and trust

Define what remains deterministic application responsibility versus model,
retrieval, agent, and tool responsibility. A model is not a deterministic
source of truth. Establish autonomy limits, human approval, grounding,
provenance, validation, fallback, and failure ownership.

## Model and provider

Establish model roles, routing, configuration, context limits, latency, cost,
provider dependency, version-change behavior, fallback, and replacement
strategy. Do not invent model choices or thresholds.

## Prompts and context

Define prompt ownership, versioning, environments, release, rollback, tests,
and observability. Define context sources, relevance, temporal validity,
isolation, retention, sanitization, authorization, and size limits. Prompts
must not contain secrets.

## RAG

When retrieval exists, cover the complete lifecycle: source authorization,
ingestion, parsing, normalization, chunking, embeddings, storage, indexing,
filters, retrieval, reranking, citations/provenance, update, deletion,
retention, evaluation, tenant isolation, and recovery.

## Agents, memory, and tools

For every agent define responsibility, input, output, state, memory, context,
tools, permissions, timeout, iteration and termination limits, validation,
fallback, audit, and recovery. Justify why agentic behavior is needed instead
of a deterministic function or workflow.

For every tool define operation, target system, read/write effect,
authorization, credential boundary, idempotency, timeout, retry, partial
failure, duplicate execution, result validation, and audit. State-changing
tools require explicit approval boundaries when applicable.

## Evaluation and observability

Define evaluation from actual product behavior: representative datasets,
golden cases, offline and continuous regression, grounding, relevance,
correctness, safety, output validity, retrieval quality, and tool correctness.
Do not invent metrics or thresholds.

Observe model and prompt version, tokens, cost, latency, retrieval, tool calls,
iterations, validation failures, fallback, safety events, and user-visible
outcomes while respecting privacy.

## AI-specific scenarios

Investigate at least when applicable:

- prompt injection and untrusted retrieved/tool content;
- unauthorized cross-user or cross-tenant context;
- stale, deleted, conflicting, or ungrounded knowledge;
- invalid, unsafe, unsupported, or malformed model output;
- model/provider outage, throttling, latency, or behavior change;
- duplicated, reordered, partially executed, or unauthorized tool calls;
- context overflow, memory corruption, infinite loops, and termination failure;
- fallback behavior and human recovery;
- data leakage through prompts, logs, traces, evaluation sets, or providers.

Resolve each material scenario in architecture and ADRs; do not reduce the
analysis to a generic AI component checklist.
