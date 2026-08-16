# Focus300 094: LeetCode 685 - Redundant Connection II

**Source:** [LeetCode 685](https://leetcode.com/problems/redundant-connection-ii/)  
**Difficulty:** Hard  
**Pattern:** two-parent detection plus disjoint-set cycle detection

## Exact contract

A rooted tree on nodes `1..n` had one extra directed edge added. Given the `n`
resulting edges, remove one edge so the graph is again a rooted tree. If more
than one removal works, return the valid edge appearing last in the input.

## First principles

A rooted tree gives every non-root node one parent and contains no undirected
cycle. One added edge can therefore create a node with two parents, a cycle,
or both.

If a node has two incoming edges, tentatively skip the later one. If all other
edges are acyclic, the later edge is removable. If a cycle remains, the earlier
incoming edge lies on that cycle and must be removed. With no two-parent node,
the edge that closes the cycle is the answer.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- A pure directed cycle has no node with two parents.
- With two parents but no remaining cycle, return the later incoming edge.
- With both violations, return the earlier incoming edge.
- Input order matters only when multiple removals are valid.
- Cycle detection treats each directed edge as an undirected union operation.

## Brute force: remove candidates from last to first

```python
from collections import deque


def redundant_directed_edge_brute(edges: list[list[int]]) -> list[int]:
    if type(edges) is not list or not 3 <= len(edges) <= 1_000:
        raise ValueError("edges must contain between 3 and 1,000 entries")
    node_count = len(edges)
    if any(
        type(edge) is not list
        or len(edge) != 2
        or any(type(node) is not int for node in edge)
        or not all(1 <= node <= node_count for node in edge)
        for edge in edges
    ):
        raise ValueError("every edge must contain two node labels in 1..n")
    edge_keys = [tuple(edge) for edge in edges]
    if len(edge_keys) != len(set(edge_keys)):
        raise ValueError("directed edges must be distinct")

    def forms_rooted_tree(removed_index: int) -> bool:
        indegree = [0] * (node_count + 1)
        adjacency = [[] for _ in range(node_count + 1)]
        for index, (source, target) in enumerate(edges):
            if index == removed_index:
                continue
            indegree[target] += 1
            if indegree[target] > 1:
                return False
            adjacency[source].append(target)

        roots = [node for node in range(1, node_count + 1) if indegree[node] == 0]
        if len(roots) != 1:
            return False
        queue = deque([roots[0]])
        visited = {roots[0]}
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor in visited:
                    return False
                visited.add(neighbor)
                queue.append(neighbor)
        return len(visited) == node_count

    for index in range(node_count - 1, -1, -1):
        if forms_rooted_tree(index):
            return list(edges[index])
    raise ValueError("input is not a rooted tree with one added edge")
```

This directly enforces the last-valid-edge rule in `O(n^2)` time.

## Better insight: only the two-parent node creates ambiguous candidates

Record its earlier and later incoming edges. Skipping the later edge reduces
the remaining decision to one union-find pass.

## Expert solution: candidate analysis plus union-find

```python
def redundant_directed_edge(edges: list[list[int]]) -> list[int]:
    if type(edges) is not list or not 3 <= len(edges) <= 1_000:
        raise ValueError("edges must contain between 3 and 1,000 entries")
    node_count = len(edges)
    if any(
        type(edge) is not list
        or len(edge) != 2
        or any(type(node) is not int for node in edge)
        or not all(1 <= node <= node_count for node in edge)
        for edge in edges
    ):
        raise ValueError("every edge must contain two node labels in 1..n")
    edge_keys = [tuple(edge) for edge in edges]
    if len(edge_keys) != len(set(edge_keys)):
        raise ValueError("directed edges must be distinct")

    incoming_edge = [-1] * (node_count + 1)
    earlier_index = -1
    later_index = -1
    for index, (_, target) in enumerate(edges):
        if incoming_edge[target] == -1:
            incoming_edge[target] = index
        else:
            earlier_index = incoming_edge[target]
            later_index = index
            break

    representative = list(range(node_count + 1))

    def find(node: int) -> int:
        while representative[node] != node:
            representative[node] = representative[representative[node]]
            node = representative[node]
        return node

    for index, (source, target) in enumerate(edges):
        if index == later_index:
            continue
        source_root = find(source)
        target_root = find(target)
        if source_root == target_root:
            if earlier_index != -1:
                return list(edges[earlier_index])
            return list(edges[index])
        representative[target_root] = source_root

    if later_index == -1:
        raise ValueError("input is not a rooted tree with one added edge")
    return list(edges[later_index])
```

The skipped graph either still has a cycle, proving the earlier candidate is
wrong, or is a tree, proving the later candidate is the redundant edge.

**Complexity:** `O(n * alpha(n))` time and `O(n)` space.
