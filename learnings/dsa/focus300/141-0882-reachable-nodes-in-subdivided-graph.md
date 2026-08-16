# Focus300 141: LeetCode 882 - Reachable Nodes In Subdivided Graph

**Source:** [LeetCode 882](https://leetcode.com/problems/reachable-nodes-in-subdivided-graph/)  
**Difficulty:** Hard  
**Pattern:** shortest paths with compressed edge interiors

## Exact contract

Nodes `0` through `n - 1` form an undirected graph. Edge `[u, v, count]` is
replaced by a chain containing `count` new nodes, so crossing it costs
`count + 1` moves. Starting at node `0`, return the number of original and new
nodes reachable in at most `max_moves` moves.

## First principles

Run Dijkstra only on original nodes with edge weight `count + 1`. If endpoint
`u` is reachable with distance `d`, it reaches `max_moves - d` interior nodes
from its side. For one edge, add the two endpoint contributions but cap their
sum at the edge's actual number of new nodes.


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

- Starting node `0` is reachable even when `max_moves = 0`.
- An original endpoint beyond the move budget contributes no interior reach.
- Interior nodes approached from both ends are counted once by the edge cap.
- Crossing an edge requires `count + 1`, not `count`, moves.
- Edges are undirected, but each edge's new nodes are added once.

## Brute force: build every subdivided node

```python
from collections import deque


def reachable_nodes_brute(
    edges: list[list[int]],
    max_moves: int,
    node_count: int,
) -> int:
    if node_count <= 0 or max_moves < 0:
        raise ValueError("node_count must be positive and max_moves non-negative")
    if any(
        len(edge) != 3
        or not 0 <= edge[0] < node_count
        or not 0 <= edge[1] < node_count
        or edge[0] == edge[1]
        or edge[2] < 0
        for edge in edges
    ):
        raise ValueError("each edge must contain two distinct nodes and a count")

    adjacency: list[list[int]] = [[] for _ in range(node_count)]
    next_node = node_count
    for start, end, subdivisions in edges:
        previous = start
        for _ in range(subdivisions):
            adjacency.append([])
            adjacency[previous].append(next_node)
            adjacency[next_node].append(previous)
            previous = next_node
            next_node += 1
        adjacency[previous].append(end)
        adjacency[end].append(previous)

    distance = [-1] * len(adjacency)
    distance[0] = 0
    queue = deque([0])
    while queue:
        node = queue.popleft()
        if distance[node] == max_moves:
            continue
        for neighbor in adjacency[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return sum(value != -1 for value in distance)
```

This is exact but requires `O(n + sum(count))` memory and time, which the source
counts make impractical.

## Better transition: retain each chain as one weighted edge

Only distances to original endpoints affect how much of an edge can be entered.
Compressing a chain to weight `count + 1` preserves those distances exactly.

## Expert solution: Dijkstra plus per-edge reach

```python
import heapq


def reachable_nodes(
    edges: list[list[int]],
    max_moves: int,
    node_count: int,
) -> int:
    if node_count <= 0 or max_moves < 0:
        raise ValueError("node_count must be positive and max_moves non-negative")
    if any(
        len(edge) != 3
        or not 0 <= edge[0] < node_count
        or not 0 <= edge[1] < node_count
        or edge[0] == edge[1]
        or edge[2] < 0
        for edge in edges
    ):
        raise ValueError("each edge must contain two distinct nodes and a count")

    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(node_count)]
    for start, end, subdivisions in edges:
        weight = subdivisions + 1
        adjacency[start].append((end, weight))
        adjacency[end].append((start, weight))

    unreachable = max_moves + 1
    distance = [unreachable] * node_count
    distance[0] = 0
    heap = [(0, 0)]
    while heap:
        moves, node = heapq.heappop(heap)
        if moves != distance[node]:
            continue
        for neighbor, weight in adjacency[node]:
            candidate = moves + weight
            if candidate <= max_moves and candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))

    answer = sum(moves <= max_moves for moves in distance)
    for start, end, subdivisions in edges:
        from_start = max(0, max_moves - distance[start])
        from_end = max(0, max_moves - distance[end])
        answer += min(subdivisions, from_start + from_end)
    return answer
```

Dijkstra gives the least moves to each original endpoint. The capped sum counts
exactly the union of the two reachable prefixes inside every subdivided edge.

**Complexity:** `O((n + e) log n)` time and `O(n + e)` space.
