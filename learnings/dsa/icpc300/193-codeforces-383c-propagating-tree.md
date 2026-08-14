# ICPC300 193: Codeforces 383C - Propagating tree

**Source:** [Codeforces 383C - Propagating tree](https://codeforces.com/problemset/problem/383/C)  
**Rating:** 2200  
**Pattern:** Euler-tour subtree intervals plus signed Fenwick updates  
**Goal:** On a tree rooted at vertex zero, update a subtree by adding `value`
at even distance from its root and subtracting it at odd distance. Point queries
return the current vertex value.

## 1. First principles

Euler order makes every rooted subtree one interval. Normalize every update to
the parity of the global root:

```text
signed = value if depth[node] is even else -value
```

Range-add `signed` to the node's Euler interval. At query time, add the stored
delta for even-depth vertices and subtract it for odd-depth vertices. This
recreates the alternating sign relative to every update root.

## 2. Cases that decide correctness

- The updated node itself is at distance zero and receives `+value`.
- Descendants one edge lower receive the opposite sign.
- Updates affect only rooted descendants, not the whole undirected component.
- Negative initial values and update values are valid.
- The edges must form one tree rooted at vertex zero.

## 3. Brute force: visit every updated subtree

```python
def propagating_tree_brute(
    values: list[int],
    edges: list[tuple[int, int]],
    operations: list[tuple[int, int] | tuple[int, int, int]],
) -> list[int]:
    if not values or len(edges) != len(values) - 1:
        raise ValueError("edges must describe a tree")
    graph = [[] for _ in values]
    for first, second in edges:
        if (
            not 0 <= first < len(values)
            or not 0 <= second < len(values)
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    parent = [-1] * len(values)
    parent[0] = 0
    depth = [0] * len(values)
    children = [[] for _ in values]
    stack = [0]
    visited_count = 0
    while stack:
        node = stack.pop()
        visited_count += 1
        for neighbor in graph[node]:
            if neighbor == parent[node]:
                continue
            if parent[neighbor] != -1:
                raise ValueError("edges must be acyclic")
            parent[neighbor] = node
            depth[neighbor] = depth[node] + 1
            children[node].append(neighbor)
            stack.append(neighbor)
    if visited_count != len(values):
        raise ValueError("edges must be connected")

    current = values.copy()
    answers: list[int] = []
    for operation in operations:
        kind = operation[0]
        if kind == 1:
            if len(operation) != 3:
                raise ValueError("update requires a node and value")
            node, amount = operation[1:]
            if not 0 <= node < len(values):
                raise ValueError("invalid update node")
            update_stack = [node]
            while update_stack:
                descendant = update_stack.pop()
                if (depth[descendant] - depth[node]) % 2 == 0:
                    current[descendant] += amount
                else:
                    current[descendant] -= amount
                update_stack.extend(children[descendant])
        elif kind == 2:
            if len(operation) != 2:
                raise ValueError("query requires one node")
            node = operation[1]
            if not 0 <= node < len(values):
                raise ValueError("invalid query node")
            answers.append(current[node])
        else:
            raise ValueError("operation kind must be one or two")
    return answers
```

**Complexity:** `O(n + qn)` time and `O(n+q)` space.

## 4. Better transition: flatten and normalize parity

Euler flattening solves the subtree boundary. Multiplying an update and query
by the vertex's root-depth sign turns every alternating subtree update into one
ordinary interval addition.

## 5. Expert solution: Euler interval difference Fenwick tree

```python
def propagating_tree(
    values: list[int],
    edges: list[tuple[int, int]],
    operations: list[tuple[int, int] | tuple[int, int, int]],
) -> list[int]:
    if not values or len(edges) != len(values) - 1:
        raise ValueError("edges must describe a tree")
    graph = [[] for _ in values]
    for first, second in edges:
        if (
            not 0 <= first < len(values)
            or not 0 <= second < len(values)
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    parent = [-1] * len(values)
    parent[0] = 0
    depth = [0] * len(values)
    children = [[] for _ in values]
    stack = [0]
    order: list[int] = []
    while stack:
        node = stack.pop()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor == parent[node]:
                continue
            if parent[neighbor] != -1:
                raise ValueError("edges must be acyclic")
            parent[neighbor] = node
            depth[neighbor] = depth[node] + 1
            children[node].append(neighbor)
            stack.append(neighbor)
    if len(order) != len(values):
        raise ValueError("edges must be connected")

    entry = [0] * len(values)
    exit_time = [0] * len(values)
    timer = 0
    traversal = [(0, False)]
    while traversal:
        node, exiting = traversal.pop()
        if exiting:
            exit_time[node] = timer - 1
            continue
        entry[node] = timer
        timer += 1
        traversal.append((node, True))
        for child in reversed(children[node]):
            traversal.append((child, False))

    fenwick = [0] * (len(values) + 1)

    def add(index: int, amount: int) -> None:
        index += 1
        while index < len(fenwick):
            fenwick[index] += amount
            index += index & -index

    def range_add(left: int, right: int, amount: int) -> None:
        add(left, amount)
        if right + 1 < len(values):
            add(right + 1, -amount)

    def point_value(index: int) -> int:
        index += 1
        total = 0
        while index:
            total += fenwick[index]
            index -= index & -index
        return total

    answers: list[int] = []
    for operation in operations:
        kind = operation[0]
        if kind == 1:
            if len(operation) != 3:
                raise ValueError("update requires a node and value")
            node, amount = operation[1:]
            if not 0 <= node < len(values):
                raise ValueError("invalid update node")
            signed_amount = amount if depth[node] % 2 == 0 else -amount
            range_add(entry[node], exit_time[node], signed_amount)
        elif kind == 2:
            if len(operation) != 2:
                raise ValueError("query requires one node")
            node = operation[1]
            if not 0 <= node < len(values):
                raise ValueError("invalid query node")
            delta = point_value(entry[node])
            answers.append(values[node] + (delta if depth[node] % 2 == 0 else -delta))
        else:
            raise ValueError("operation kind must be one or two")
    return answers
```

### Why the expert code is correct

The Euler interval contains exactly an update root's descendants. A normalized
update has the root-depth sign; multiplying it by a queried descendant's sign
produces `+amount` for equal parity and `-amount` for opposite parity, exactly
matching even and odd tree distance. Fenwick range-add and point-query preserve
the sum of all such updates.

**Complexity:** `O((n+q) log n)` time and `O(n+q)` space.

## 6. What to remember

```text
rooted subtree -> Euler interval
alternating signs -> normalize by global depth parity
range add plus point query -> difference Fenwick tree
```
