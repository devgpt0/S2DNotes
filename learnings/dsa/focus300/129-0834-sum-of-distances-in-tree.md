# Focus300 129: LeetCode 834 - Sum of Distances in Tree

**Source:** [LeetCode 834](https://leetcode.com/problems/sum-of-distances-in-tree/)  
**Difficulty:** Hard  
**Pattern:** subtree aggregation followed by rerooting DP

## Exact contract

Given an undirected tree on nodes `0..n-1`, return an array whose entry for node
`u` is the sum of shortest-path edge counts from `u` to every node.

## First principles

Root the tree at `0`. One postorder pass computes every subtree size, while the
sum of root depths is the answer for node `0`.

Rerooting across edge `parent -> child` makes all `subtree[child]` nodes one
step closer and the other `n-subtree[child]` nodes one step farther. Therefore
`answer[child] = answer[parent] + n - 2*subtree[child]`.

## Cases that decide correctness

- A one-node tree returns `[0]`.
- Edges are undirected even though traversal assigns parents.
- The parent must be excluded when building the rooted order.
- Long chains require iterative traversal to avoid recursion limits.
- Every edge must connect valid, distinct labels and the graph must be connected.

## Brute force: BFS from every node

```python
from collections import deque


def tree_distance_sums_brute(node_count: int, edges: list[list[int]]) -> list[int]:
    if type(node_count) is not int or not 1 <= node_count <= 30_000:
        raise ValueError("node_count must be an integer between 1 and 30,000")
    if type(edges) is not list or len(edges) != node_count - 1:
        raise ValueError("a tree must contain exactly node_count - 1 edges")
    if any(
        type(edge) is not list
        or len(edge) != 2
        or type(edge[0]) is not int
        or type(edge[1]) is not int
        or edge[0] == edge[1]
        or not 0 <= edge[0] < node_count
        or not 0 <= edge[1] < node_count
        for edge in edges
    ):
        raise ValueError("every edge must join two distinct valid nodes")
    normalized = {tuple(sorted(edge)) for edge in edges}
    if len(normalized) != len(edges):
        raise ValueError("tree edges must be distinct")

    adjacency = [[] for _ in range(node_count)]
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)

    answer: list[int] = []
    for source in range(node_count):
        queue = deque([(source, 0)])
        visited = {source}
        distance_sum = 0
        while queue:
            node, distance = queue.popleft()
            distance_sum += distance
            for neighbor in adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        if len(visited) != node_count:
            raise ValueError("edges must form a connected tree")
        answer.append(distance_sum)
    return answer
```

This repeats almost all path work and costs `O(n^2)` time.

## Better insight: adjacent roots share all but one edge contribution

Compute one root answer and every subtree size, then transfer the answer across
each parent-child edge with the rerooting formula.

## Expert solution: iterative two-pass rerooting DP

```python
def tree_distance_sums(node_count: int, edges: list[list[int]]) -> list[int]:
    if type(node_count) is not int or not 1 <= node_count <= 30_000:
        raise ValueError("node_count must be an integer between 1 and 30,000")
    if type(edges) is not list or len(edges) != node_count - 1:
        raise ValueError("a tree must contain exactly node_count - 1 edges")
    if any(
        type(edge) is not list
        or len(edge) != 2
        or type(edge[0]) is not int
        or type(edge[1]) is not int
        or edge[0] == edge[1]
        or not 0 <= edge[0] < node_count
        or not 0 <= edge[1] < node_count
        for edge in edges
    ):
        raise ValueError("every edge must join two distinct valid nodes")
    normalized = {tuple(sorted(edge)) for edge in edges}
    if len(normalized) != len(edges):
        raise ValueError("tree edges must be distinct")

    adjacency = [[] for _ in range(node_count)]
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)

    parent = [-1] * node_count
    depth = [0] * node_count
    order = [0]
    for node in order:
        for neighbor in adjacency[node]:
            if neighbor == parent[node]:
                continue
            if parent[neighbor] != -1 or neighbor == 0:
                raise ValueError("edges must be acyclic")
            parent[neighbor] = node
            depth[neighbor] = depth[node] + 1
            order.append(neighbor)
    if len(order) != node_count:
        raise ValueError("edges must form a connected tree")

    subtree_size = [1] * node_count
    for node in reversed(order[1:]):
        subtree_size[parent[node]] += subtree_size[node]

    answer = [0] * node_count
    answer[0] = sum(depth)
    for node in order[1:]:
        answer[node] = answer[parent[node]] + node_count - 2 * subtree_size[node]
    return answer
```

The postorder computes subtree effects once; the preorder reroots each edge
once using the proven distance change.

**Complexity:** `O(n)` time and `O(n)` space.
