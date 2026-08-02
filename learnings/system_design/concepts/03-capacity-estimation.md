# Capacity Estimation

## Idea

Estimation reveals the correct architecture class and its bottlenecks. Orders
of magnitude matter more than false precision.

## Visual model

```text
daily actions / 86,400 = average QPS
peak QPS = average QPS * peak factor
storage/year = writes/day * bytes/write * 365 * replication
```

## Design steps

1. Estimate daily active users and actions per user.
2. Convert to average and peak reads/writes per second.
3. Estimate record, media, and index sizes.
4. Calculate network egress and retention growth.
5. Identify skew: one celebrity, tenant, document, or model may dominate.

## Example

`10M` users × `20` feed reads/day = `200M/day`, about `2.3K` average QPS.
At a `10x` peak, plan near `23K` QPS, then add measured safety margin.

## When to use it

Estimate enough to choose single-node vs distributed storage, push vs pull,
cache size, partitions, and synchronous vs asynchronous work.

## Common mistakes

- Using average traffic as capacity.
- Ignoring replicas, indexes, metadata, and backups.
- Treating every object as the same size.
- Forgetting egress and model/GPU cost.
