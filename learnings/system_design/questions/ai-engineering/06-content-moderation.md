# Design an AI Content Moderation Pipeline

> **Difficulty:** Hard  
> **Main focus:** multi-stage classification, policy, human review

## Interview prompt

Design moderation for text, image, audio, and video uploads at large scale.

## 1. Clarify the product and success criteria

**What I would say first:** Models estimate signals; a versioned policy engine decides actions. High-impact uncertain cases go to trained human review with appeals.

### Functional requirements

- Scan content before or shortly after publication.
- Support multiple modalities and policy categories.
- Block, limit, label, allow, or route to human review.
- Handle policy versions, appeals, emergency rules, and audit.

### AI and product constraints

- False positives and false negatives both cause harm.
- Video and live content require sampled or streaming analysis.
- Policy varies by age, region, product surface, and legal obligation.

## 2. Contracts and data

- POST /v1/moderation {contentId, contentVersion, modality, objectRef, context}
- Signal {modelVersion, category, score, evidenceRef}
- Decision {policyVersion, action, reasons, reviewRequired, expiresAt?}

## 3. High-level design

```text
upload/live stream -> basic validation/hash match
                      |
                modality preprocessing
              / text / image / audio / video
                      |
                  model signals
                      |
           versioned policy decision engine
              | allow/label | block | review queue
                                      |
                                reviewer/appeal
                                      |
                              audit + training curation
```

## 4. Critical request flow

1. Validate media and check exact known-illegal hashes where legally appropriate.
2. Extract text, frames, audio, or metadata in isolated processing.
3. Run category models and calibrate scores by content class.
4. Policy engine combines signals, user context, region, and policy version.
5. Apply action idempotently; queue uncertain high-impact cases with evidence and priority.

## 5. Quality and evaluation

- Report precision and recall per category at policy thresholds, not one aggregate accuracy.
- Use adjudicated, diverse, time-sliced test sets and track reviewer disagreement.
- Shadow new models and policies before changing actions.
- Measure appeal overturns and downstream harm, not only model labels.

## 6. Reliability, scale, observability, and cost

- Prioritize imminent harm and live streams; degrade low-risk scans under overload.
- Model or preprocessing failure follows an explicit policy: quarantine, limited publish, or fallback.
- Keep a kill switch for each model, rule, and content surface.
- Track decision latency, queue age, reviewer capacity, category drift, appeal rate, and missed-harm incidents.

## 7. Safety, security, and privacy

- Least-privilege reviewer access, redacted context, wellness controls, and immutable access audit are required.
- Protect victims' data and tightly control illegal-content evidence.
- Do not automatically train on raw reviewer actions without quality checks and policy-version context.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Pre-publication review | Prevents exposure but increases latency. |
| Post-publication review | Fast publishing with possible harm window. |
| Single model threshold | Simple but ignores product and category costs. |
| Policy over calibrated signals | Flexible and auditable with more governance. |

## 9. 60-second interview summary

Modality-specific models produce calibrated signals, and a deterministic versioned policy engine chooses product actions. Uncertain high-impact cases enter a protected human-review and appeal flow, while per-category evaluation, overload policy, and kill switches support safe operations.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

