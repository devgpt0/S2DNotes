# Articulation Points

## Idea

An articulation point is a vertex whose removal disconnects an undirected
graph. It uses the same discovery and low-link values as bridge finding.

## Visual model

- A non-root vertex is critical when some child cannot reach an ancestor:
  `low[child] >= discovery[vertex]`.
- A DFS root is critical only when it has at least two DFS children.

## Classroom board: critical vertex

```text
A-B-C and B-D
remove B -> A, C, and D become separate
B is an articulation point
remove C -> remaining A-B-D stays connected
```

## Steps

1. Record discovery and low values during DFS.
2. After a child returns, check the non-root rule.
3. Count direct DFS children for the root rule.
4. Mark points in a boolean array to avoid duplicates.

## First-principles derivation

A non-root DFS vertex is critical when one child subtree cannot reach any
strict ancestor of that vertex. Removing the vertex then separates that
subtree.

The DFS root is special: it is critical only when it has at least two
independent DFS children.

## Classroom board: critical vertex

```text
0 - 1 - 2
    |
    3 - 4

remove 1:
0     2     3-4       -> three components

DFS from 0:
child subtrees through 2 and 3 cannot climb above vertex 1
therefore 1 is an articulation point

remove leaf 2:
remaining vertices stay connected -> not an articulation point
```

## Pattern recognition

Use it for critical servers/cities or single vertices whose failure separates
an undirected network.

## Implementation

### C++

```cpp
std::vector<int> articulationPoints(const std::vector<std::vector<int>>& graph) {
    std::vector<int> discovery(graph.size(), -1), low(graph.size());
    std::vector<bool> critical(graph.size(), false);
    int timer = 0;
    std::function<void(int, int)> dfs = [&](int vertex, int parent) {
        discovery[vertex] = low[vertex] = timer++;
        int children = 0;
        for (int neighbor : graph[vertex]) {
            if (neighbor == parent) continue;
            if (discovery[neighbor] == -1) {
                ++children;
                dfs(neighbor, vertex);
                low[vertex] = std::min(low[vertex], low[neighbor]);
                if (parent != -1 && low[neighbor] >= discovery[vertex]) critical[vertex] = true;
            } else low[vertex] = std::min(low[vertex], discovery[neighbor]);
        }
        if (parent == -1 && children >= 2) critical[vertex] = true;
    };
    for (int vertex = 0; vertex < static_cast<int>(graph.size()); ++vertex) if (discovery[vertex] == -1) dfs(vertex, -1);
    std::vector<int> answer;
    for (int vertex = 0; vertex < static_cast<int>(graph.size()); ++vertex) if (critical[vertex]) answer.push_back(vertex);
    return answer;
}
```

### Python

```python
def articulation_points(graph: list[list[int]]) -> list[int]:
    discovery = [-1] * len(graph)
    low = [0] * len(graph)
    critical = [False] * len(graph)
    timer = 0

    def dfs(vertex: int, parent: int) -> None:
        nonlocal timer
        discovery[vertex] = low[vertex] = timer
        timer += 1
        children = 0
        for neighbor in graph[vertex]:
            if neighbor == parent:
                continue
            if discovery[neighbor] == -1:
                children += 1
                dfs(neighbor, vertex)
                low[vertex] = min(low[vertex], low[neighbor])
                if parent != -1 and low[neighbor] >= discovery[vertex]:
                    critical[vertex] = True
            else:
                low[vertex] = min(low[vertex], discovery[neighbor])
        if parent == -1 and children >= 2:
            critical[vertex] = True

    for vertex in range(len(graph)):
        if discovery[vertex] == -1:
            dfs(vertex, -1)
    return [vertex for vertex, value in enumerate(critical) if value]
```

### Java

```java
static List<Integer> articulationPoints(List<List<Integer>> graph) {
    int[] discovery = new int[graph.size()];
    Arrays.fill(discovery, -1);
    int[] low = new int[graph.size()];
    boolean[] critical = new boolean[graph.size()];
    int[] timer = {0};
    for (int vertex = 0; vertex < graph.size(); vertex++) {
        if (discovery[vertex] == -1) articulationDfs(graph, vertex, -1, discovery, low, critical, timer);
    }
    List<Integer> answer = new ArrayList<>();
    for (int vertex = 0; vertex < graph.size(); vertex++) if (critical[vertex]) answer.add(vertex);
    return answer;
}

static void articulationDfs(List<List<Integer>> graph, int vertex, int parent, int[] discovery, int[] low, boolean[] critical, int[] timer) {
    discovery[vertex] = low[vertex] = timer[0]++;
    int children = 0;
    for (int neighbor : graph.get(vertex)) {
        if (neighbor == parent) continue;
        if (discovery[neighbor] == -1) {
            children++;
            articulationDfs(graph, neighbor, vertex, discovery, low, critical, timer);
            low[vertex] = Math.min(low[vertex], low[neighbor]);
            if (parent != -1 && low[neighbor] >= discovery[vertex]) critical[vertex] = true;
        } else low[vertex] = Math.min(low[vertex], discovery[neighbor]);
    }
    if (parent == -1 && children >= 2) critical[vertex] = true;
}
```

## Why it works

If a child subtree cannot reach above its parent, removing that parent isolates
the subtree. The root has no ancestor, so only multiple independent DFS child
subtrees make it critical.

## Complexity

Time and space are `O(V + E)`.

## Common mistakes

- Applying the non-root rule to the root.
- Using `>` instead of `>=`.
- Mishandling parallel edges; use edge IDs when multigraphs are allowed.
