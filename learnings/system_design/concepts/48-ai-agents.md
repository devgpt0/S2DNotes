# AI Agents and Tool Orchestration

## Idea

An agent is a bounded control loop where a model chooses among allowed tools,
observes results, and continues until completion or a budget limit. The system,
not the model, owns permissions, state, validation, and side effects.

## Visual model

```text
goal -> policy/model -> proposed tool call -> validate/authorize -> sandbox/tool
  ^                                                      |
  +-- durable state <- observation <- normalized result -+
```

## Design steps

1. Define success, allowed actions, risk tiers, and stop conditions.
2. Publish typed tool schemas with least-privilege credentials.
3. Validate every argument and authorize using trusted user/tenant context.
4. Make side-effecting calls idempotent and require approval for high-risk actions.
5. Persist step state, budgets, tool results, and audit events.
6. Limit steps, time, tokens, cost, recursion, output size, and concurrency.
7. Evaluate task completion plus unsafe/needless actions.

## When to use it

Use an agent when tasks require dynamic multi-step tool selection. Prefer a
deterministic workflow when the steps and branches are known.

## Trade-offs

More autonomy handles varied tasks but reduces predictability and increases
security, latency, and cost. Human approval improves safety but slows completion.

## Failure modes

- Looping/planning drift: hard budgets and progress checks.
- Duplicate action: idempotency key and durable action ledger.
- Tool outage: typed error, bounded retry, resume or explicit failure.
- Prompt injection: treat all external content as data, never policy.

## Common mistakes

- Giving the model broad credentials or raw shell/network access.
- Trusting tool arguments because they match a schema syntactically.
- Keeping critical agent state only in the context window.
- Measuring impressive traces instead of successful safe outcomes.
