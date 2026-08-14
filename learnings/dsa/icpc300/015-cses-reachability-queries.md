# ICPC300 015: CSES - Reachability Queries

**Source:** [CSES - Reachability Queries](https://cses.fi/problemset/task/2143/)  
**Pattern:** SCC condensation and DAG transitive closure with bitsets  
**Goal:** For each ordered pair `(a, b)` in a directed graph, decide whether a
directed route from `a` to `b` exists.

## 1. Problem in plain words

Reachability is directional. A cycle makes every vertex inside it mutually
reachable, while an edge between two cycles may work in only one direction.

Running a graph search for every query repeats the same work. The source is
large enough that we must share reachability information between queries.

## 2. First principles

Every vertex in one strongly connected component (SCC) has the same
reachability outside that component. Collapse SCCs. The condensation graph is
a DAG.

For a DAG component `u`, its reachable set is:

`{u} union reachable[v]` for every edge `u -> v`.

Process components in reverse topological order so every `reachable[v]` is
already known. A Python integer is a compact bitset: bit `v` records whether
component `v` is reachable, and integer `|` unions many bits at once.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| Query `(a, a)` | Reachable by a zero-edge route. |
| Same SCC | Always reachable. |
| One-way edge between SCCs | Only the forward query is true. |
| Parallel edges | They must not change the result. |
| Disconnected components | Neither direction is reachable. |

## 4. Brute force: DFS for every query

```python
def answer_reachability_brute_force(
    vertex_count: int,
    edges: list[tuple[int, int]],
    queries: list[tuple[int, int]],
) -> list[bool]:
    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    for source, destination in edges:
        graph[source].append(destination)

    answers: list[bool] = []
    for start, target in queries:
        seen = [False] * vertex_count
        seen[start] = True
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if not seen[neighbor]:
                    seen[neighbor] = True
                    stack.append(neighbor)
        answers.append(seen[target])
    return answers
```

**Complexity:** `O(q(n + m))` time and `O(n + m)` memory.

## 5. Better when queries repeat their start

Cache one DFS result per distinct query source. If there are `s` distinct
starts, this reduces the number of graph searches from `q` to `s`.

```python
def answer_reachability_cached(
    vertex_count: int,
    edges: list[tuple[int, int]],
    queries: list[tuple[int, int]],
) -> list[bool]:
    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    for source, destination in edges:
        graph[source].append(destination)

    cache: dict[int, set[int]] = {}
    answers: list[bool] = []
    for start, target in queries:
        if start not in cache:
            reachable = {start}
            stack = [start]
            while stack:
                node = stack.pop()
                for neighbor in graph[node]:
                    if neighbor not in reachable:
                        reachable.add(neighbor)
                        stack.append(neighbor)
            cache[start] = reachable
        answers.append(target in cache[start])
    return answers
```

**Complexity:** `O(s(n + m) + q)` time and up to `O(sn + m)` memory. In the
worst case every query has a different start, so this remains too slow.

## 6. Expert solution: SCC DAG plus integer bitsets

The code uses iterative Kosaraju passes to avoid recursion-depth dependence,
then computes a topological order of the deduplicated component DAG.

```python
from collections import deque


def answer_reachability(
    vertex_count: int,
    edges: list[tuple[int, int]],
    queries: list[tuple[int, int]],
) -> list[bool]:
    if vertex_count < 1:
        raise ValueError("at least one vertex is required")

    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    reverse_graph: list[list[int]] = [[] for _ in range(vertex_count)]
    for source, destination in edges:
        if not 0 <= source < vertex_count or not 0 <= destination < vertex_count:
            raise ValueError("edge endpoint is outside the graph")
        graph[source].append(destination)
        reverse_graph[destination].append(source)

    visited = [False] * vertex_count
    finish_order: list[int] = []
    for start in range(vertex_count):
        if visited[start]:
            continue
        visited[start] = True
        stack = [(start, 0)]
        while stack:
            node, edge_index = stack[-1]
            if edge_index == len(graph[node]):
                finish_order.append(node)
                stack.pop()
                continue
            neighbor = graph[node][edge_index]
            stack[-1] = (node, edge_index + 1)
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append((neighbor, 0))

    component = [-1] * vertex_count
    component_count = 0
    for start in reversed(finish_order):
        if component[start] != -1:
            continue
        component[start] = component_count
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in reverse_graph[node]:
                if component[neighbor] == -1:
                    component[neighbor] = component_count
                    stack.append(neighbor)
        component_count += 1

    dag: list[set[int]] = [set() for _ in range(component_count)]
    for source, destination in edges:
        source_component = component[source]
        destination_component = component[destination]
        if source_component != destination_component:
            dag[source_component].add(destination_component)

    indegree = [0] * component_count
    for neighbors in dag:
        for neighbor in neighbors:
            indegree[neighbor] += 1

    queue = deque(node for node in range(component_count) if indegree[node] == 0)
    topological_order: list[int] = []
    while queue:
        node = queue.popleft()
        topological_order.append(node)
        for neighbor in dag[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    reachable = [0] * component_count
    for node in reversed(topological_order):
        mask = 1 << node
        for neighbor in dag[node]:
            mask |= reachable[neighbor]
        reachable[node] = mask

    answers: list[bool] = []
    for start, target in queries:
        if not 0 <= start < vertex_count or not 0 <= target < vertex_count:
            raise ValueError("query endpoint is outside the graph")
        target_component = component[target]
        answers.append(bool(reachable[component[start]] & (1 << target_component)))
    return answers
```

### Why the expert code is correct

- SCC contraction preserves reachability between original vertices.
- The condensation graph is a DAG, so reverse topological processing sees all
  successor masks before computing a node's mask.
- The recurrence includes the node itself and every route beginning with each
  outgoing edge; these are exactly all reachable components.
- A query is true exactly when its target component's bit is set.

If `c` is the number of SCCs, the masks occupy `O(c^2)` bits. Bitset unions use
word-parallel operations, giving `O((c + e) c / w + n + m + q)` bit-operation
time, where `e` is the number of condensation edges and `w` is the machine-word
size.

## 7. What to remember

Compress mutual reachability first. On the remaining DAG, transitive closure is
the reverse-topological recurrence `reach[u] = {u} union reach[children]`.
