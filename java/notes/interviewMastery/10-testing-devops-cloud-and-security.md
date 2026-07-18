# 10 - Testing, DevOps, Cloud, and Security Interviews

## Testing

- test pyramid and boundaries
- contract tests for APIs/events
- Testcontainers for real infrastructure semantics
- deterministic time/random/ID sources
- load, soak, stress, and chaos tests
- mutation testing and coverage limitations
- flaky-test diagnosis

## CI/CD

```text
checkout -> dependency verification -> compile -> unit tests -> static/security checks
-> integration/contract tests -> artifact + SBOM -> sign -> deploy -> verify -> promote/rollback
# Result: one immutable artifact moves through controlled environments.
```

Know rolling, blue-green, and canary deployments; backward-compatible migrations; feature flags; automated rollback signals; and separation of build-time from runtime secrets.

## Containers and Kubernetes

- image layers, non-root execution, read-only filesystem
- requests vs limits and JVM container awareness
- liveness vs readiness vs startup probes
- Deployment, Service, ConfigMap, Secret, Ingress/Gateway
- horizontal autoscaling signals and cold-start behavior
- graceful shutdown and Pod disruption
- logs to stdout, metrics/traces to collectors

## Security

- authentication vs authorization
- least privilege and defense in depth
- OWASP injection, SSRF, XSS, CSRF, traversal, unsafe deserialization
- OAuth2 roles: resource owner/client/authorization/resource server
- OIDC identity layer and JWT validation
- TLS and secret rotation
- dependency/SBOM/image scanning
- threat modeling and incident response

## Cloud Tradeoffs

Know managed vs self-hosted services, multi-zone design, autoscaling limits, egress/data-transfer cost, identity roles, encryption keys, backup restoration, and vendor lock-in.
