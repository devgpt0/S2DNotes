# Human-in-the-Loop Systems and AI Incidents

## Idea

Human review is a designed operational system, not a message saying “ask a human.” It needs routing rules, queues, context, permissions, service targets, and auditability.

AI incidents require fast containment because behavior can change through models, prompts, retrieval data, tools, or traffic.

## Visual model

```text
AI decision
   |
risk and confidence policy
   |                  |
auto-complete      review queue
                       |
                reviewer decision
                       |
           result + audit + safe feedback
```

## Design steps

1. Define which decisions require review based on impact, uncertainty, and policy.
2. Route cases to reviewers with the required skill and least-privilege access.
3. Show evidence, uncertainty, policy, and model version without leading the reviewer.
4. Set queue priorities, response targets, escalation, and overload behavior.
5. Support correction, rejection, appeal, and immutable audit records.
6. Sample some auto-approved cases to detect silent failures.
7. Validate reviewer feedback before using it for training.
8. Protect reviewers from unnecessary sensitive or harmful content.

## AI incident response

```text
detect -> disable or roll back -> contain -> investigate
       -> correct -> validate -> gradual restore -> learn
```

Keep tested controls to disable a model, prompt, retrieval source, memory write, or tool independently.

## Incident evidence

Preserve request identifiers, versions, policy decisions, retrieval references, tool calls, and outcomes while respecting retention and privacy limits.

## Common mistakes

- Making human approval a rubber stamp.
- Sending more work to the review queue than people can handle.
- Showing reviewers raw personal data they do not need.
- Having no appeal path for high-impact decisions.
- Feeding unverified reviewer actions directly into training.
- Lacking a fast kill switch and known-good rollback version.
