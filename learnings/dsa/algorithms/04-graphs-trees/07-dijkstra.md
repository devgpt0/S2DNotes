# Dijkstra's Algorithm

## Idea

Dijkstra finds shortest paths from one source when all edge weights are
non-negative. A min-heap chooses the unfinished vertex with smallest known
distance.

## Visual model

```text
known shortest region -- cheapest crossing edge/path --> next settled vertex
```

## Classroom board: relax cheaper routes

```text
A->B cost 5, A->C cost 1, C->B cost 2

start: dist A=0, B=∞, C=∞
pop A -> B=5, C=1; heap [(1,C),(5,B)]
pop C -> B improves to 3; heap [(3,B),(5,B)]
pop B at 3 -> final
later pop B at 5 -> stale; skip
```

The heap may contain old guesses; the distance array is the source of truth.

## Steps

1. Set the start distance to `0`; all others are infinity.
2. Push `(distance, vertex)` into a min-heap.
3. Skip a popped entry if it is stale.
4. Relax every outgoing edge and push improved distances.

## First-principles derivation

Repeatedly select the unfinished vertex with the smallest known distance. Since
all remaining edges are non-negative, no route through a farther vertex can
later improve it.

The heap proposes candidates; the distance array is the source of truth, so
older heap entries must be skipped.

## Pattern recognition

Use Dijkstra for minimum-cost paths with non-negative weights. Use BFS for all
weights `1`, 0-1 BFS for weights `0/1`, and Bellman-Ford for negative edges.

## Implementation

### C++

```cpp
std::vector<long long> dijkstra(const std::vector<std::vector<std::pair<int, int>>>& graph, int start) {
    const long long infinity = std::numeric_limits<long long>::max() / 4;
    std::vector<long long> distance(graph.size(), infinity);
    using State = std::pair<long long, int>;
    std::priority_queue<State, std::vector<State>, std::greater<>> heap;
    distance[start] = 0;
    heap.push({0, start});
    while (!heap.empty()) {
        const auto [currentDistance, vertex] = heap.top();
        heap.pop();
        if (currentDistance != distance[vertex]) continue;
        for (const auto& [neighbor, weight] : graph[vertex]) {
            const long long candidate = currentDistance + weight;
            if (candidate < distance[neighbor]) {
                distance[neighbor] = candidate;
                heap.push({candidate, neighbor});
            }
        }
    }
    return distance;
}
```

### Python

```python
import heapq


def dijkstra(graph: list[list[tuple[int, int]]], start: int) -> list[int]:
    infinity = 10**30
    distance = [infinity] * len(graph)
    distance[start] = 0
    heap = [(0, start)]
    while heap:
        current_distance, vertex = heapq.heappop(heap)
        if current_distance != distance[vertex]:
            continue
        for neighbor, weight in graph[vertex]:
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return distance
```

### Java

```java
record Edge(int to, int weight) {}
record State(long distance, int vertex) {}

static long[] dijkstra(List<List<Edge>> graph, int start) {
    long[] distance = new long[graph.size()];
    Arrays.fill(distance, Long.MAX_VALUE / 4);
    PriorityQueue<State> heap = new PriorityQueue<>(Comparator.comparingLong(State::distance));
    distance[start] = 0;
    heap.add(new State(0, start));
    while (!heap.isEmpty()) {
        State state = heap.remove();
        if (state.distance() != distance[state.vertex()]) continue;
        for (Edge edge : graph.get(state.vertex())) {
            long candidate = state.distance() + edge.weight();
            if (candidate < distance[edge.to()]) {
                distance[edge.to()] = candidate;
                heap.add(new State(candidate, edge.to()));
            }
        }
    }
    return distance;
}
```

## Why it works

With non-negative edges, no later path through a farther unfinished vertex can
improve the smallest heap distance. That distance is final when popped fresh.

## Complexity

With an adjacency list and binary heap, time is `O((V + E) log V)` and space is
`O(V + E)`.

## Common mistakes

- Using Dijkstra with negative edges.
- Forgetting to skip stale heap entries.
- Using a max-heap by accident.
- Letting infinity plus a weight overflow.
