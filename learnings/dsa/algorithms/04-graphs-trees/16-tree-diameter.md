# Tree Diameter

## Idea

The diameter is the longest simple path in a tree. Two BFS/DFS traversals find
it in an unweighted tree.

## Visual model

```text
arbitrary start --BFS--> endpoint A --BFS--> farthest endpoint B
                                           distance(A, B) is the diameter
```

## Classroom board: two farthest searches

```text
tree path 0-1-2-3 with branch 1-4
start 0 -> a farthest endpoint is 3
start 3 -> farthest is 0, distance 3 edges
diameter length = 3
```

## Steps

1. Run BFS from any vertex and take a farthest vertex `A`.
2. Run BFS from `A`.
3. The largest distance in the second run is the diameter.

## First-principles derivation

In a tree there is one path between every pair. Starting anywhere, a farthest
vertex lies at an endpoint of some diameter; starting again there finds the
opposite endpoint.

The second traversal distance is the maximum path length.

## Classroom board: two farthest searches

```text
0 - 1 - 2 - 3
        |
        4

start 0: farthest is 3 (distance 3)
start 3: distances
3:0, 2:1, 1:2, 4:2, 0:3

farthest is 0; diameter path is 3-2-1-0, length 3
```

Vertex `4` is a branch, but its longest path to an endpoint has length only
`2`.

## Pattern recognition

Use it for a longest path in a tree, tree centers, or minimum height after
choosing a root. This two-search rule does not work on arbitrary graphs.

## Implementation

### C++

```cpp
std::pair<int, int> farthest(const std::vector<std::vector<int>>& tree, int start) {
    std::vector<int> distance(tree.size(), -1);
    std::queue<int> queue;
    distance[start] = 0;
    queue.push(start);
    int farthestVertex = start;
    while (!queue.empty()) {
        const int vertex = queue.front();
        queue.pop();
        if (distance[vertex] > distance[farthestVertex]) farthestVertex = vertex;
        for (int neighbor : tree[vertex]) if (distance[neighbor] == -1) {
            distance[neighbor] = distance[vertex] + 1;
            queue.push(neighbor);
        }
    }
    return {farthestVertex, distance[farthestVertex]};
}

int treeDiameter(const std::vector<std::vector<int>>& tree) {
    if (tree.empty()) return 0;
    const int endpoint = farthest(tree, 0).first;
    return farthest(tree, endpoint).second;
}
```

### Python

```python
from collections import deque


def farthest(tree: list[list[int]], start: int) -> tuple[int, int]:
    distance = [-1] * len(tree)
    distance[start] = 0
    queue = deque([start])
    farthest_vertex = start
    while queue:
        vertex = queue.popleft()
        if distance[vertex] > distance[farthest_vertex]:
            farthest_vertex = vertex
        for neighbor in tree[vertex]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[vertex] + 1
                queue.append(neighbor)
    return farthest_vertex, distance[farthest_vertex]


def tree_diameter(tree: list[list[int]]) -> int:
    if not tree:
        return 0
    endpoint, _ = farthest(tree, 0)
    return farthest(tree, endpoint)[1]
```

### Java

```java
static int[] farthest(List<List<Integer>> tree, int start) {
    int[] distance = new int[tree.size()];
    Arrays.fill(distance, -1);
    Queue<Integer> queue = new ArrayDeque<>();
    distance[start] = 0;
    queue.add(start);
    int farthestVertex = start;
    while (!queue.isEmpty()) {
        int vertex = queue.remove();
        if (distance[vertex] > distance[farthestVertex]) farthestVertex = vertex;
        for (int neighbor : tree.get(vertex)) {
            if (distance[neighbor] == -1) {
                distance[neighbor] = distance[vertex] + 1;
                queue.add(neighbor);
            }
        }
    }
    return new int[] {farthestVertex, distance[farthestVertex]};
}

static int treeDiameter(List<List<Integer>> tree) {
    if (tree.isEmpty()) return 0;
    int endpoint = farthest(tree, 0)[0];
    return farthest(tree, endpoint)[1];
}
```

## Why it works

A farthest vertex from any start is an endpoint of some diameter. Starting
there, the farthest reachable vertex is the opposite endpoint.

## Complexity

Time is `O(V)` and space is `O(V)`.

## Common mistakes

- Applying the rule to a graph with cycles.
- Counting vertices when the problem asks for edges, or the reverse.
- Using ordinary BFS for weighted trees; use DFS with accumulated weights.
