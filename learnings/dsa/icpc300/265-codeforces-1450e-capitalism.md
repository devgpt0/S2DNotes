# ICPC300 265: Codeforces 1450E - Capitalism

**Source:** [Codeforces 1450E - Capitalism](https://codeforces.com/problemset/problem/1450/E)  
**Rating:** 2400  
**Pattern:** bipartite feasibility plus unweighted graph diameter  
**Goal:** Assign integer levels to a connected graph so adjacent levels differ
by exactly one. Maximize `max(level) - min(level)` and return one assignment, or
report that none exists.

## 1. First principles

An odd cycle makes alternating `+1/-1` differences impossible, so feasibility
is exactly bipartiteness.

In a bipartite graph, BFS distances from any root differ by exactly one on
every edge: they differ by at most one by the triangle inequality and cannot
have the same parity. Distances from a diameter endpoint attain the graph
diameter. No valid assignment can have a larger range because level difference
along any path is at most its length.

## 2. Cases that decide correctness

- A self-loop is immediately infeasible.
- A single vertex has range zero.
- The graph must be connected under the source contract.
- Multiple edges do not affect feasibility or distances.
- Any diameter endpoint gives an optimal assignment.

## 3. Brute force: enumerate normalized level assignments

```python
from itertools import product


def capitalism_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> tuple[int, list[int]] | None:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            if first == second and 0 <= first < vertex_count:
                return None
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in graph[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                stack.append(neighbor)
    if len(reached) != vertex_count:
        raise ValueError("graph must be connected")

    best: tuple[int, list[int]] | None = None
    for assignment in product(range(vertex_count), repeat=vertex_count):
        if min(assignment) != 0:
            continue
        if any(
            abs(assignment[first] - assignment[second]) != 1 for first, second in edges
        ):
            continue
        spread = max(assignment)
        if best is None or spread > best[0]:
            best = spread, list(assignment)
    return best
```

**Complexity:** `O(n^n (n + m))` time and `O(n + m)` space.

## 4. Better approach: test every root after a separate color DFS

One traversal can first check bipartiteness, followed by one BFS per possible
root. The expert code folds the connectivity and color check into its first
BFS but keeps the same `O(n(n+m))` bound.

## 5. Expert solution: choose the best BFS distance labeling

```python
from collections import deque


def optimal_capitalism_levels(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> tuple[int, list[int]] | None:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
        ):
            raise ValueError("invalid edge")
        if first == second:
            return None
        graph[first].append(second)
        graph[second].append(first)

    colors = [-1] * vertex_count
    colors[0] = 0
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            if colors[neighbor] == -1:
                colors[neighbor] = colors[vertex] ^ 1
                queue.append(neighbor)
            elif colors[neighbor] == colors[vertex]:
                return None
    if any(color == -1 for color in colors):
        raise ValueError("graph must be connected")

    best_spread = -1
    best_levels: list[int] = []
    for start in range(vertex_count):
        distance = [-1] * vertex_count
        distance[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        spread = max(distance)
        if spread > best_spread:
            best_spread = spread
            best_levels = distance
    return best_spread, best_levels
```

### Why the expert code is correct

Bipartiteness is necessary and sufficient. For every feasible root, BFS
distances form a valid assignment. Taking the root with maximum eccentricity
produces the graph diameter, while the path bound proves that no assignment
can have a larger level range.

**Complexity:** `O(n(n + m))` time and `O(n + m)` space.

## 6. What to remember

```text
edge difference exactly one -> bipartite graph
BFS levels in a bipartite graph -> valid assignment
maximum possible range -> graph diameter
```
