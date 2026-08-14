# ICPC300 271: Codeforces 1004F - Sonya and Bitwise OR

**Source:** [Codeforces 1004F](https://codeforces.com/problemset/problem/1004/F)  
**Difficulty:** 2400  
**Pattern:** segment tree with compressed prefix and suffix OR values

## Exact contract

Maintain an integer array under point assignments. A range query asks how many
nonempty subarrays inside `[l,r]` have bitwise OR at least the fixed threshold
`x`.

## First principles

For one segment, store its valid-subarray count and the distinct OR values of
prefixes and suffixes, grouped with their multiplicities. Extending a prefix
or suffix can only add bits, so each list has at most one entry per bit.

When joining two nodes, all new subarrays are a suffix of the left node plus a
prefix of the right node. Their monotone OR lists count qualifying pairs with
one moving boundary.

## Cases that decide correctness

- Query ranges and subarrays are inclusive and nonempty.
- Equal adjacent OR values must merge their multiplicities.
- Crossing subarrays use every suffix-prefix multiplicity pair.
- A point assignment rebuilds every ancestor summary.
- Query fragments must be merged in their original left-to-right order.

## Brute force: recompute every queried subarray OR

```python
def sonya_bitwise_or_brute(
    values: list[int],
    threshold: int,
    operations: list[tuple[int, ...]],
) -> list[int]:
    current = values.copy()
    answers: list[int] = []
    for operation in operations:
        if operation[0] == 1:
            _, position, value = operation
            current[position] = value
            continue
        _, left, right = operation
        answer = 0
        for start in range(left, right + 1):
            bitwise_or = 0
            for finish in range(start, right + 1):
                bitwise_or |= current[finish]
                answer += bitwise_or >= threshold
        answers.append(answer)
    return answers
```

This takes `O(length^2)` time per range query.

## Better insight: a segment has few distinct prefix and suffix ORs

Every strict change adds a previously absent bit. A node therefore needs only
`O(B)` prefix and suffix groups for `B` value bits, not every boundary choice.

## Expert solution: merge compressed OR summaries

```python
from dataclasses import dataclass
import sys


@dataclass(slots=True)
class Node:
    length: int
    prefixes: list[tuple[int, int]]
    suffixes: list[tuple[int, int]]
    valid_subarrays: int


def append_group(groups: list[tuple[int, int]], value: int, count: int) -> None:
    if groups and groups[-1][0] == value:
        groups[-1] = (value, groups[-1][1] + count)
    else:
        groups.append((value, count))


def make_leaf(value: int, threshold: int) -> Node:
    return Node(1, [(value, 1)], [(value, 1)], int(value >= threshold))


def merge_nodes(left: Node, right: Node, threshold: int) -> Node:
    right_count_suffix = [0] * (len(right.prefixes) + 1)
    for index in range(len(right.prefixes) - 1, -1, -1):
        right_count_suffix[index] = (
            right_count_suffix[index + 1] + right.prefixes[index][1]
        )

    first_valid = len(right.prefixes)
    crossing = 0
    for left_value, left_count in left.suffixes:
        while (
            first_valid > 0
            and left_value | right.prefixes[first_valid - 1][0] >= threshold
        ):
            first_valid -= 1
        crossing += left_count * right_count_suffix[first_valid]

    prefixes = left.prefixes.copy()
    left_total = left.prefixes[-1][0]
    for value, count in right.prefixes:
        append_group(prefixes, left_total | value, count)

    suffixes = right.suffixes.copy()
    right_total = right.suffixes[-1][0]
    for value, count in left.suffixes:
        append_group(suffixes, right_total | value, count)

    return Node(
        left.length + right.length,
        prefixes,
        suffixes,
        left.valid_subarrays + right.valid_subarrays + crossing,
    )


def solve() -> None:
    input_stream = sys.stdin.buffer
    size, query_count, threshold = map(int, input_stream.readline().split())
    values = list(map(int, input_stream.readline().split()))
    tree: list[Node | None] = [None] * (4 * size)

    def build(node: int, left: int, right: int) -> None:
        if right - left == 1:
            tree[node] = make_leaf(values[left], threshold)
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle, right)
        left_node = tree[node * 2]
        right_node = tree[node * 2 + 1]
        if left_node is None or right_node is None:
            raise RuntimeError("segment tree child was not built")
        tree[node] = merge_nodes(left_node, right_node, threshold)

    def update(node: int, left: int, right: int, position: int, value: int) -> None:
        if right - left == 1:
            tree[node] = make_leaf(value, threshold)
            return
        middle = (left + right) // 2
        if position < middle:
            update(node * 2, left, middle, position, value)
        else:
            update(node * 2 + 1, middle, right, position, value)
        left_node = tree[node * 2]
        right_node = tree[node * 2 + 1]
        if left_node is None or right_node is None:
            raise RuntimeError("segment tree child was not built")
        tree[node] = merge_nodes(left_node, right_node, threshold)

    def query(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> Node | None:
        if query_right <= left or right <= query_left:
            return None
        if query_left <= left and right <= query_right:
            return tree[node]
        middle = (left + right) // 2
        left_result = query(node * 2, left, middle, query_left, query_right)
        right_result = query(node * 2 + 1, middle, right, query_left, query_right)
        if left_result is None:
            return right_result
        if right_result is None:
            return left_result
        return merge_nodes(left_result, right_result, threshold)

    build(1, 0, size)
    answers: list[str] = []
    for _ in range(query_count):
        operation = list(map(int, input_stream.readline().split()))
        if operation[0] == 1:
            update(1, 0, size, operation[1] - 1, operation[2])
        else:
            result = query(1, 0, size, operation[1] - 1, operation[2])
            if result is None:
                raise RuntimeError("nonempty query returned no node")
            answers.append(str(result.valid_subarrays))
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

Each node summary is exact, and every query merge partitions its subarrays
into left-only, right-only, and crossing choices.

**Complexity:** `O((n+q) B log n)` time and `O(nB)` space.
