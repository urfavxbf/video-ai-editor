# AI Engineering — senior workflow

## Scope and architecture
Identify user outcome, task success criteria, data sensitivity, model modalities, latency/cost budget, volume, and failure tolerance. Decide whether the problem needs a deterministic algorithm, retrieval, one LLM call, tool calling, or multi-step orchestration. Prefer the simplest reliable approach. Separate model inference from business logic, persistence, user interface and background jobs.

## Tool-using agents
Specify tools with narrow typed schemas, predictable errors, timeouts and observable effects. Treat model outputs and retrieved documents as untrusted inputs; enforce authorization in code, not prompts. Prevent prompt injection from granting execution rights. Log tool decisions without logging secrets or private user data. Use checkpoints for irreversible or paid actions; limit iterations, spend, tokens and recursion. Require explicit permission for publishing, deleting, spending, sending messages or modifying access controls.

## Knowledge, retrieval and memory
Maintain source provenance, document timestamps, access controls and deletion semantics. For RAG, specify ingestion, parsing, chunking, embeddings, retrieval, reranking, context packaging, citation grounding and update policy. Evaluate retrieval separately from answer generation. Do not call an agent 'memory-enabled' unless storage and retrieval actually exist and are tested.

## Evaluation and reliability
Assemble representative gold cases, difficult edge cases, adversarial prompts, harmful input and regression fixtures. Record model/version, prompts, tool contracts, metrics, cost and latency. Measure answer correctness, citation fidelity, tool safety, hallucination rate, retrieval relevance and task completion, rather than judging on impressive prose. Add fallbacks, rate limits, retries with backoff, cancellation, and human escalation.

## Security and privacy
Store API credentials in approved secret managers/environment configuration, never a repo or unprotected logs. Redact customer content, scope permissions, defend prompt injection and SSRF, constrain shell execution to workspace policies, and confirm data residency or retention requirements where relevant.

## Delivery
Document model/provider dependencies, setup, failure modes, evaluation results, costs, monitored limits, reproducibility and rollback. A prompt alone is not a deployable agent.
