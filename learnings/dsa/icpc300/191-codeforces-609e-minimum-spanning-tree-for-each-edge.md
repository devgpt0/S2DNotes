# ICPC300 191: Codeforces 609E - Minimum spanning tree for each edge

**Source:** [Codeforces 609E - Minimum spanning tree for each edge](https://codeforces.com/problemset/problem/609/E)  
**Rating:** 2300  
**Pattern:** Kruskal MST plus binary-lifting path maxima  
**Goal:** For every weighted edge, return the minimum spanning-tree weight
among spanning trees forced to contain that edge.

## 1. First principles

Build one MST of weight `mst_weight`. For a non-tree edge `(u, v, w)`, adding
it creates one cycle. To keep a spanning tree while minimizing weight, remove
the heaviest edge on the MST path from `u` to `v`:

```text
forced_weight = mst_weight + w - maximum_edge_on_path(u, v)
```

Binary lifting stores both the `2^k` ancestor and the maximum edge on that
jump, so each path maximum takes logarithmic time.

## 2. Cases that decide correctness

- An edge already chosen by Kruskal returns the original MST weight.
- Parallel edges are distinct answers and may have equal endpoints.
- Equal-weight MST choices do not change the formula's minimum weight.
- Negative edge weights are valid; path maxima must not start at zero.
- The input graph must be connected.

## 3. Brute force: force each edge and rerun Kruskal

```python
def forced_mst_weights_brute(
    vertex_count: int, edges: list[tuple[int, int, int]]
) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    for first, second, _ in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")

    order = sorted(range(len(edges)), key=lambda index: edges[index][2])
    answers: list[int] = []
    for forced in range(len(edges)):
        parent = list(range(vertex_count))
        sizes = [1] * vertex_count

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        def union(first: int, second: int) -> bool:
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                return False
            if sizes[first_root] < sizes[second_root]:
                first_root, second_root = second_root, first_root
            parent[second_root] = first_root
            sizes[first_root] += sizes[second_root]
            return True

        first, second, weight = edges[forced]
        union(first, second)
        total = weight
        chosen = 1
        for edge_index in order:
            if edge_index == forced:
                continue
            first, second, weight = edges[edge_index]
            if union(first, second):
                total += weight
                chosen += 1
        if chosen != vertex_count - 1:
            raise ValueError("graph must be connected")
        answers.append(total)
    if vertex_count > 1 and not edges:
        raise ValueError("graph must be connected")
    return answers
```

**Complexity:** `O(E^2 alpha(V) + E log E)` time and `O(V+E)` space.

## 4. Better transition: replace the worst cycle edge

The cut and cycle properties reduce every forced-edge problem to one query on
one fixed MST. A parent table alone finds ancestors; augmenting every jump with
its maximum edge answers the required replacement cost at the same time.

## 5. Expert solution: Kruskal plus maximum-edge LCA

```python
def forced_mst_weights(
    vertex_count: int, edges: list[tuple[int, int, int]]
) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    for first, second, _ in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")

    parent = list(range(vertex_count))
    sizes = [1] * vertex_count

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(first: int, second: int) -> bool:
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            return False
        if sizes[first_root] < sizes[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        sizes[first_root] += sizes[second_root]
        return True

    tree = [[] for _ in range(vertex_count)]
    in_tree = [False] * len(edges)
    mst_weight = 0
    chosen = 0
    for edge_index in sorted(range(len(edges)), key=lambda index: edges[index][2]):
        first, second, weight = edges[edge_index]
        if not union(first, second):
            continue
        in_tree[edge_index] = True
        mst_weight += weight
        chosen += 1
        tree[first].append((second, weight))
        tree[second].append((first, weight))
    if chosen != vertex_count - 1:
        raise ValueError("graph must be connected")

    levels = max(1, vertex_count.bit_length())
    ancestors = [[0] * vertex_count for _ in range(levels)]
    maxima = [[-(10**30)] * vertex_count for _ in range(levels)]
    depth = [0] * vertex_count
    visited = [False] * vertex_count
    visited[0] = True
    stack = [0]
    while stack:
        node = stack.pop()
        for neighbor, weight in tree[node]:
            if visited[neighbor]:
                continue
            visited[neighbor] = True
            depth[neighbor] = depth[node] + 1
            ancestors[0][neighbor] = node
            maxima[0][neighbor] = weight
            stack.append(neighbor)
    for level in range(1, levels):
        for node in range(vertex_count):
            middle = ancestors[level - 1][node]
            ancestors[level][node] = ancestors[level - 1][middle]
            maxima[level][node] = max(
                maxima[level - 1][node],
                maxima[level - 1][middle],
            )

    def path_maximum(first: int, second: int) -> int:
        answer = -(10**30)
        if depth[first] < depth[second]:
            first, second = second, first
        difference = depth[first] - depth[second]
        for level in range(levels):
            if difference >> level & 1:
                answer = max(answer, maxima[level][first])
                first = ancestors[level][first]
        if first == second:
            return answer
        for level in range(levels - 1, -1, -1):
            if ancestors[level][first] != ancestors[level][second]:
                answer = max(
                    answer,
                    maxima[level][first],
                    maxima[level][second],
                )
                first = ancestors[level][first]
                second = ancestors[level][second]
        return max(answer, maxima[0][first], maxima[0][second])

    answers: list[int] = []
    for edge_index, (first, second, weight) in enumerate(edges):
        if in_tree[edge_index]:
            answers.append(mst_weight)
        else:
            answers.append(mst_weight + weight - path_maximum(first, second))
    return answers
```

### Why the expert code is correct

Kruskal produces an MST. Forcing a non-tree edge creates exactly one cycle;
every resulting spanning tree must remove an edge from that cycle, and removing
its maximum-weight MST edge is optimal. Binary lifting returns that exact
maximum. Tree edges already satisfy the force condition in the original MST.

**Complexity:** `O((V+E) log V + E log E)` time and `O(V log V + E)` space.

## 6. What to remember

```text
force non-tree edge -> create one MST cycle
best repair -> remove maximum edge on that path
many path maxima -> binary lifting with aggregated weights
```
