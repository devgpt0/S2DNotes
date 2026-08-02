# A Repeatable System Design Interview Framework

## Idea

System design is a sequence of decisions, not a memorized diagram. Make the
problem smaller before making the system larger.

## Visual model

```text
clarify -> estimate -> contract/data -> architecture -> deep dive -> operate
```

## Design steps

1. Clarify users, core actions, and what is out of scope.
2. Rank non-functional needs: availability, consistency, latency, durability,
   privacy, and cost.
3. Estimate traffic, storage, bandwidth, and hot-key risk.
4. Define APIs/events and the data model from access patterns.
5. Draw the smallest end-to-end design.
6. Deep-dive the hardest two parts.
7. Walk through overload, dependency failure, recovery, security, and metrics.

## When to use it

Use this order for every interview prompt. Spend roughly 5 minutes scoping,
5 estimating/contracts, 20–25 designing, and the remainder on trade-offs.

## Trade-offs

Breadth proves coverage; depth proves engineering judgment. Tell the interviewer
where you want to go deeper instead of silently skipping areas.

## Common mistakes

- Drawing microservices before requirements.
- Giving exact numbers without assumptions.
- Naming products instead of explaining required properties.
- Claiming perfect availability, consistency, latency, and low cost together.
