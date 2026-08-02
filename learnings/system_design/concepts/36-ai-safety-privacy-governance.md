# AI Safety, Privacy, and Governance

## Idea

AI controls must cover input, retrieval, model output, tools, storage, and human
operations. One output filter is not a safety system.

## Classroom board

```text
input policy -> data/ACL boundary -> model -> output policy
                              tool action -> authorization/approval/audit
incident -> trace/version evidence -> contain -> correct -> re-evaluate
```

## Design steps

1. Classify data and harms by use case/tenant/region.
2. Minimize/redact data and enforce retention/deletion.
3. Layer prompt-injection defenses, grounded permissions, output checks, and
   tool approvals.
4. Keep model/prompt/data lineage, audit logs, incident response, and rollback.

## Trade-offs and mistakes

Stricter controls can reduce utility and add latency; risk determines depth.
Never expose cross-tenant context, claim filters are perfect, store everything
for “future training,” or deploy a model with unknown lineage.
