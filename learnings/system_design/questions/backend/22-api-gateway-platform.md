# Design an API Gateway and Service Platform

> **Difficulty:** Hard  
> **Main focus:** routing, policy, resilience

## Interview prompt

Design the shared ingress platform for many backend services and teams.

## 1. Clarify the scope

**What I would say first:** The gateway should enforce cross-cutting policy and route traffic, not become a home for business logic. Its data plane must survive control-plane failure.

### Functional requirements

- TLS termination, authentication, routing, rate limits, and request size limits.
- Service discovery, canary routing, timeouts, retries, and circuit breaking.
- Tenant-aware observability and safe configuration rollout.
- Support HTTP, gRPC, and selected streaming connections.

### Out of scope for the first version

- Business validation and data transformation remain inside services.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume millions of requests per second across regions.
- Every added millisecond affects all products.
- A bad configuration has a larger blast radius than one service bug.

## 3. API and data model

### Main contracts

- Control plane: publish Route, Backend, AuthPolicy, RatePolicy, RetryPolicy resources
- Data plane: proxy external request to selected healthy backend
- Admin: validate, diff, canary, promote, and rollback configuration versions

### Important data

- Route(host, path, methods, backend, policies, version)
- Backend(service, endpoints, protocol, health, locality)
- Snapshot(region, version, signed_blob, status)

## 4. High-level design

```text
operators/service registry -> control plane -> validated signed snapshots
                                                |
clients -> edge/load balancer -> gateway fleet -> service endpoints
                                  |   |   |
                                  auth rate telemetry
                                  |
                           last-known-good snapshot
```

## 5. Critical request flow

1. Accept TLS, normalize the request, and reject malformed or oversized input.
2. Match a deterministic route from the local immutable snapshot.
3. Authenticate, authorize coarse route access, and apply rate policy.
4. Select a healthy local backend and proxy with a deadline.
5. Retry only safe operations within the original deadline and emit correlated telemetry.

## 6. Deep dive

- Configuration is schema-validated, referentially validated, canaried, then atomically activated.
- Retries need idempotency and budgets; avoid retrying every layer.
- Endpoint discovery updates are separate from route policy but combine into one consistent data-plane view.
- WebSocket and streaming routes use different timeout and draining behavior.

## 7. Scaling, failures, and observability

- Gateways retain last-known-good config when the control plane is unavailable.
- Circuit breaking and outlier detection remove unhealthy endpoints without ejecting an entire service from one transient error.
- Graceful drain preserves in-flight and streaming connections during rollout.
- Monitor gateway overhead, route misses, auth failures, retry amplification, and per-backend SLOs.

## 8. Security and privacy

- Store private keys in managed key systems, rotate trust bundles, and enforce mTLS internally where required.
- Prevent header spoofing by stripping and rewriting trusted identity headers.
- Restrict admin plane access and audit every policy change.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Rich gateway transformations | Convenient initially but couples business behavior to the platform. |
| Thin policy gateway | Clear ownership and safer evolution. |
| Central control plane | Consistent policy but must not be a runtime dependency. |
| Local immutable snapshots | Fast and resilient with propagation delay. |

## 10. 60-second interview summary

A validated control plane publishes signed immutable snapshots, while regional gateways enforce routing, identity, quotas, deadlines, and coarse resilience locally. Business logic stays in services, and last-known-good config preserves ingress during control-plane failure.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you recover and prove no work was lost?
- Which metric best reflects the user's experience?

