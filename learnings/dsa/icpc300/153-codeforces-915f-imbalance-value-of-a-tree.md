# ICPC300 153: Codeforces 915F - Imbalance Value of a Tree

**Source:** [Codeforces 915F - Imbalance Value of a Tree](https://codeforces.com/problemset/problem/915/F)  
**Rating:** 2300  
**Pattern:** offline DSU contributions in value order  
**Goal:** For every unordered pair of tree vertices, take the maximum value on
their path minus the minimum value on that path; return the sum over all pairs.

## 1. First principles

Split every path's imbalance into its maximum contribution minus its minimum
contribution. Activate vertices from low value to high value. When a vertex of
value `x` joins active neighbor components of sizes `a` and `b`, exactly `a*b`
new endpoint pairs become connected, and every such path has maximum `x`.

Reverse the order to count path minima in the same way, then subtract them.

## 2. Cases that decide correctness

- A one-vertex path contributes zero and need not be counted.
- Equal values may be activated in any order because their contribution value
  is identical.
- Negative vertex values are valid.
- Each unordered endpoint pair becomes connected exactly once in each pass.
- The edges must form one tree.

## 3. Brute force: find each endpoint path separately

```python
def tree_imbalance_brute(values: list[int], edges: list[tuple[int, int]]) -> int:
    if not values or len(edges) != len(values) - 1:
        raise ValueError("edges must describe a tree")
    graph = [[] for _ in values]
    for first, second in edges:
        if not 0 <= first < len(values) or not 0 <= second < len(values):
            raise ValueError("edge endpoint out of range")
        graph[first].append(second)
        graph[second].append(first)

    answer = 0
    for start in range(len(values)):
        for target in range(start + 1, len(values)):
            stack = [(start, -1, values[start], values[start])]
            while stack:
                node, parent, minimum, maximum = stack.pop()
                if node == target:
                    answer += maximum - minimum
                    break
                for neighbor in graph[node]:
                    if neighbor != parent:
                        stack.append(
                            (
                                neighbor,
                                node,
                                min(minimum, values[neighbor]),
                                max(maximum, values[neighbor]),
                            )
                        )
            else:
                raise ValueError("edges must form a connected tree")
    return answer
```

**Complexity:** `O(V^3)` time and `O(V+E)` space.

## 4. Better: one traversal per start vertex

```python
def tree_imbalance_all_starts(values: list[int], edges: list[tuple[int, int]]) -> int:
    if not values or len(edges) != len(values) - 1:
        raise ValueError("edges must describe a tree")
    graph = [[] for _ in values]
    for first, second in edges:
        if not 0 <= first < len(values) or not 0 <= second < len(values):
            raise ValueError("edge endpoint out of range")
        graph[first].append(second)
        graph[second].append(first)

    answer = 0
    for start in range(len(values)):
        visited = 0
        stack = [(start, -1, values[start], values[start])]
        while stack:
            node, parent, minimum, maximum = stack.pop()
            visited += 1
            if node > start:
                answer += maximum - minimum
            for neighbor in graph[node]:
                if neighbor != parent:
                    stack.append(
                        (
                            neighbor,
                            node,
                            min(minimum, values[neighbor]),
                            max(maximum, values[neighbor]),
                        )
                    )
        if visited != len(values):
            raise ValueError("edges must form a connected tree")
    return answer
```

**Complexity:** `O(V^2)` time and `O(V+E)` space.

## 5. Expert solution: ascending and descending DSU sweeps

```python
def tree_imbalance_dsu(values: list[int], edges: list[tuple[int, int]]) -> int:
    if not values or len(edges) != len(values) - 1:
        raise ValueError("edges must describe a tree")
    graph = [[] for _ in values]
    for first, second in edges:
        if not 0 <= first < len(values) or not 0 <= second < len(values):
            raise ValueError("edge endpoint out of range")
        graph[first].append(second)
        graph[second].append(first)

    def path_extreme_sum(order: list[int]) -> int:
        parent = list(range(len(values)))
        sizes = [1] * len(values)
        active = [False] * len(values)

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        total = 0
        for node in order:
            active[node] = True
            for neighbor in graph[node]:
                if not active[neighbor]:
                    continue
                first_root = find(node)
                second_root = find(neighbor)
                if first_root == second_root:
                    continue
                total += values[node] * sizes[first_root] * sizes[second_root]
                if sizes[first_root] < sizes[second_root]:
                    first_root, second_root = second_root, first_root
                parent[second_root] = first_root
                sizes[first_root] += sizes[second_root]
        root = find(0)
        if any(find(node) != root for node in range(len(values))):
            raise ValueError("edges must form a connected tree")
        return total

    ascending = sorted(range(len(values)), key=values.__getitem__)
    descending = sorted(range(len(values)), key=values.__getitem__, reverse=True)
    maximum_sum = path_extreme_sum(ascending)
    minimum_sum = path_extreme_sum(descending)
    return maximum_sum - minimum_sum
```

### Why the expert code is correct

In the ascending sweep, active paths contain only values at most the current
one. A union creates precisely the paths whose final missing highest vertex has
just activated, so the current value is their maximum. The descending sweep is
the identical argument for minima. Their difference is the requested sum.

**Complexity:** `O(V log V + E alpha(V))` time and `O(V+E)` space.

## 6. What to remember

```text
path imbalance = path maximum - path minimum
activate by value -> newly connected pairs share that extreme
new pairs across components -> size_left * size_right
```
