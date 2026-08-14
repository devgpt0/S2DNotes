# ICPC300 038: CSES - Reversals and Sums

**Source:** [CSES - Reversals and Sums](https://cses.fi/problemset/task/2074/)  
**Pattern:** implicit treap with lazy reversal and subtree sums

## Exact contract

Input gives array length `n`, query count `q`
(`1 <= n, q <= 200000`), the array, and queries `type a b`:

- type `1`: reverse the current subarray from `a` through `b`;
- type `2`: output the sum of that current subarray.

Indices are one-based and both endpoints are inclusive.

## First principles

An implicit treap locates an element by subtree sizes rather than an explicit
key. Two splits isolate any range as one subtree. Its stored sum answers type
`2` immediately.

For type `1`, reversing every node now would be linear. Instead, swap the
range root's children and toggle a lazy flag. Before descending through a node,
`push` applies that pending reversal to its children. Subtree sum is unchanged
by order, so no sum recomputation is needed solely for the reversal.

## Cases that decide correctness

- A one-element reversal changes nothing but remains valid.
- Multiple pending reversals cancel because the flag is toggled with XOR.
- `split` and `merge` must call `push` before deciding by child sizes.
- Sums may exceed 32-bit range.
- After answering a sum query, merge all three pieces back in the same order.

## Brute force: use Python list slices

```python
def reversals_and_sums_brute(
    values: list[int],
    queries: list[tuple[int, int, int]],
) -> list[int]:
    values = values.copy()
    answers = []
    for query_type, left, right in queries:
        start = left - 1
        if query_type == 1:
            values[start:right] = reversed(values[start:right])
        else:
            answers.append(sum(values[start:right]))
    return answers
```

**Complexity:** `O(nq)` worst-case time and `O(n)` space.

## Better for sum-heavy inputs: Fenwick tree with explicit swaps

```python
class FenwickTree:
    def __init__(self, values: list[int]) -> None:
        self.tree = [0] * (len(values) + 1)
        for index, value in enumerate(values, start=1):
            self.add(index, value)

    def add(self, index: int, difference: int) -> None:
        while index < len(self.tree):
            self.tree[index] += difference
            index += index & -index

    def prefix_sum(self, end: int) -> int:
        total = 0
        while end > 0:
            total += self.tree[end]
            end -= end & -end
        return total


def reversals_and_sums_fenwick(
    values: list[int],
    queries: list[tuple[int, int, int]],
) -> list[int]:
    values = values.copy()
    fenwick = FenwickTree(values)
    answers = []

    for query_type, left, right in queries:
        if query_type == 2:
            answers.append(fenwick.prefix_sum(right) - fenwick.prefix_sum(left - 1))
            continue

        low = left - 1
        high = right - 1
        while low < high:
            low_value = values[low]
            high_value = values[high]
            values[low], values[high] = high_value, low_value
            fenwick.add(low + 1, high_value - low_value)
            fenwick.add(high + 1, low_value - high_value)
            low += 1
            high -= 1

    return answers
```

Range sums become `O(log n)`. Reversal still costs `O(length log n)`, so this
is a genuine improvement only when sum queries dominate and reversed ranges
are short; it does not meet the general worst case.

## Expert solution: lazy implicit treap

```python
import sys


class Node:
    __slots__ = (
        "value",
        "priority",
        "size",
        "total",
        "reversed",
        "left",
        "right",
    )

    def __init__(self, value: int, priority: int) -> None:
        self.value = value
        self.priority = priority
        self.size = 1
        self.total = value
        self.reversed = False
        self.left: Node | None = None
        self.right: Node | None = None


def node_size(node: Node | None) -> int:
    return 0 if node is None else node.size


def node_sum(node: Node | None) -> int:
    return 0 if node is None else node.total


def update(node: Node) -> None:
    node.size = 1 + node_size(node.left) + node_size(node.right)
    node.total = node.value + node_sum(node.left) + node_sum(node.right)


def apply_reverse(node: Node | None) -> None:
    if node is not None:
        node.left, node.right = node.right, node.left
        node.reversed = not node.reversed


def push(node: Node) -> None:
    if node.reversed:
        apply_reverse(node.left)
        apply_reverse(node.right)
        node.reversed = False


def split(root: Node | None, left_size: int) -> tuple[Node | None, Node | None]:
    if root is None:
        return None, None
    push(root)
    if node_size(root.left) >= left_size:
        left, root.left = split(root.left, left_size)
        update(root)
        return left, root
    root.right, right = split(
        root.right,
        left_size - node_size(root.left) - 1,
    )
    update(root)
    return root, right


def merge(left: Node | None, right: Node | None) -> Node | None:
    if left is None:
        return right
    if right is None:
        return left
    if left.priority > right.priority:
        push(left)
        left.right = merge(left.right, right)
        update(left)
        return left
    push(right)
    right.left = merge(left, right.left)
    update(right)
    return right


def solve() -> None:
    sys.setrecursionlimit(1_000_000)
    data = list(map(int, sys.stdin.buffer.read().split()))
    value_count, query_count = data[0:2]
    values = data[2 : 2 + value_count]
    offset = 2 + value_count
    priority_state = 0x9E3779B97F4A7C15

    def next_priority() -> int:
        nonlocal priority_state
        priority_state ^= priority_state >> 12
        priority_state ^= priority_state << 25
        priority_state ^= priority_state >> 27
        priority_state &= (1 << 64) - 1
        return priority_state * 0x2545F4914F6CDD1D & ((1 << 64) - 1)

    root: Node | None = None
    for value in values:
        root = merge(root, Node(value, next_priority()))

    answers: list[str] = []
    for _ in range(query_count):
        query_type, left_position, right_position = data[offset : offset + 3]
        offset += 3
        left, remainder = split(root, left_position - 1)
        middle, right = split(remainder, right_position - left_position + 1)

        if query_type == 1:
            apply_reverse(middle)
        else:
            answers.append(str(node_sum(middle)))
        root = merge(left, merge(middle, right))

    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

The isolated middle subtree contains exactly the queried positions. Its
aggregate is therefore the required sum, while its lazy child swap represents
the exact reversed order for all later splits and merges.

**Complexity:** `O((n+q) log n)` expected time and `O(n)` space.

