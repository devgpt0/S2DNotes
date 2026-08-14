# ICPC300 111: CSES - Dynamic Connectivity

**Source:** [CSES - Dynamic Connectivity](https://cses.fi/problemset/task/2133/)  
**Pattern:** segment tree over time + rollback DSU  
**Goal:** Track the number of connected components while undirected edges are
added and removed.

Operations are `(1, u, v)` additions and `(2, u, v)` removals. The returned
list contains the initial component count and the count after every operation.
Edges are simple; adding an active edge or removing an inactive edge fails.

## 1. First principles

Ordinary DSU cannot undo a deletion. Offline, each edge instead has one or more
active time intervals. Add the edge to a segment tree covering those times.

During a segment-tree DFS, a rollback DSU contains exactly the edges active for
the current time. Save a history length before entering a node and undo back to
it after leaving.

## 2. Cases that decide correctness

- Initial edges begin at time `0`.
- A removed edge is inactive in the state after that removal.
- An added edge is active in the state after that addition.
- Edges still active at the end close at the final state.
- Failed unions must not corrupt rollback history.

## 3. Brute force: rebuild reachability after every event

```python
def dynamic_connectivity_brute(
    vertex_count: int,
    initial_edges: list[tuple[int, int]],
    operations: list[tuple[int, int, int]],
) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    def edge(first: int, second: int) -> tuple[int, int]:
        if first == second:
            raise ValueError("self-loops are not supported")
        return (first, second) if first < second else (second, first)

    active = {edge(first, second) for first, second in initial_edges}
    if len(active) != len(initial_edges):
        raise ValueError("initial edges must be unique")

    def component_count() -> int:
        graph = [[] for _ in range(vertex_count)]
        for first, second in active:
            graph[first].append(second)
            graph[second].append(first)
        seen = [False] * vertex_count
        components = 0
        for start in range(vertex_count):
            if seen[start]:
                continue
            components += 1
            seen[start] = True
            stack = [start]
            while stack:
                node = stack.pop()
                for neighbor in graph[node]:
                    if not seen[neighbor]:
                        seen[neighbor] = True
                        stack.append(neighbor)
        return components

    answers = [component_count()]
    for operation_type, first, second in operations:
        normalized = edge(first, second)
        if operation_type == 1:
            if normalized in active:
                raise ValueError("cannot add an active edge")
            active.add(normalized)
        elif operation_type == 2:
            if normalized not in active:
                raise ValueError("cannot remove an inactive edge")
            active.remove(normalized)
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
        answers.append(component_count())
    return answers
```

**Complexity:** `O((q+1)(V+E+q))` worst-case time and `O(V+E+q)` space.

## 4. Better: rebuild a DSU after every event

```python
def dynamic_connectivity_rebuild_dsu(
    vertex_count: int,
    initial_edges: list[tuple[int, int]],
    operations: list[tuple[int, int, int]],
) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    def edge(first: int, second: int) -> tuple[int, int]:
        if first == second:
            raise ValueError("self-loops are not supported")
        return (first, second) if first < second else (second, first)

    active = {edge(first, second) for first, second in initial_edges}
    if len(active) != len(initial_edges):
        raise ValueError("initial edges must be unique")

    def component_count() -> int:
        parent = list(range(vertex_count))
        size = [1] * vertex_count

        def find(vertex: int) -> int:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        components = vertex_count
        for first, second in active:
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                continue
            if size[first_root] < size[second_root]:
                first_root, second_root = second_root, first_root
            parent[second_root] = first_root
            size[first_root] += size[second_root]
            components -= 1
        return components

    answers = [component_count()]
    for operation_type, first, second in operations:
        normalized = edge(first, second)
        if operation_type == 1:
            if normalized in active:
                raise ValueError("cannot add an active edge")
            active.add(normalized)
        elif operation_type == 2:
            if normalized not in active:
                raise ValueError("cannot remove an inactive edge")
            active.remove(normalized)
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
        answers.append(component_count())
    return answers
```

**Complexity:** `O((q+1)(V+E+q) alpha(V))` time and `O(V+E+q)` space.

## 5. Expert solution: time intervals and rollback DSU

```python
def dynamic_connectivity_rollback(
    vertex_count: int,
    initial_edges: list[tuple[int, int]],
    operations: list[tuple[int, int, int]],
) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    def edge(first: int, second: int) -> tuple[int, int]:
        if first == second:
            raise ValueError("self-loops are not supported")
        return (first, second) if first < second else (second, first)

    active_since = {edge(first, second): 0 for first, second in initial_edges}
    if len(active_since) != len(initial_edges):
        raise ValueError("initial edges must be unique")

    state_count = len(operations) + 1
    intervals: list[tuple[int, int, tuple[int, int]]] = []
    for time, (operation_type, first, second) in enumerate(operations, start=1):
        normalized = edge(first, second)
        if operation_type == 1:
            if normalized in active_since:
                raise ValueError("cannot add an active edge")
            active_since[normalized] = time
        elif operation_type == 2:
            start = active_since.pop(normalized, None)
            if start is None:
                raise ValueError("cannot remove an inactive edge")
            intervals.append((start, time - 1, normalized))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    for normalized, start in active_since.items():
        intervals.append((start, state_count - 1, normalized))

    timeline: list[list[tuple[int, int]]] = [[] for _ in range(4 * state_count)]

    def add_interval(
        node: int,
        low: int,
        high: int,
        left: int,
        right: int,
        normalized: tuple[int, int],
    ) -> None:
        if left <= low and high <= right:
            timeline[node].append(normalized)
            return
        middle = (low + high) // 2
        if left <= middle:
            add_interval(2 * node, low, middle, left, right, normalized)
        if right > middle:
            add_interval(2 * node + 1, middle + 1, high, left, right, normalized)

    for left, right, normalized in intervals:
        if left <= right:
            add_interval(1, 0, state_count - 1, left, right, normalized)

    parent = list(range(vertex_count))
    size = [1] * vertex_count
    history: list[tuple[int, int]] = []
    components = vertex_count

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            vertex = parent[vertex]
        return vertex

    def unite(first: int, second: int) -> None:
        nonlocal components
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            return
        if size[first_root] < size[second_root]:
            first_root, second_root = second_root, first_root
        history.append((second_root, size[first_root]))
        parent[second_root] = first_root
        size[first_root] += size[second_root]
        components -= 1

    def rollback(snapshot: int) -> None:
        nonlocal components
        while len(history) > snapshot:
            child, old_parent_size = history.pop()
            root = parent[child]
            size[root] = old_parent_size
            parent[child] = child
            components += 1

    answers = [0] * state_count

    def solve(node: int, low: int, high: int) -> None:
        snapshot = len(history)
        for first, second in timeline[node]:
            unite(first, second)
        if low == high:
            answers[low] = components
        else:
            middle = (low + high) // 2
            solve(2 * node, low, middle)
            solve(2 * node + 1, middle + 1, high)
        rollback(snapshot)

    solve(1, 0, state_count - 1)
    return answers
```

### Why the expert code is correct

Each time leaf inherits exactly the edges whose active intervals contain that
time. Rollback restores the DSU state at every recursion boundary, so sibling
time ranges cannot leak unions into each other.

**Complexity:** `O((E+q) log q log V)` time and `O((E+q) log q + V)` space.

## 6. What to remember

```text
edge deletion offline -> active interval
active interval -> segment tree over time
DFS time tree -> apply unions, answer leaf, rollback
```
