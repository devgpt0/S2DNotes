# ICPC300 222: Codeforces 949C - Data Center Maintenance

**Source:** [Codeforces 949C - Data Center Maintenance](https://codeforces.com/problemset/problem/949/C)  
**Rating:** 2200  
**Pattern:** implication graph, strongly connected components, minimum sink SCC  
**Goal:** Choose the smallest nonempty server set closed under maintenance
dependencies induced by connected servers and cyclic schedule times.

## 1. First principles

For a connection `(u, v)` and schedule modulus `h`, add dependency `u -> v`
when `(time[u] + 1) % h == time[v]`; add `v -> u` under the symmetric
condition. A valid chosen set has no dependency leaving it.

Contract strongly connected components. Any closed nonempty set contains a
sink component, and one sink component is itself closed. Therefore the minimum
answer is the smallest sink SCC.

## 2. Cases that decide correctness

- With modulus two, one connection may create dependencies in both directions.
- Vertices in one SCC cannot be separated by a closed choice.
- Only outgoing condensation edges matter for sink status.
- Isolated vertices are one-vertex sink components.
- Ties may return any minimum sink; the code chooses lexicographically.

## 3. Brute force: enumerate every nonempty closed subset

```python
def maintenance_set_brute(
    times: list[int], modulus: int, edges: list[tuple[int, int]]
) -> list[int]:
    if not times or modulus <= 0 or any(not 0 <= time < modulus for time in times):
        raise ValueError("invalid schedule")
    dependencies: list[tuple[int, int]] = []
    for first, second in edges:
        if (
            not 0 <= first < len(times)
            or not 0 <= second < len(times)
            or first == second
        ):
            raise ValueError("invalid edge")
        if (times[first] + 1) % modulus == times[second]:
            dependencies.append((first, second))
        if (times[second] + 1) % modulus == times[first]:
            dependencies.append((second, first))

    answer: list[int] | None = None
    for mask in range(1, 1 << len(times)):
        if any(
            mask >> first & 1 and mask >> second & 1 == 0
            for first, second in dependencies
        ):
            continue
        chosen = [vertex for vertex in range(len(times)) if mask >> vertex & 1]
        if answer is None or (len(chosen), chosen) < (len(answer), answer):
            answer = chosen
    if answer is None:
        raise RuntimeError("no nonempty subset")
    return answer
```

**Complexity:** `O(2^V (V+E))` time and `O(E)` space.

## 4. Better transition: contract inseparable dependency cycles

Mutually reachable servers must be chosen together. SCC contraction turns the
dependency graph into a DAG, where the smallest closed nonempty choice is
immediately one of its sinks.

## 5. Expert solution: Kosaraju and minimum sink component

```python
def maintenance_set(
    times: list[int], modulus: int, edges: list[tuple[int, int]]
) -> list[int]:
    if not times or modulus <= 0 or any(not 0 <= time < modulus for time in times):
        raise ValueError("invalid schedule")
    graph = [[] for _ in times]
    reverse = [[] for _ in times]
    for first, second in edges:
        if (
            not 0 <= first < len(times)
            or not 0 <= second < len(times)
            or first == second
        ):
            raise ValueError("invalid edge")
        if (times[first] + 1) % modulus == times[second]:
            graph[first].append(second)
            reverse[second].append(first)
        if (times[second] + 1) % modulus == times[first]:
            graph[second].append(first)
            reverse[first].append(second)

    visited = [False] * len(times)
    order: list[int] = []
    for start in range(len(times)):
        if visited[start]:
            continue
        visited[start] = True
        stack = [(start, 0)]
        while stack:
            node, next_index = stack[-1]
            if next_index < len(graph[node]):
                neighbor = graph[node][next_index]
                stack[-1] = (node, next_index + 1)
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append((neighbor, 0))
            else:
                order.append(node)
                stack.pop()

    component = [-1] * len(times)
    components: list[list[int]] = []
    for start in reversed(order):
        if component[start] != -1:
            continue
        component_index = len(components)
        members: list[int] = []
        component[start] = component_index
        stack = [start]
        while stack:
            node = stack.pop()
            members.append(node)
            for neighbor in reverse[node]:
                if component[neighbor] == -1:
                    component[neighbor] = component_index
                    stack.append(neighbor)
        components.append(sorted(members))

    has_outgoing = [False] * len(components)
    for node in range(len(times)):
        for neighbor in graph[node]:
            if component[node] != component[neighbor]:
                has_outgoing[component[node]] = True
    return min(
        (
            members
            for index, members in enumerate(components)
            if not has_outgoing[index]
        ),
        key=lambda members: (len(members), members),
    )
```

### Why the expert code is correct

SCCs are precisely the inseparable dependency groups. The condensation is a
DAG. Every closed nonempty union contains at least one sink SCC, while a sink
SCC alone has no dependency leaving it and is valid. Choosing the smallest sink
therefore minimizes the number of maintained servers.

**Complexity:** `O(V+E)` time and `O(V+E)` space.

## 6. What to remember

```text
schedule relation -> directed dependency
mutual dependency -> one SCC
smallest nonempty closed set -> smallest sink SCC
```
