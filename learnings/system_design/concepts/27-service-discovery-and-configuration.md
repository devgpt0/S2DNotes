# Service Discovery and Dynamic Configuration

## Idea

Instances change continuously. Discovery maps a logical service name to healthy
endpoints; configuration changes behavior without rebuilding the application.
Both are control-plane concerns and must fail safely.

## Visual model

```text
instances -> register/health -> service registry
client/load balancer --------> resolve healthy endpoints

config author -> validated version -> staged rollout -> watchers
```

## Design steps

1. Choose client-side discovery, a proxy/sidecar, or platform load balancing.
2. Register endpoints with leases and separate readiness from liveness.
3. Cache discovery results with bounded staleness and retry other endpoints.
4. Store typed, versioned configuration with validation and ownership.
5. Roll out config progressively and preserve a known-good rollback version.

## When to use it

Use dynamic discovery in elastic/containerized fleets. Use dynamic configuration
for operational values such as feature rollout, limits, and routing—not secrets
or arbitrary executable behavior.

## Trade-offs

Central control simplifies management but becomes a high-impact dependency.
Cached state improves availability but may route to removed instances briefly.

## Failure modes and safeguards

- Registry unavailable: use last known endpoints, not an empty fleet.
- Bad config: schema validation, canary rollout, automatic rollback.
- Thundering refresh: jitter watchers and use push plus periodic reconciliation.
- Split control plane: attach monotonically increasing versions to every update.

## Common mistakes

- Using health checks that report ready before dependencies/migrations are ready.
- Storing secrets in ordinary config systems.
- Updating every instance at once.
- Letting stale instances accept traffic indefinitely after lease expiry.
