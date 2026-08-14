# ICPC300 037: CSES - Cut and Paste

**Source:** [CSES - Cut and Paste](https://cses.fi/problemset/task/2072/)  
**Pattern:** implicit treap sequence editing

## Exact contract

Input gives string length `n`, operation count `m`
(`1 <= n, m <= 200000`), a lowercase string of length `n`, and `m` ranges
`a b`. For each operation, cut out the current substring from one-based
positions `a` through `b` and append it to the end. Output the final string.

## First principles

The string is a sequence, so a node's position can be implicit: its index is
the size of its left subtree. A treap maintains both binary-search-tree order
by this implicit index and heap order by a fixed priority.

`split(root, k)` separates the first `k` characters from the rest in expected
`O(log n)` time. Two splits isolate `[a, b]`. If they produce `left`, `middle`,
and `right`, the operation is exactly `left + right + middle`, implemented by
treap merges without copying characters.

## Cases that decide correctness

- Positions refer to the current string after all earlier operations.
- Cutting the entire string leaves it unchanged.
- Cutting a suffix and appending it also leaves the order unchanged.
- Both endpoints are inclusive, so the isolated length is `b - a + 1`.
- Output traversal is iterative to avoid recursion depth proportional to `n`.

## Brute force: rebuild the immutable string

```python
def cut_and_paste_brute(text: str, operations: list[tuple[int, int]]) -> str:
    for left, right in operations:
        start = left - 1
        text = text[:start] + text[right:] + text[start:right]
    return text
```

Each operation copies up to the whole string.

**Complexity:** `O(nm)` time and `O(n)` temporary space per operation.

## Better: square-root block rebuilding

```python
from math import isqrt


def cut_and_paste_blocks(text: str, operations: list[tuple[int, int]]) -> str:
    block_size = isqrt(len(text) + len(operations)) + 1
    blocks = [
        text[start : start + block_size] for start in range(0, len(text), block_size)
    ]

    def split_at(position: int) -> int:
        consumed = 0
        for block_index, block in enumerate(blocks):
            next_consumed = consumed + len(block)
            if position == consumed:
                return block_index
            if position < next_consumed:
                offset = position - consumed
                blocks[block_index : block_index + 1] = [block[:offset], block[offset:]]
                return block_index + 1
            consumed = next_consumed
        return len(blocks)

    for operation_index, (left, right) in enumerate(operations, start=1):
        start_index = split_at(left - 1)
        end_index = split_at(right)
        middle = blocks[start_index:end_index]
        del blocks[start_index:end_index]
        blocks.extend(middle)

        if operation_index % block_size == 0:
            current = "".join(blocks)
            blocks = [
                current[start : start + block_size]
                for start in range(0, len(current), block_size)
            ]

    return "".join(blocks)
```

Only block descriptors move during most operations. Periodic rebuilding keeps
the number of fragments `O(n/B + B)`, giving roughly `O((n+m) sqrt(n+m))`
total work rather than copying all `n` characters every time.

## Expert solution: implicit treap splits and merges

```python
import sys


class Node:
    __slots__ = ("character", "priority", "size", "left", "right")

    def __init__(self, character: str, priority: int) -> None:
        self.character = character
        self.priority = priority
        self.size = 1
        self.left: Node | None = None
        self.right: Node | None = None


def node_size(node: Node | None) -> int:
    return 0 if node is None else node.size


def update(node: Node) -> None:
    node.size = 1 + node_size(node.left) + node_size(node.right)


def split(root: Node | None, left_size: int) -> tuple[Node | None, Node | None]:
    if root is None:
        return None, None
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
        left.right = merge(left.right, right)
        update(left)
        return left
    right.left = merge(left, right.left)
    update(right)
    return right


def solve() -> None:
    sys.setrecursionlimit(1_000_000)
    input_stream = sys.stdin.buffer
    _, operation_count = map(int, input_stream.readline().split())
    text = input_stream.readline().strip().decode()
    priority_state = 0x9E3779B97F4A7C15

    def next_priority() -> int:
        nonlocal priority_state
        priority_state ^= priority_state >> 12
        priority_state ^= priority_state << 25
        priority_state ^= priority_state >> 27
        priority_state &= (1 << 64) - 1
        return priority_state * 0x2545F4914F6CDD1D & ((1 << 64) - 1)

    root: Node | None = None
    for character in text:
        root = merge(root, Node(character, next_priority()))

    for _ in range(operation_count):
        left_position, right_position = map(int, input_stream.readline().split())
        left, remainder = split(root, left_position - 1)
        middle, right = split(remainder, right_position - left_position + 1)
        root = merge(merge(left, right), middle)

    characters: list[str] = []
    stack: list[Node] = []
    current = root
    while current is not None or stack:
        while current is not None:
            stack.append(current)
            current = current.left
        current = stack.pop()
        characters.append(current.character)
        current = current.right
    print("".join(characters))


if __name__ == "__main__":
    solve()
```

Split preserves sequence order on both sides, and merge preserves every
character from its left argument before every character from its right. Thus
the two splits and two merges implement the required sequence equation exactly.

**Complexity:** `O((n+m) log n)` expected time and `O(n)` space.

