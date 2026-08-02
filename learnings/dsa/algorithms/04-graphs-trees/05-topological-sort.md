# Topological Sort

## Idea

A topological order places every directed edge `u -> v` with `u` before `v`.
It exists exactly for a directed acyclic graph (DAG).

## Visual model

```text
prerequisite -> course
zero indegree vertices are ready now
```

## Classroom board: remove ready work

```text
A -> C, B -> C, C -> D
indegree: A=0, B=0, C=2, D=1

ready [A,B]
remove A -> C indegree 1
remove B -> C indegree 0; add C
remove C -> D indegree 0; add D
order A,B,C,D (B,A,C,D is also valid)
```

## Steps: Kahn's algorithm

1. Count each vertex's incoming edges.
2. Queue every zero-indegree vertex.
3. Remove one ready vertex and append it to the order.
4. Remove its outgoing edges; queue neighbors whose indegree becomes zero.
5. If fewer than `V` vertices are output, a cycle exists.

## First-principles derivation

A vertex can be placed next only after all its prerequisites are placed.
Indegree counts how many prerequisites remain.

Removing an indegree-zero vertex satisfies one prerequisite of each neighbor.
If no such vertex exists before all vertices are removed, a cycle blocks the
order.

## Pattern recognition

Use topological sorting for prerequisites, dependency build order, DAG DP, or
any “must happen before” relation.

## Implementation

### C++

```cpp
std::vector<int> topologicalSort(const std::vector<std::vector<int>>& graph) {
    std::vector<int> indegree(graph.size(), 0);
    for (const auto& neighbors : graph) for (int neighbor : neighbors) ++indegree[neighbor];
    std::queue<int> queue;
    for (int vertex = 0; vertex < static_cast<int>(graph.size()); ++vertex) if (indegree[vertex] == 0) queue.push(vertex);
    std::vector<int> order;
    while (!queue.empty()) {
        const int vertex = queue.front();
        queue.pop();
        order.push_back(vertex);
        for (int neighbor : graph[vertex]) if (--indegree[neighbor] == 0) queue.push(neighbor);
    }
    return order.size() == graph.size() ? order : std::vector<int>{};
}
```

### Python

```python
from collections import deque


def topological_sort(graph: list[list[int]]) -> list[int]:
    indegree = [0] * len(graph)
    for neighbors in graph:
        for neighbor in neighbors:
            indegree[neighbor] += 1
    queue = deque(vertex for vertex, degree in enumerate(indegree) if degree == 0)
    order: list[int] = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph[vertex]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == len(graph) else []
```

### Java

```java
static int[] topologicalSort(List<List<Integer>> graph) {
    int[] indegree = new int[graph.size()];
    for (List<Integer> neighbors : graph) for (int neighbor : neighbors) indegree[neighbor]++;
    Queue<Integer> queue = new ArrayDeque<>();
    for (int vertex = 0; vertex < graph.size(); vertex++) if (indegree[vertex] == 0) queue.add(vertex);
    int[] order = new int[graph.size()];
    int write = 0;
    while (!queue.isEmpty()) {
        int vertex = queue.remove();
        order[write++] = vertex;
        for (int neighbor : graph.get(vertex)) if (--indegree[neighbor] == 0) queue.add(neighbor);
    }
    return write == graph.size() ? order : new int[0];
}
```

## Why it works

A zero-indegree vertex has no unmet prerequisite. Removing it cannot violate
any edge; a cycle prevents every remaining vertex from becoming ready.

## Complexity

Time is `O(V + E)` and space is `O(V)`.

## Common mistakes

- Reversing prerequisite edges.
- Forgetting isolated vertices.
- Returning a partial order when a cycle exists.
- Assuming the valid order is unique.
