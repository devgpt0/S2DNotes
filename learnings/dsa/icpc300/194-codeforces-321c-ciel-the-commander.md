# ICPC300 194: Codeforces 321C - Ciel the Commander

**Source:** [Codeforces 321C - Ciel the Commander](https://codeforces.com/problemset/problem/321/C)  
**Rating:** 2200  
**Pattern:** centroid decomposition with hierarchy labels  
**Goal:** Label tree vertices `A`, `B`, ... so the path between two vertices
with the same label contains a vertex with a smaller label. Return `None` if
more than 26 levels are required.

## 1. First principles

Choose a centroid and label it at the current level. Removing it splits the
component into parts of at most half the size; recursively label every part at
the next level.

Two equal-level vertices lie either in one recursive part, where induction
handles them, or in different parts, where their path crosses the earlier
centroid. Halving keeps the number of levels logarithmic.

## 2. Cases that decide correctness

- A one-vertex component labels its only vertex immediately.
- Trees with two centroids may choose either; the code chooses the smaller ID.
- Each recursive component excludes all previously chosen centroids.
- Level zero maps to `A`; level 25 maps to `Z`.
- The input must be one connected acyclic tree.

## 3. Brute force: test every vertex as a centroid

```python
def commander_labels_brute(
    vertex_count: int, edges: list[tuple[int, int]]
) -> list[str] | None:
    if vertex_count <= 0 or len(edges) != vertex_count - 1:
        raise ValueError("edges must describe a tree")
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    parent = [-1] * vertex_count
    parent[0] = 0
    stack = [0]
    visited = 0
    while stack:
        node = stack.pop()
        visited += 1
        for neighbor in graph[node]:
            if neighbor == parent[node]:
                continue
            if parent[neighbor] != -1:
                raise ValueError("edges must be acyclic")
            parent[neighbor] = node
            stack.append(neighbor)
    if visited != vertex_count:
        raise ValueError("edges must be connected")

    label = [-1] * vertex_count

    def decompose(component: set[int], level: int) -> bool:
        if level >= 26:
            return False
        centroid = -1
        for candidate in sorted(component):
            remaining = component - {candidate}
            seen: set[int] = set()
            largest = 0
            for start in sorted(remaining):
                if start in seen:
                    continue
                size = 0
                search = [start]
                seen.add(start)
                while search:
                    node = search.pop()
                    size += 1
                    for neighbor in graph[node]:
                        if neighbor in remaining and neighbor not in seen:
                            seen.add(neighbor)
                            search.append(neighbor)
                largest = max(largest, size)
            if 2 * largest <= len(component):
                centroid = candidate
                break
        if centroid == -1:
            raise RuntimeError("tree component has no centroid")

        label[centroid] = level
        remaining = component - {centroid}
        seen: set[int] = set()
        for start in sorted(remaining):
            if start in seen:
                continue
            part: set[int] = set()
            search = [start]
            seen.add(start)
            while search:
                node = search.pop()
                part.add(node)
                for neighbor in graph[node]:
                    if neighbor in remaining and neighbor not in seen:
                        seen.add(neighbor)
                        search.append(neighbor)
            if not decompose(part, level + 1):
                return False
        return True

    if not decompose(set(range(vertex_count)), 0):
        return None
    return [chr(ord("A") + level) for level in label]
```

**Complexity:** `O(n^2)` time and `O(n)` space.

## 4. Better transition: compute all split sizes together

Testing each candidate repeats component traversals. One rooted traversal gives
every subtree size, so each candidate's largest remaining piece is available in
constant time. Repeating that linear work per centroid level is logarithmic.

## 5. Expert solution: linear work per decomposition level

```python
def commander_labels(
    vertex_count: int, edges: list[tuple[int, int]]
) -> list[str] | None:
    if vertex_count <= 0 or len(edges) != vertex_count - 1:
        raise ValueError("edges must describe a tree")
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    parent_check = [-1] * vertex_count
    parent_check[0] = 0
    stack = [0]
    visited = 0
    while stack:
        node = stack.pop()
        visited += 1
        for neighbor in graph[node]:
            if neighbor == parent_check[node]:
                continue
            if parent_check[neighbor] != -1:
                raise ValueError("edges must be acyclic")
            parent_check[neighbor] = node
            stack.append(neighbor)
    if visited != vertex_count:
        raise ValueError("edges must be connected")

    blocked = [False] * vertex_count
    label = [-1] * vertex_count

    def decompose(entry: int, level: int) -> bool:
        if level >= 26:
            return False
        component: list[int] = []
        parent = {entry: -1}
        stack = [entry]
        while stack:
            node = stack.pop()
            component.append(node)
            for neighbor in graph[node]:
                if blocked[neighbor] or neighbor == parent[node]:
                    continue
                parent[neighbor] = node
                stack.append(neighbor)

        sizes = {node: 1 for node in component}
        for node in reversed(component):
            if parent[node] != -1:
                sizes[parent[node]] += sizes[node]

        component_size = len(component)
        centroids: list[int] = []
        for node in component:
            largest = component_size - sizes[node]
            for neighbor in graph[node]:
                if not blocked[neighbor] and parent.get(neighbor) == node:
                    largest = max(largest, sizes[neighbor])
            if 2 * largest <= component_size:
                centroids.append(node)
        centroid = min(centroids)
        blocked[centroid] = True
        label[centroid] = level
        for neighbor in graph[centroid]:
            if not blocked[neighbor] and not decompose(neighbor, level + 1):
                return False
        return True

    if not decompose(0, 0):
        return None
    return [chr(ord("A") + level) for level in label]
```

### Why the expert code is correct

The selected vertex is a true centroid because no remaining piece exceeds half
the component. Any path joining separate recursive pieces crosses this earlier
centroid; paths inside one piece satisfy the same invariant recursively.
Centroid halving bounds the hierarchy depth, and blocked vertices ensure every
vertex receives exactly one label.

**Complexity:** `O(n log n)` time and `O(n)` space.

## 6. What to remember

```text
centroid -> balanced separator
separator hierarchy -> path between equal ranks crosses an earlier rank
component halves -> logarithmic label depth
```
