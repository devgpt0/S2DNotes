# 0-1 BFS

## Idea

0-1 BFS finds shortest paths when every edge weight is exactly `0` or `1`.
Use a deque: a zero-cost improvement goes to the front; a one-cost improvement
goes to the back.

## Visual model

```text
weight 0 -> front [process soon ... later] back <- weight 1
```

## Classroom board: free move goes first

```text
at A, distance 4
A -> B costs 1 -> candidate distance 5 -> add B to back
A -> C costs 0 -> candidate distance 4 -> add C to front

deque [C, ..., B]
```

`C` must be processed before a more expensive pending state, which is exactly
what the deque provides.

## Steps

1. Set start distance to `0` and add it to the deque.
2. Remove the front vertex.
3. Relax each outgoing edge.
4. Put an improved neighbor at the front for weight `0`, otherwise at the back.

## First-principles derivation

BFS works because every transition costs the same. With costs `0` and `1`,
a zero-cost improvement belongs to the current distance layer and a one-cost
improvement belongs to the next layer.

A deque puts zero-cost moves at the front and one-cost moves at the back,
preserving nondecreasing distance order.

## Pattern recognition

Use it for binary costs: free versus paid moves, same-direction versus changed
direction, or edges labeled `0/1`. Use Dijkstra for other non-negative weights.

## Implementation

### C++

```cpp
std::vector<long long> zeroOneBfs(const std::vector<std::vector<std::pair<int, int>>>& graph, int start) {
    const long long infinity = std::numeric_limits<long long>::max() / 4;
    std::vector<long long> distance(graph.size(), infinity);
    std::deque<int> deque{start};
    distance[start] = 0;
    while (!deque.empty()) {
        const int vertex = deque.front();
        deque.pop_front();
        for (const auto& [neighbor, weight] : graph[vertex]) {
            if (distance[vertex] + weight >= distance[neighbor]) continue;
            distance[neighbor] = distance[vertex] + weight;
            if (weight == 0) deque.push_front(neighbor);
            else deque.push_back(neighbor);
        }
    }
    return distance;
}
```

### Python

```python
from collections import deque


def zero_one_bfs(graph: list[list[tuple[int, int]]], start: int) -> list[int]:
    infinity = 10**30
    distance = [infinity] * len(graph)
    distance[start] = 0
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbor, weight in graph[vertex]:
            candidate = distance[vertex] + weight
            if candidate >= distance[neighbor]:
                continue
            distance[neighbor] = candidate
            if weight == 0:
                queue.appendleft(neighbor)
            else:
                queue.append(neighbor)
    return distance
```

### Java

```java
record Edge(int to, int weight) {}

static long[] zeroOneBfs(List<List<Edge>> graph, int start) {
    long[] distance = new long[graph.size()];
    Arrays.fill(distance, Long.MAX_VALUE / 4);
    Deque<Integer> queue = new ArrayDeque<>();
    distance[start] = 0;
    queue.add(start);
    while (!queue.isEmpty()) {
        int vertex = queue.removeFirst();
        for (Edge edge : graph.get(vertex)) {
            long candidate = distance[vertex] + edge.weight();
            if (candidate >= distance[edge.to()]) continue;
            distance[edge.to()] = candidate;
            if (edge.weight() == 0) queue.addFirst(edge.to());
            else queue.addLast(edge.to());
        }
    }
    return distance;
}
```

## Why it works

The deque keeps pending vertices ordered by distance difference of at most one.
Zero-cost improvements must be processed before one-cost moves.

## Complexity

Time is `O(V + E)` and space is `O(V)` besides the graph.

## Common mistakes

- Using it when a weight can be `2` or negative.
- Reversing front and back insertion.
- Marking a vertex permanently visited before all relaxations.
