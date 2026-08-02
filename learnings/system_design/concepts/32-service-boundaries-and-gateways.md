# Service Boundaries, API Gateways, and BFFs

## Idea

Service boundaries should follow cohesive business capabilities and ownership,
not technical layers. An API gateway handles cross-cutting edge concerns; a
backend-for-frontend (BFF) shapes APIs for one client experience.

## Visual model

```text
web/mobile -> edge gateway -> BFF/domain APIs -> services -> owned data
                 |
                 +-> auth, routing, limits, telemetry (not business truth)
```

## Design steps

1. Start with a modular monolith unless independent scale/ownership is proven.
2. Identify domain boundaries, invariants, data ownership, and team ownership.
3. Define contracts and avoid shared write ownership of one database table.
4. Put authentication, routing, coarse limits, and observability at the gateway.
5. Keep authorization/business rules in the owning service too.
6. Use BFFs only when client workflows genuinely differ.

## When to split a service

Split when a capability needs independent scaling, release cadence, reliability,
security isolation, or clear long-term ownership. Do not split only to use a new
technology.

## Trade-offs

Smaller services improve autonomy and fault isolation but add network failures,
eventual consistency, deployment coordination, and operational cost.

## Evolution path

```text
modular monolith -> measure coupling/hotspots -> extract one boundary
                 -> establish platform/observability -> repeat only if valuable
```

## Common mistakes

- Gateway containing domain business logic.
- Shared database used as an undocumented integration API.
- One service per table/entity.
- Synchronous call chains spanning many services for one user request.
