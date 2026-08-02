# Bellman-Ford

## Idea

Bellman-Ford finds single-source shortest paths even with negative edge
weights. It can also detect a negative cycle reachable from the source.

## Visual model

One full pass over all edges can extend a known shortest path by one edge. A
simple shortest path uses at most `V - 1` edges.

## Classroom board: improvements travel one edge per pass

```text
A->B = 4, B->C = -6, A->C = 5
start: A=0, B=∞, C=∞
pass 1: B=4, C becomes -2 through B (better than 5)
pass 2: no change -> stop
```

If a `V`-th pass still improves a distance, the route used a negative cycle.

## Steps

1. Set the source distance to `0` and others to infinity.
2. Repeat `V - 1` times: relax every directed edge.
3. Stop early if a full pass changes nothing.
4. Relax once more; any improvement means a reachable negative cycle.

## First-principles derivation

Any shortest simple path uses at most `V - 1` edges. One full relaxation pass
can extend correct shortest paths by one edge.

After `V - 1` passes all reachable shortest paths are known. A further
improvement proves a reachable negative cycle.

## Pattern recognition

Use it for negative edges, negative-cycle detection, or small graphs where
`O(VE)` fits. Use Dijkstra when all weights are non-negative.

## Implementation

### C++

```cpp
struct Edge { int from; int to; long long weight; };

std::optional<std::vector<long long>> bellmanFord(int vertexCount, const std::vector<Edge>& edges, int start) {
    const long long infinity = std::numeric_limits<long long>::max() / 4;
    std::vector<long long> distance(vertexCount, infinity);
    distance[start] = 0;
    for (int pass = 0; pass < vertexCount - 1; ++pass) {
        bool changed = false;
        for (const Edge& edge : edges) {
            if (distance[edge.from] == infinity) continue;
            const long long candidate = distance[edge.from] + edge.weight;
            if (candidate < distance[edge.to]) {
                distance[edge.to] = candidate;
                changed = true;
            }
        }
        if (!changed) break;
    }
    for (const Edge& edge : edges) {
        if (distance[edge.from] != infinity && distance[edge.from] + edge.weight < distance[edge.to]) return std::nullopt;
    }
    return distance;
}
```

### Python

```python
def bellman_ford(
    vertex_count: int, edges: list[tuple[int, int, int]], start: int
) -> list[int] | None:
    infinity = 10**30
    distance = [infinity] * vertex_count
    distance[start] = 0
    for _ in range(vertex_count - 1):
        changed = False
        for source, target, weight in edges:
            if distance[source] == infinity:
                continue
            candidate = distance[source] + weight
            if candidate < distance[target]:
                distance[target] = candidate
                changed = True
        if not changed:
            break
    for source, target, weight in edges:
        if distance[source] != infinity and distance[source] + weight < distance[target]:
            return None
    return distance
```

### Java

```java
record Edge(int from, int to, long weight) {}

static long[] bellmanFord(int vertexCount, List<Edge> edges, int start) {
    long infinity = Long.MAX_VALUE / 4;
    long[] distance = new long[vertexCount];
    Arrays.fill(distance, infinity);
    distance[start] = 0;
    for (int pass = 0; pass < vertexCount - 1; pass++) {
        boolean changed = false;
        for (Edge edge : edges) {
            if (distance[edge.from()] == infinity) continue;
            long candidate = distance[edge.from()] + edge.weight();
            if (candidate < distance[edge.to()]) {
                distance[edge.to()] = candidate;
                changed = true;
            }
        }
        if (!changed) break;
    }
    for (Edge edge : edges) {
        if (distance[edge.from()] != infinity
            && distance[edge.from()] + edge.weight() < distance[edge.to()]) return null;
    }
    return distance;
}
```

## Why it works

After pass `k`, every shortest path using at most `k` edges is correct. A path
that still improves after `V - 1` passes must repeat a vertex and use a
negative cycle.

## Complexity

Time is `O(VE)` and space is `O(V)`.

## Common mistakes

- Relaxing from infinity.
- Reporting a negative cycle that is unreachable from the source.
- Forgetting that an undirected negative edge immediately forms a negative
  two-edge walk.
