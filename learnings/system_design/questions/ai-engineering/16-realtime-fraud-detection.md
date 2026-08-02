# Design a Real-Time Fraud Detection System

> **Difficulty:** Hard  
> **Main focus:** streaming features, adversarial drift, decisions

## Interview prompt

Design a low-latency fraud system for payments, account login, or marketplace activity.

## 1. Clarify the product and success criteria

**What I would say first:** Fraud is adversarial and labels are delayed. I will combine deterministic rules, online features, a calibrated model, and an action policy with review and appeal.

### Functional requirements

- Score events within a strict transaction latency.
- Allow, challenge, hold, or block according to risk and policy.
- Use device, account, velocity, graph, and historical signals.
- Learn from confirmed outcomes while resisting manipulated feedback.

### AI and product constraints

- Attack patterns shift after defenses change.
- False positives harm legitimate users; false negatives cause loss.
- Chargebacks and investigations may arrive weeks later.

## 2. Contracts and data

- POST /v1/risk-decisions {eventId, actor, device, amount, context} -> action, reason codes, decisionId
- Feature {entity, name, value, eventTime, computedAt, version}
- Outcome {decisionId, label, source, confidence, observedAt}

## 3. High-level design

```text
events -> stream processing -> online feature store
   |              |                  |
   |              +-> velocity/graph |
   v                                 v
decision API -> rules -> calibrated model -> policy/action
                  |          |             |
                  +-> reason codes         +-> challenge/review
events/outcomes -> offline point-in-time features -> training/evaluation
```

## 4. Critical request flow

1. Deduplicate event ID and fetch fresh online features under a deadline.
2. Apply hard rules for known invalid or prohibited cases.
3. Score with a versioned calibrated model and record feature/model lineage.
4. Policy maps score plus product context to allow, challenge, hold, or block.
5. Join delayed trusted outcomes for monitoring, investigation, and future training.

## 5. Quality and evaluation

- Evaluate precision-recall and monetary/user cost at actual policy thresholds.
- Use point-in-time-correct data to prevent future chargeback information leaking into training.
- Segment by attack type, region, merchant, new users, and legitimate high-value behavior.
- Use champion/challenger shadowing and monitor attacker adaptation after launch.

## 6. Reliability, scale, observability, and cost

- Fallback rules and cached features handle temporary model or feature-store failure.
- Bound feature age and return explicit unknown values rather than silent defaults.
- Rate-limit expensive graph features and precompute what the latency path needs.
- Track loss, false-positive proxies, challenge completion, feature freshness, drift, latency, and review queue.

## 7. Safety, security, and privacy

- Restrict sensitive features, encrypt identifiers, and audit investigator access.
- Provide reason codes suitable for operations and required user notices without revealing exploitable rules.
- Protect outcome pipelines against poisoned labels and insider manipulation.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Aggressive blocking | Lower immediate fraud with more legitimate-user harm. |
| Step-up challenge | Recovers good users but adds friction and provider cost. |
| Complex online graph | Strong signal with latency and availability risk. |
| Precomputed features | Fast decisions with some staleness. |

## 9. 60-second interview summary

Streaming pipelines maintain fresh point-in-time features, a fast decision service combines hard rules and a calibrated model, and policy chooses allow, challenge, hold, or block. Delayed trusted labels, drift monitoring, fallbacks, and human review address adversarial change.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

