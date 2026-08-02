# Design a Feature Flag and Dynamic Configuration Service

> **Difficulty:** Medium  
> **Main focus:** low-latency evaluation, safe rollout, consistency

## Interview prompt

Design feature flags used by many services and clients for gradual rollouts and emergency disables.

## 1. Clarify the scope

**What I would say first:** Evaluation must continue when the control plane is down. I will distribute immutable versioned snapshots and keep the hot path local.

### Functional requirements

- Create boolean, multivariate, and percentage flags.
- Target by tenant, user attributes, environment, and stable cohorts.
- Propagate changes quickly and support instant rollback.
- Audit every change and prevent unsafe client exposure.

### Out of scope for the first version

- A full experimentation statistics platform is a separate question.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume billions of evaluations per second across server and client SDKs.
- A remote network call per evaluation is unacceptable.
- Configuration writes are rare but operationally sensitive.

## 3. API and data model

### Main contracts

- PUT /v1/projects/{id}/flags/{key} {rules, variants, version}
- GET /sdk/v1/snapshot?environment=prod
- stream /sdk/v1/updates

### Important data

- Flag(project_id, key, environment, rules, version, status)
- Snapshot(environment, version, content_hash, object_ref)
- AuditChange(actor, flag_key, before, after, approved_at)

## 4. High-level design

```text
operator -> control API -> config database -> validator/approval
                                              |
                                      snapshot builder
                                              |
                                     CDN + update stream
                                              |
service/client SDK -> local immutable snapshot -> evaluation
```

## 5. Critical request flow

1. Validate rule schema and detect conflicting or unreachable rules.
2. Require approval for protected production environments.
3. Commit a new version, build a signed snapshot, and publish an update hint.
4. SDK downloads and atomically swaps the complete snapshot.
5. Evaluation hashes a stable subject key into a deterministic rollout bucket.

## 6. Deep dive

- Server flags may use trusted attributes; public client snapshots must contain no secret rules.
- Deterministic hashing keeps users in one cohort as instances change.
- Prerequisites and rule order need cycle checks and explicit semantics.
- SDK retains the last known good snapshot and a safe default for missing flags.

## 7. Scaling, failures, and observability

- Bad snapshots fail verification and never replace the current version.
- The data plane continues locally during control-plane or network outages.
- A kill switch can use a small high-priority update channel but still needs authentication.
- Monitor propagation delay, evaluation errors, snapshot age, and fallback usage.

## 8. Security and privacy

- Use environment-scoped SDK credentials and least-privilege operator roles.
- Audit and optionally require two-person approval for high-impact flags.
- Do not place secrets or sensitive targeting values in browser-delivered config.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Remote evaluation | Central rules but unacceptable latency and dependency risk. |
| Local evaluation | Fast and resilient but requires snapshot distribution. |
| Delta updates | Small transfers but harder recovery. |
| Full immutable snapshots | Larger transfers with simple atomic rollback. |

## 10. 60-second interview summary

The control plane validates and audits changes, then publishes signed immutable snapshots. SDKs evaluate locally using deterministic hashing and last-known-good state, so the data path survives control-plane failure and rollbacks are one version switch.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you test recovery from a dependency timeout?
- Which metric best reflects the user's experience?

