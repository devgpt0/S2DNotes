# Graph Performance in Python

## First principles

Graph performance is dominated by representation and traversal primitives.
Sparse contest graphs need adjacency lists, BFS needs `deque.popleft`, and
large adversarial depth usually needs iterative traversal.

## Why it matters

Large graphs combine many Python objects, loops, and queue/heap operations.
Representation and traversal style can decide whether a correct algorithm fits.

## Technique

Use adjacency lists and zero-based integer vertices:

```python
graph = [[] for _ in range(vertex_count)]
for first, second in edges:
    graph[first].append(second)
    graph[second].append(first)
```

Use iterative traversal for deep graphs:

```python
visited = bytearray(vertex_count)
visited[start] = 1
stack = [start]
while stack:
    vertex = stack.pop()
    for neighbor in graph[vertex]:
        if not visited[neighbor]:
            visited[neighbor] = 1
            stack.append(neighbor)
```

Weighted edges should use the smallest clear representation:

```python
weighted_graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
weighted_graph[source].append((target, weight))
```

## Pattern recognition

Before coding, decide: directed or undirected, weighted or unweighted, possible
parallel edges, connected or disconnected, and recursion depth.

## Expert habits

- Mark BFS/DFS vertices when enqueued/pushed.
- Use `bytearray` for a compact boolean visited array.
- Store edge IDs when bridges, Euler paths, or parallel edges matter.
- For tree postorder, build a parent/order list iteratively and process it in
  reverse.

## Visual worked example: store only existing edges

For `V=5` and edges `0-1, 1-2, 1-4`:

```text
adjacency matrix: 5*5 = 25 cells

adjacency list:
0: [1]
1: [0,2,4]
2: [1]
3: []
4: [1]
stored neighbor entries = 2E = 6
```

As `V` grows with few edges, `O(V+E)` storage and traversal remain practical
while `O(V^2)` does not.

## Traps

- Building an adjacency matrix for a sparse `200_000`-vertex graph.
- Forgetting the reverse undirected edge.
- Using a set for every adjacency list unless duplicate removal is required;
  sets cost more memory.
- Reinitializing an `O(V)` visited array inside every query when timestamps or
  offline processing can avoid it.
