# Design a Tool-Using AI Agent Platform

> **Difficulty:** Hard  
> **Main focus:** orchestration, permissions, durable state

## Interview prompt

Design a platform where AI agents plan multi-step tasks and call external tools.

## 1. Clarify the product and success criteria

**What I would say first:** The model proposes actions; application code validates, authorizes, and executes them. The agent loop needs explicit budgets, durable checkpoints, and approval boundaries.

### Functional requirements

- Run multi-step tasks using registered tools.
- Pause for approval, resume after failure, and expose a trace.
- Protect credentials and enforce user/tenant permissions.
- Bound time, tokens, tool calls, retries, and spend.

### AI and product constraints

- Model decisions are probabilistic and may loop.
- Tool results and retrieved text are untrusted.
- External actions can be irreversible or costly.

## 2. Contracts and data

- POST /v1/runs {agentVersion, objective, inputRefs, budget}
- Tool schema {name, typedInputSchema, typedOutputSchema, risk, permission, timeout}
- Run events: planned, tool_proposed, approval_required, tool_started, tool_completed, checkpointed, completed

## 3. High-level design

```text
user -> run API -> durable orchestrator/state machine
                         |
                   context builder <-> model
                         |
                   policy/authorization
                         |
              tool proposal -> approval gate
                         |
                sandboxed tool executor -> external systems
                         |
               result validation -> checkpoint/audit
```

## 4. Critical request flow

1. Create a run with immutable agent, model, prompt, tool, and policy versions.
2. Build the minimum context and request the next typed proposal.
3. Validate schema, budget, risk, and authorization independently of model text.
4. Require user approval for high-impact actions, then execute with scoped short-lived credentials.
5. Persist result and checkpoint before choosing the next step; stop on completion or budget.

## 5. Quality and evaluation

- Evaluate task success, unnecessary steps, tool selection, argument accuracy, policy adherence, and recovery.
- Use simulated or sandboxed tools for regression and adversarial tests.
- Replay traces against new versions without repeating real side effects.
- Human review samples high-risk or low-confidence completions.

## 6. Reliability, scale, observability, and cost

- Use a durable workflow engine so hours-long runs survive process restarts.
- Each tool call has an idempotency key, deadline, retry policy, and explicit unknown-result handling.
- Detect repeated equivalent states and terminate loops.
- Track success per task class, steps, approval rate, tool failures, loop stops, latency, tokens, and spend.

## 7. Safety, security, and privacy

- Tool allowlists, least privilege, sandboxing, egress controls, and user confirmation are real boundaries.
- Treat prompt injection from websites and tool output as hostile data.
- Never place broad permanent credentials in model context; audit every proposed and executed action.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Model-controlled direct tools | Fast prototype but unsafe and unauditable. |
| Policy-mediated tools | More engineering with enforceable permissions. |
| Long autonomous runs | More capability with growing cost and error risk. |
| Short bounded plans | Safer and easier to recover, sometimes less flexible. |

## 9. 60-second interview summary

The agent is a durable state machine. The model emits typed proposals, while deterministic code enforces schema, authorization, budgets, approvals, and tool isolation. Versioned traces support replay, evaluation, recovery, and audit without repeating side effects.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

