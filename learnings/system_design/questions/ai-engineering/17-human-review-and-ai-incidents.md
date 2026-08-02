# Design Human Review and AI Incident Response

> **Difficulty:** Hard  
> **Main focus:** risk routing, reviewer operations, containment

## Interview prompt

Design the human-review platform and incident controls for high-impact AI decisions.

## 1. Clarify the product and success criteria

**What I would say first:** Human review must have capacity, evidence, permissions, service targets, appeals, and quality controls. Incident response needs independent kill switches for models, prompts, retrieval, memory, and tools.

### Functional requirements

- Route cases by risk, uncertainty, policy, language, and reviewer skill.
- Present evidence without leading reviewers.
- Support decision, escalation, appeal, and immutable audit.
- Detect, contain, investigate, and recover from AI incidents.

### AI and product constraints

- A human can become a rubber stamp under poor UI or overload.
- Review queues can grow faster than staffing.
- Incidents may originate from data, prompts, models, retrieval, tools, or traffic.

## 2. Contracts and data

- ReviewCase {caseId, risk, SLA, evidenceRefs, modelDecision, versions, requiredSkill}
- ReviewDecision {caseId, reviewer, action, reasonCodes, confidence, timestamp}
- IncidentControl {component, version, scope, action=disable|rollback|restrict}

## 3. High-level design

```text
AI decision -> risk router -> auto action
                   |
                   +-> priority review queues -> reviewer workspace
                                                   |
                                      decide/escalate/appeal/audit
                                                   |
                                          quality sampling

telemetry -> incident detection -> control plane kill switches
                                -> evidence preservation -> recovery
```

## 4. Critical request flow

1. Policy calculates review need and queue priority from impact and uncertainty.
2. Router assigns only to a reviewer with the required skill and permission.
3. Workspace shows minimum evidence, provenance, policy, and uncertainty with blinded ordering where useful.
4. Decision applies idempotently, records an immutable audit, and exposes appeal.
5. Incident detection can immediately disable one version or capability while evidence is preserved.

## 5. Quality and evaluation

- Measure reviewer agreement, sampled accuracy, appeal overturns, and policy consistency.
- Calibrate automation thresholds against actual review outcomes without assuming reviewers are always correct.
- Run drills for model rollback, prompt rollback, index disable, and tool disable.
- Regression suites include every confirmed incident and near miss.

## 6. Reliability, scale, observability, and cost

- Forecast arrival and service rates; overload policy may narrow automation or defer low-risk work.
- Avoid assigning the same disturbing category continuously and provide wellness support.
- Keep a known-good degraded mode that does not depend on the failing AI component.
- Track queue age, SLA misses, reviewer throughput, overturns, incident detection/containment time, and recurrence.

## 7. Safety, security, and privacy

- Use least-privilege evidence access, redaction, watermarking, and access audits.
- Separate reviewers, policy authors, and deployment approvers where risk requires it.
- Validate feedback before training and never expose unnecessary victim or personal data.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Review every case | High nominal control but impossible scale and reviewer fatigue. |
| Risk-based review | Efficient with threshold and monitoring responsibility. |
| One global kill switch | Simple but excessive blast radius. |
| Component-level controls | Precise containment with more control-plane work. |

## 9. 60-second interview summary

Risk and uncertainty route cases into skill- and SLA-aware queues, reviewers see provenance-rich minimum evidence, and decisions support audit and appeal. Independent component kill switches, known-good fallbacks, evidence preservation, and incident regression tests make recovery operational.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

