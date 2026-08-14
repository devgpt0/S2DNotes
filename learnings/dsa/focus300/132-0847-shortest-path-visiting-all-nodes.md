# Focus300 132: LeetCode 847 - Shortest Path Visiting All Nodes

**Source:** [LeetCode 847](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)  
**Difficulty:** Hard  
**Pattern:** multi-source BFS over `(node, visited_mask)` states

## Exact contract

Given a connected undirected graph with `1 <= n <= 12`, return the minimum
number of edges in a walk that visits every node. The walk may start and end at
any nodes and may revisit nodes and edges.

## First principles

The future depends on the current node and the set of nodes already visited.
Those form an unweighted state graph. Starting BFS simultaneously from every
single-node mask represents the freedom to choose any start without adding a
synthetic edge.

## Cases that decide correctness

- One node requires zero edges.
- Revisiting a hub can be necessary.
- Reaching the same node with a different visited mask is a different state.
- The first full-mask state dequeued has minimum walk length.
- The input graph must be symmetric, connected, and contain valid node IDs.

## Brute force: enumerate walks without global state merging

```python
from collections import deque


def shortest_covering_walk_brute(graph: list[list[int]]) -> int:
    if (
        type(graph) is not list
        or not 1 <= len(graph) <= 12
        or any(
            type(neighbors) is not list
            or any(type(node) is not int for node in neighbors)
            for neighbors in graph
        )
    ):
        raise TypeError("graph must be a list of integer adjacency lists")
    node_count = len(graph)
    if any(
        neighbor == node
        or not 0 <= neighbor < node_count
        or graph[node].count(neighbor) != 1
        or node not in graph[neighbor]
        for node, neighbors in enumerate(graph)
        for neighbor in neighbors
    ):
        raise ValueError("graph must be a simple undirected graph")
    reachable = {0}
    stack = [0]
    while stack:
        for neighbor in graph[stack.pop()]:
            if neighbor not in reachable:
                reachable.add(neighbor)
                stack.append(neighbor)
    if len(reachable) != node_count:
        raise ValueError("graph must be connected")

    complete = (1 << node_count) - 1
    queue = deque((node, 1 << node, 0) for node in range(node_count))
    while queue:
        node, visited, distance = queue.popleft()
        if visited == complete:
            return distance
        for neighbor in graph[node]:
            queue.append((neighbor, visited | (1 << neighbor), distance + 1))
    raise RuntimeError("a connected graph must have a covering walk")
```

Without merging equal states, the number of generated walks grows
exponentially with the answer length.

## Better approach: subset DP after all-pairs shortest paths

Compute shortest distances between graph nodes, then run traveling-salesperson
DP over subsets and endpoints. That takes `O(2^n n^2)` time. Direct BFS visits
the same essential state space but uses only actual graph edges.

## Expert solution: merge identical node-and-mask states

```python
from collections import deque


def shortest_covering_walk(graph: list[list[int]]) -> int:
    if (
        type(graph) is not list
        or not 1 <= len(graph) <= 12
        or any(
            type(neighbors) is not list
            or any(type(node) is not int for node in neighbors)
            for neighbors in graph
        )
    ):
        raise TypeError("graph must be a list of integer adjacency lists")
    node_count = len(graph)
    if any(
        neighbor == node
        or not 0 <= neighbor < node_count
        or graph[node].count(neighbor) != 1
        or node not in graph[neighbor]
        for node, neighbors in enumerate(graph)
        for neighbor in neighbors
    ):
        raise ValueError("graph must be a simple undirected graph")
    reachable = {0}
    stack = [0]
    while stack:
        for neighbor in graph[stack.pop()]:
            if neighbor not in reachable:
                reachable.add(neighbor)
                stack.append(neighbor)
    if len(reachable) != node_count:
        raise ValueError("graph must be connected")

    complete = (1 << node_count) - 1
    queue = deque((node, 1 << node, 0) for node in range(node_count))
    seen = {(node, 1 << node) for node in range(node_count)}
    while queue:
        node, visited, distance = queue.popleft()
        if visited == complete:
            return distance
        for neighbor in graph[node]:
            next_visited = visited | (1 << neighbor)
            state = (neighbor, next_visited)
            if state not in seen:
                seen.add(state)
                queue.append((neighbor, next_visited, distance + 1))
    raise RuntimeError("a connected graph must have a covering walk")
```

BFS reaches each `(node, mask)` with its shortest distance. Later arrivals at
that identical state cannot improve any continuation and are safely discarded.

**Complexity:** `O(2^n (n + m))` time and `O(2^n n)` space.
