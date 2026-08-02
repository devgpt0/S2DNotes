# Cost and Capacity Engineering

## Idea

A design is incomplete until it can meet its SLO at an affordable cost. Capacity
planning converts workload forecasts into compute, memory, storage, network,
queue, and regional headroom.

## Visual model

```text
demand forecast + SLO + failure headroom
       -> capacity model -> load test -> autoscaling bounds -> cost allocation
```

## Design steps

1. Measure workload units: requests, bytes, events, tokens, GPU-seconds, tenants.
2. Benchmark one instance/partition under representative load and data shape.
3. Model average, peak, burst, growth, and one-zone/instance failure.
4. Set autoscaling signals, minimums, maximums, and warm-up time.
5. Attribute cost to product/tenant/model and establish budgets/alerts.
6. Revisit architecture at clear scale or cost breakpoints.

## When to use it

During design, launch readiness, major growth, cloud migration, and any time
unit cost or SLO burn changes materially.

## Trade-offs

More headroom improves resilience but costs money. High utilization looks cheap
until a burst or failure removes the remaining margin.

## Useful unit economics

- Cost per successful request/job/GB/token/customer.
- Cache hit savings versus invalidation/storage cost.
- Reserved/base capacity plus burst/on-demand capacity.
- Storage growth including replicas, indexes, backups, and derived data.

## Common mistakes

- Sizing from average traffic only.
- Autoscaling on CPU when queue age or latency is the real bottleneck.
- Ignoring data transfer, observability, replicas, and idle GPU cost.
- Optimizing cloud cost by removing required failure headroom.
