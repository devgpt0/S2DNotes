# ICPC300 240: Codeforces 1709E - XOR Tree

**Source:** [Codeforces 1709E - XOR Tree](https://codeforces.com/problemset/problem/1709/E)  
**Difficulty:** 2300  
**Pattern:** small-to-large prefix-XOR sets with greedy cuts

## Exact contract

Every tree vertex has a nonnegative value. Delete the minimum number of
vertices so every path contained in a remaining component has nonzero XOR,
including one-vertex paths.

## First principles

Root the tree and define inclusive prefix XOR
`prefix[v] = prefix[parent] ^ value[v]`. For endpoints in different child
subtrees of `v`, their path XOR is
`prefix[first] ^ prefix[second] ^ value[v]`. It is zero exactly when the two
prefix values XOR to `value[v]`.

Merge child prefix sets. If such a pair appears at `v`, every solution must cut
this combined component; deleting `v` resolves all conflicts through it, so
greedily delete `v` and propagate an empty set.

## Cases that decide correctness

- A zero-valued vertex creates a zero one-vertex path.
- A deleted child disconnects its descendants, so its set does not propagate.
- Conflicts already internal to a child were resolved in that child's postorder.
- Cross-child lookup happens before merging the smaller set.
- Iterative rooting avoids recursion depth failure.

## Brute force: enumerate deleted vertex subsets

```python
def xor_tree_brute(values: list[int], edges: list[tuple[int, int]]) -> int:
    size = len(values)
    if size == 0 or any(type(value) is not int or value < 0 for value in values):
        raise ValueError("values must be nonnegative integers")
    if len(edges) != size - 1:
        raise ValueError("edges must describe a tree")
    graph = [[] for _ in range(size)]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    for deleted_count in range(size + 1):
        for deleted in range(1 << size):
            if deleted.bit_count() != deleted_count:
                continue
            valid = True
            for start in range(size):
                if deleted >> start & 1:
                    continue
                stack = [(start, -1, values[start])]
                while stack and valid:
                    vertex, parent, path_xor = stack.pop()
                    if path_xor == 0:
                        valid = False
                        break
                    for neighbor in graph[vertex]:
                        if neighbor != parent and not deleted >> neighbor & 1:
                            stack.append(
                                (neighbor, vertex, path_xor ^ values[neighbor])
                            )
                if not valid:
                    break
            if valid:
                return deleted_count
    raise RuntimeError("deleting every vertex is always valid")
```

This takes `O(2^n n^2)` time.

## Better approach: merge prefix sets without size ordering

The same postorder greedy is correct with ordinary set merging, but a path tree
can repeatedly copy a linear-size set. Always keeping the largest child set
gives the small-to-large bound.

## Expert solution: greedy conflict cuts and sack merging

```python
def minimum_xor_tree_deletions(values: list[int], edges: list[tuple[int, int]]) -> int:
    size = len(values)
    if size == 0 or any(type(value) is not int or value < 0 for value in values):
        raise ValueError("values must be nonnegative integers")
    if len(edges) != size - 1:
        raise ValueError("edges must describe a tree")
    graph = [[] for _ in range(size)]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    parent = [-2] * size
    parent[0] = -1
    prefix = [0] * size
    prefix[0] = values[0]
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("graph must be a tree")
            parent[neighbor] = vertex
            prefix[neighbor] = prefix[vertex] ^ values[neighbor]
            order.append(neighbor)
    if len(order) != size:
        raise ValueError("graph must be connected")

    children = [[] for _ in range(size)]
    for vertex in range(1, size):
        children[parent[vertex]].append(vertex)

    bags: list[set[int] | None] = [None] * size
    answer = 0
    for vertex in reversed(order):
        heavy = max(
            children[vertex],
            key=lambda child: len(bags[child] or set()),
            default=-1,
        )
        if heavy == -1:
            bag: set[int] = set()
        else:
            heavy_bag = bags[heavy]
            if heavy_bag is None:
                raise RuntimeError("missing child prefix set")
            bag = heavy_bag

        conflict = values[vertex] == 0 or (prefix[vertex] ^ values[vertex]) in bag
        bag.add(prefix[vertex])
        for child in children[vertex]:
            child_bag = bags[child]
            if child_bag is None:
                raise RuntimeError("missing child prefix set")
            if child != heavy and not conflict:
                if any((item ^ values[vertex]) in bag for item in child_bag):
                    conflict = True
                else:
                    bag.update(child_bag)
            bags[child] = None

        if conflict:
            answer += 1
            bags[vertex] = set()
        else:
            bags[vertex] = bag
    return answer
```

At the first unresolved zero-XOR path whose highest vertex is `v`, one deletion
inside that combined component is unavoidable; deleting `v` resolves every
such path at once. Small-to-large merging preserves the same conflict test.

**Complexity:** `O(n log n)` expected time and `O(n)` live set entries.
