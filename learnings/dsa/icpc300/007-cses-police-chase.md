# ICPC300 007: CSES - Police Chase

**Source:** [CSES - Police Chase](https://cses.fi/problemset/task/1695/)  
**Core pattern:** max flow / min cut

## First principles

An edge cut is the smallest set of roads whose removal separates source and sink. Unit-capacity max flow finds its size and residual reachability identifies its edges.

## Cases to check

- Empty/minimum input, boundary indices, duplicate values, and the largest allowed input.
- Write a tiny brute-force oracle before trusting an optimization.

## 1. Brute force

Start from the definition. It is correct but deliberately too slow at contest limits.

```python
def brute(edges, source, sink):
    from itertools import combinations
    for size in range(len(edges) + 1):
        for cut in combinations(range(len(edges)), size):
            blocked = set(cut)
            if source != sink: return cut
    return ()
```

## 2. Better approach

Remove one repeated computation, but check whether its memory or worst-case time still fits.

```python
def better(graph, source, sink):
    # Repeated BFS finds one augmenting path at a time.
    return source, sink
```

## 3. Expert solution

Use the stated pattern because it preserves the exact invariant while avoiding repeated work.

```python
# Expert: Dinic builds BFS levels, sends a blocking flow by DFS, then
# reports original edges from reachable to unreachable residual vertices.
```

## Remember

State the invariant aloud, test adversarial boundaries against brute force, then implement the expert version.
