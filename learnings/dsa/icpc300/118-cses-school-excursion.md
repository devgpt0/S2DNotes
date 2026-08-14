# ICPC300 118: CSES - School Excursion

**Source:** [CSES - School Excursion](https://cses.fi/problemset/task/1706/)  
**Pattern:** connected components plus subset-sum bitset  
**Goal:** Given an undirected friendship graph, decide for every size from `1`
to `n` whether an excursion group of that size can be formed when each chosen
child's entire connected component must join.

## 1. First principles

Friendship is transitive through paths, so a connected component is
indivisible. After finding component sizes `s_1, ..., s_k`, the graph vanishes
and the problem becomes subset sum:

```text
possible <- possible OR (possible shifted left by s_i)
```

Bit `j` records whether some processed components total `j` children.

## 2. Cases that decide correctness

- An isolated child is a component of size `1`.
- Parallel friendship edges do not change a component.
- Size `0` seeds the subset sum but is not part of the returned answer.
- Size `n` is always possible by choosing every component.
- Edge endpoints outside `0..n-1` are invalid.

## 3. Brute force: enumerate component subsets

```python
def excursion_sizes_brute(
    child_count: int, friendships: list[tuple[int, int]]
) -> list[bool]:
    if child_count <= 0:
        raise ValueError("child_count must be positive")
    graph = [[] for _ in range(child_count)]
    for first, second in friendships:
        if not 0 <= first < child_count or not 0 <= second < child_count:
            raise ValueError("friendship endpoint out of range")
        graph[first].append(second)
        graph[second].append(first)

    seen = [False] * child_count
    component_sizes: list[int] = []
    for start in range(child_count):
        if seen[start]:
            continue
        seen[start] = True
        stack = [start]
        size = 0
        while stack:
            node = stack.pop()
            size += 1
            for neighbor in graph[node]:
                if not seen[neighbor]:
                    seen[neighbor] = True
                    stack.append(neighbor)
        component_sizes.append(size)

    possible = [False] * (child_count + 1)
    for mask in range(1 << len(component_sizes)):
        total = sum(
            size for index, size in enumerate(component_sizes) if mask & (1 << index)
        )
        possible[total] = True
    return possible[1:]
```

**Complexity:** `O(V+E + 2^c * c)` time and `O(V+E)` space for `c`
components.

## 4. Better: boolean subset-sum dynamic programming

```python
def excursion_sizes_dp(
    child_count: int, friendships: list[tuple[int, int]]
) -> list[bool]:
    if child_count <= 0:
        raise ValueError("child_count must be positive")
    parent = list(range(child_count))
    sizes = [1] * child_count

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for first, second in friendships:
        if not 0 <= first < child_count or not 0 <= second < child_count:
            raise ValueError("friendship endpoint out of range")
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            continue
        if sizes[first_root] < sizes[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        sizes[first_root] += sizes[second_root]

    possible = [False] * (child_count + 1)
    possible[0] = True
    for node in range(child_count):
        if find(node) != node:
            continue
        size = sizes[node]
        for total in range(child_count, size - 1, -1):
            possible[total] |= possible[total - size]
    return possible[1:]
```

**Complexity:** `O((V+E) alpha(V) + cV)` time and `O(V)` space.

## 5. Expert solution: integer subset-sum bitset

```python
def excursion_sizes_bitset(
    child_count: int, friendships: list[tuple[int, int]]
) -> list[bool]:
    if child_count <= 0:
        raise ValueError("child_count must be positive")
    parent = list(range(child_count))
    sizes = [1] * child_count

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for first, second in friendships:
        if not 0 <= first < child_count or not 0 <= second < child_count:
            raise ValueError("friendship endpoint out of range")
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            continue
        if sizes[first_root] < sizes[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        sizes[first_root] += sizes[second_root]

    possible = 1
    for node in range(child_count):
        if find(node) == node:
            possible |= possible << sizes[node]
    return [bool(possible & (1 << size)) for size in range(1, child_count + 1)]
```

### Why the expert code is correct

Initially only sum zero is reachable. Shifting by a component size represents
choosing that whole component; OR also retains every choice that omits it.
Induction over the components therefore makes bit `j` true exactly for the
feasible group sizes.

**Complexity:** `O((V+E) alpha(V) + cV / word_size)` bit work and `O(V)`
space for the disjoint-set structure and result integer.

## 6. What to remember

```text
must travel with every friend -> choose whole connected components
component sizes -> 0/1 subset sum
boolean DP -> integer shift and OR
```
