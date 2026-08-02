# Design an AI Coding Assistant

> **Difficulty:** Hard  
> **Main focus:** repository context, low-latency completion, safe edits

## Interview prompt

Design an IDE assistant for code completion, chat, multi-file edits, and command execution.

## 1. Clarify the product and success criteria

**What I would say first:** Completion and agentic editing are different latency and risk classes. Repository context must respect workspace boundaries, and generated actions need review or sandboxing.

### Functional requirements

- Provide low-latency inline completion and conversational code help.
- Index a repository and retrieve relevant symbols and files.
- Propose multi-file patches with diffs and tests.
- Optionally run commands in a restricted workspace with approval.

### AI and product constraints

- Repositories can be large, private, generated, or partially indexed.
- Source files and dependency docs can contain prompt injection.
- Edits and commands can destroy work or expose secrets.

## 2. Contracts and data

- Completion request {prefix, suffix, language, filePath, cursor, contextVersion}
- Agent task {workspaceId, objective, allowedPaths, allowedTools, budget}
- Patch proposal contains base file hashes, unified diff, rationale, tests, and provenance

## 3. High-level design

```text
IDE extension -> local context selector -> AI gateway -> completion model
       |                  |
       |                  +-> repository symbol/index service
       |
task UI -> durable agent orchestrator -> model
                    |              |
             policy/approval    sandboxed file/tools
                    |              |
                  diff review <- results/tests
```

## 4. Critical request flow

1. Inline completion selects a small local prefix/suffix and routes to a fast model.
2. Repository chat retrieves symbols, definitions, and version-matched docs within workspace ACL.
3. Agent plans bounded steps and reads only allowed paths.
4. File edits become patches against recorded base hashes; conflicts stop application.
5. Commands run in a restricted sandbox and results return to an explicit diff/test review.

## 5. Quality and evaluation

- Evaluate completion acceptance carefully alongside correctness, latency, and later reversion.
- Use repository-level tasks with tests, style checks, security cases, and hidden holdouts.
- Measure retrieval relevance and whether cited code actually exists at the recorded revision.
- Red-team secret extraction, instruction injection, destructive commands, and dependency hallucination.

## 6. Reliability, scale, observability, and cost

- Incrementally index file hashes and symbols; exclude binaries, generated files, secrets, and ignored paths.
- Cancel obsolete completion requests on every new keystroke.
- Checkpoint agent state and cap tokens, commands, changed files, and runtime.
- Track time to suggestion, accepted-and-kept rate, patch test pass, rollback, sandbox failure, and cost.

## 7. Safety, security, and privacy

- Keep credentials outside model context and restrict network egress and filesystem roots.
- Treat repository text as untrusted data, not policy.
- Require confirmation for commands, dependency changes, deletion, external messages, or broad edits.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Large context dump | Simple with high cost, distraction, and leakage risk. |
| Targeted retrieval | Efficient and safer but can miss dependencies. |
| Direct file mutation | Fast demo but risky and hard to review. |
| Patch proposal | Reviewable and conflict-aware with one more step. |

## 9. 60-second interview summary

Fast completion uses minimal cancellable context, while repository chat and editing use permission-aware symbol retrieval. Agent work is budgeted and sandboxed; all edits are hash-based reviewable patches, and destructive tools require explicit authority.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

