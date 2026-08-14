# ICPC300 002: CSES - Range Queries and Copies

**Source:** [CSES - Range Queries and Copies](https://cses.fi/problemset/task/1737/)  
**Pattern:** persistent segment tree  
**Goal:** Process point assignments, range-sum queries, and independent array
copies.

The implementations below use zero-based version numbers and array indices.
An operation is `(1, version, index, value)`, `(2, version, left, right)`, or
`(3, version)`.

## 1. First principles

A copied version must keep its old values even after either copy is updated.
Copying all `n` values is correct but expensive.

A segment-tree point update touches only one root-to-leaf path. Make those
`O(log n)` nodes new and reuse every untouched node. A copy then needs only
another reference to the same immutable root.

```text
version 0 root ---- old left subtree ---- ...
             \
              old right subtree

update one value in version 0

version 0 root' --- new nodes on one path
version 1 root  ---- old nodes remain unchanged
```

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Update after a copy | Only the selected version changes. |
| Copy after several updates | The new version starts from the selected version's current root. |
| One-element range | Return that element. |
| Full range | Return the root sum. |
| Negative values | Sums and assignments still work. |

## 3. Brute force: materialize every version

Store each version as a full list. This is the simplest oracle for testing.

```python
def range_queries_and_copies_brute(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    versions = [values.copy()]
    answers: list[int] = []

    for operation in operations:
        if not operation:
            raise ValueError("operation must not be empty")

        operation_type = operation[0]
        if operation_type == 1:
            _, version, index, value = operation
            versions[version][index] = value
        elif operation_type == 2:
            _, version, left, right = operation
            answers.append(sum(versions[version][left : right + 1]))
        elif operation_type == 3:
            _, version = operation
            versions.append(versions[version].copy())
        else:
            raise ValueError(f"unknown operation type: {operation_type}")

    return answers
```

**Why it works:** each list is an independent version, so mutations cannot
leak across copies.

**Complexity:** update `O(1)`, query `O(n)`, copy `O(n)`, and `O(nv)` memory
for `v` versions.

## 4. Better: one Fenwick tree per materialized version

A Fenwick tree reduces updates and sums to `O(log n)`. Copying still duplicates
the value list and tree, so this remains too slow when there are many copies.

```python
class FenwickVersion:
    def __init__(self, values: list[int]) -> None:
        self.values = values.copy()
        self.tree = [0] * (len(values) + 1)
        for index, value in enumerate(values, start=1):
            self.tree[index] += value
            parent = index + (index & -index)
            if parent < len(self.tree):
                self.tree[parent] += self.tree[index]

    def copy(self) -> "FenwickVersion":
        copied = FenwickVersion([])
        copied.values = self.values.copy()
        copied.tree = self.tree.copy()
        return copied

    def assign(self, index: int, value: int) -> None:
        difference = value - self.values[index]
        self.values[index] = value
        tree_index = index + 1
        while tree_index < len(self.tree):
            self.tree[tree_index] += difference
            tree_index += tree_index & -tree_index

    def prefix_sum(self, end: int) -> int:
        total = 0
        while end > 0:
            total += self.tree[end]
            end -= end & -end
        return total

    def range_sum(self, left: int, right: int) -> int:
        return self.prefix_sum(right + 1) - self.prefix_sum(left)


def range_queries_and_copies_fenwick(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    versions = [FenwickVersion(values)]
    answers: list[int] = []

    for operation in operations:
        if not operation:
            raise ValueError("operation must not be empty")

        operation_type = operation[0]
        if operation_type == 1:
            _, version, index, value = operation
            versions[version].assign(index, value)
        elif operation_type == 2:
            _, version, left, right = operation
            answers.append(versions[version].range_sum(left, right))
        elif operation_type == 3:
            _, version = operation
            versions.append(versions[version].copy())
        else:
            raise ValueError(f"unknown operation type: {operation_type}")

    return answers
```

**Complexity:** update/query `O(log n)`, copy `O(n)`, and `O(nv)` memory.

## 5. Expert solution: persistent segment tree

Every node is immutable after construction. `assign` returns a new root and
shares the untouched child at every level. Operation 3 therefore appends a
root reference in `O(1)`.

```python
from __future__ import annotations


class SegmentNode:
    __slots__ = ("total", "left", "right")

    def __init__(
        self,
        total: int,
        left: SegmentNode | None = None,
        right: SegmentNode | None = None,
    ) -> None:
        self.total = total
        self.left = left
        self.right = right


def range_queries_and_copies_persistent(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    def build(low: int, high: int) -> SegmentNode:
        if low == high:
            return SegmentNode(values[low])
        middle = (low + high) // 2
        left = build(low, middle)
        right = build(middle + 1, high)
        return SegmentNode(left.total + right.total, left, right)

    def assign(
        node: SegmentNode, low: int, high: int, index: int, value: int
    ) -> SegmentNode:
        if low == high:
            return SegmentNode(value)

        left = node.left
        right = node.right
        if left is None or right is None:
            raise RuntimeError("internal segment node must have two children")

        middle = (low + high) // 2
        if index <= middle:
            left = assign(left, low, middle, index, value)
        else:
            right = assign(right, middle + 1, high, index, value)
        return SegmentNode(left.total + right.total, left, right)

    def range_sum(
        node: SegmentNode,
        low: int,
        high: int,
        query_left: int,
        query_right: int,
    ) -> int:
        if query_left <= low and high <= query_right:
            return node.total

        left = node.left
        right = node.right
        if left is None or right is None:
            raise RuntimeError("internal segment node must have two children")

        middle = (low + high) // 2
        total = 0
        if query_left <= middle:
            total += range_sum(left, low, middle, query_left, query_right)
        if query_right > middle:
            total += range_sum(right, middle + 1, high, query_left, query_right)
        return total

    last_index = len(values) - 1
    roots = [build(0, last_index)]
    answers: list[int] = []

    for operation in operations:
        if not operation:
            raise ValueError("operation must not be empty")

        operation_type = operation[0]
        if operation_type == 1:
            _, version, index, value = operation
            roots[version] = assign(roots[version], 0, last_index, index, value)
        elif operation_type == 2:
            _, version, left, right = operation
            answers.append(range_sum(roots[version], 0, last_index, left, right))
        elif operation_type == 3:
            _, version = operation
            roots.append(roots[version])
        else:
            raise ValueError(f"unknown operation type: {operation_type}")

    return answers
```

### Why the expert code is correct

- A leaf stores its version's value; every internal node stores the sum of its
  two children.
- An assignment rebuilds exactly the nodes whose sums changed and shares every
  other immutable subtree.
- Each root therefore describes one complete version, and sharing a root
  cannot allow later mutations because nodes are never modified.

**Complexity:** build `O(n)`, update/query `O(log n)`, copy `O(1)`. Memory is
`O(n + u log n + v)` for `u` updates and `v` versions.

## 6. What to remember

```text
copy full array       -> O(n) per copy
copy immutable root   -> O(1) per copy
point assignment      -> copy one root-to-leaf path
range sum             -> ordinary segment-tree query
```
