# Design an A/B Experimentation Platform

> **Difficulty:** Hard  
> **Main focus:** stable assignment, exposure logging, trustworthy analysis

## Interview prompt

Design a platform that assigns users to experiments and calculates reliable results.

## 1. Clarify the scope

**What I would say first:** Assignment and exposure are different events. I will keep assignment deterministic and measure only users who were actually exposed under a versioned experiment.

### Functional requirements

- Define experiments, variants, eligibility, allocation, and guardrails.
- Assign a stable unit such as user or account.
- Log assignment, actual exposure, and outcome events.
- Detect broken experiments and produce reproducible analysis.

### Out of scope for the first version

- Automatic causal interpretation for arbitrary observational data is out of scope.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume billions of assignment checks and events per day.
- Assignment is latency-sensitive and should be local; analysis is asynchronous.
- Late outcomes and identity changes complicate joins.

## 3. API and data model

### Main contracts

- evaluate(experimentKey, subjectId, attributes) -> variant and assignmentVersion
- POST /v1/exposures {experiment, subject, variant, version, timestamp}
- POST /v1/experiments {hypothesis, unit, variants, metrics, guardrails}

### Important data

- Experiment(key, status, unit, eligibility, allocation, version, start, end)
- Exposure(experiment, subject_hash, variant, version, timestamp)
- Outcome(subject_hash, metric, value, timestamp)

## 4. High-level design

```text
operator -> experiment control plane -> validated snapshots -> SDK/local assignment
                                                               |
product event -> exposure/outcome stream -> validation -> warehouse
                                                     -> metric jobs
                                                     -> analysis/report
```

## 5. Critical request flow

1. Validate mutually exclusive experiment rules and pre-register metrics.
2. Hash experiment key plus stable subject ID into a deterministic bucket.
3. Log exposure only when the user can actually experience the treatment.
4. Join exposures to outcomes within defined windows using the same analysis unit.
5. Check sample-ratio mismatch and guardrails before reporting effect and uncertainty.

## 6. Deep dive

- Namespace or layer mutually exclusive experiments to prevent hidden interaction.
- Freeze analysis code, metric definitions, and event schemas by version.
- Use account-level assignment when users within one account can affect each other.
- Keep a long-lived holdout for measuring the combined impact of many launches.

## 7. Scaling, failures, and observability

- Automatically pause analysis on sample-ratio mismatch or missing exposure data.
- Serve control when snapshots are missing or invalid unless product specifies otherwise.
- Recompute results from immutable events after fixing analysis code.
- Monitor assignment split, exposure loss, metric delay, guardrail breaches, and novelty effects.

## 8. Security and privacy

- Hash subject identifiers, restrict sensitive attributes, and enforce data retention.
- Require approvals for experiments affecting payments, safety, or regulated outcomes.
- Audit allocations and prevent operators from changing a running test after viewing results.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Server assignment | Trusted attributes with a network or service dependency. |
| Local SDK assignment | Fast and resilient with distributed snapshot management. |
| User randomization | More samples but possible account interference. |
| Account randomization | Cleaner isolation with fewer statistical units. |

## 10. 60-second interview summary

A versioned control plane publishes deterministic assignment snapshots, products log true exposures, and an immutable event pipeline joins outcomes using predeclared metrics. Sample-ratio checks and guardrails stop invalid conclusions before rollout.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you recover and prove no work was lost?
- Which metric best reflects the user's experience?

