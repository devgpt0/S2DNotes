# Breadth-First Search (BFS)

## Idea

BFS explores an unweighted graph layer by layer. It finds the minimum number
of edges from a start vertex to every reachable vertex.

## Visual model

```text
distance 0: start
distance 1: all direct neighbors
distance 2: their unvisited neighbors
```

## Classroom board: shortest unweighted path

```text
edges: A-B, A-C, B-D, C-D

queue [A], distance A=0
remove A -> discover B,C at distance 1; queue [B,C]
remove B -> discover D at distance 2;   queue [C,D]
remove C -> D was already reached in 2; do not add again
```

The first time BFS reaches a vertex is through the fewest edges.

## Steps

1. Set all distances to `-1` and the start distance to `0`.
2. Add the start to a queue.
3. Remove one vertex and inspect its neighbors.
4. Mark and enqueue each unseen neighbor with distance `current + 1`.

## First-principles derivation

In an unweighted graph, every edge adds one step. Therefore all vertices at
distance `d` must be processed before vertices at distance `d + 1`.

A FIFO queue preserves exactly that layer order; the first discovery of a
vertex gives its shortest distance.

## Pattern recognition

Use BFS for shortest paths with equal edge cost, minimum moves, levels,
multi-source spreading, or reachability by fewest steps.

## Implementation

### C++

```cpp
std::vector<int> bfs(const std::vector<std::vector<int>>& graph, int start) {
    std::vector<int> distance(graph.size(), -1);
    std::queue<int> queue;
    distance[start] = 0;
    queue.push(start);
    while (!queue.empty()) {
        const int vertex = queue.front();
        queue.pop();
        for (int neighbor : graph[vertex]) {
            if (distance[neighbor] != -1) continue;
            distance[neighbor] = distance[vertex] + 1;
            queue.push(neighbor);
        }
    }
    return distance;
}
```

### Python

```python
from collections import deque


def bfs(graph: list[list[int]], start: int) -> list[int]:
    distance = [-1] * len(graph)
    distance[start] = 0
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            if distance[neighbor] != -1:
                continue
            distance[neighbor] = distance[vertex] + 1
            queue.append(neighbor)
    return distance
```

### Java

```java
static int[] bfs(List<List<Integer>> graph, int start) {
    int[] distance = new int[graph.size()];
    Arrays.fill(distance, -1);
    Queue<Integer> queue = new ArrayDeque<>();
    distance[start] = 0;
    queue.add(start);
    while (!queue.isEmpty()) {
        int vertex = queue.remove();
        for (int neighbor : graph.get(vertex)) {
            if (distance[neighbor] != -1) continue;
            distance[neighbor] = distance[vertex] + 1;
            queue.add(neighbor);
        }
    }
    return distance;
}
```

## Why it works

The queue processes vertices in non-decreasing distance. The first time a
vertex is reached therefore uses the fewest possible edges.

## Complexity

Time is `O(V + E)` and space is `O(V)` besides the graph.

## Common mistakes

- Marking visited when dequeued instead of enqueued, causing duplicates.
- Using BFS when edge weights differ.
- Forgetting to start from every source in a multi-source problem.
