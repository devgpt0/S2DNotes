# Prompt, Context, and Memory Management

## Idea

The model sees only the context supplied for the current request. A production system must deliberately choose what enters that context.

Prompts are versioned application code. Model memory is stored application data that is retrieved into a later prompt; it is not magical permanent knowledge.

## Visual model

```text
system policy + user request + recent conversation
                         +
retrieved knowledge + selected user memory + tool results
                         |
              context builder and budget
                         |
                        model
```

## Design steps

1. Separate trusted system policy from untrusted user, retrieval, and tool content.
2. Give every context source a purpose, owner, priority, and size budget.
3. Keep recent turns exactly when wording matters; summarize older turns when safe.
4. Retrieve long-term memories by relevance and permission, not by dumping all history.
5. Store durable business state in a database, not only in conversation text.
6. Version prompts and evaluate changes before rollout.
7. Record which context sources influenced an answer, subject to privacy rules.
8. Delete expired or user-requested memory from every derived store.

## Types of memory

| Memory | Example | Correct storage |
|---|---|---|
| Working memory | Current task and recent turns | Request context |
| Long-term preference | Preferred response language | Permission-aware profile store |
| Episodic memory | A past support interaction | Searchable event store |
| Durable application state | Order status or account balance | Source-of-truth database |

## Trade-offs

- More context may improve recall but increases latency, cost, and distraction.
- Summaries save space but can lose details or preserve an old mistake.
- Long-term memory improves continuity but raises privacy and deletion obligations.

## Common mistakes

- Treating the context window as a database.
- Trusting retrieved text as instructions.
- Sending unbounded conversation history.
- Mixing data between users or tenants.
- Updating memory from an uncertain model claim without verification.
- Changing prompts without versioned tests.
