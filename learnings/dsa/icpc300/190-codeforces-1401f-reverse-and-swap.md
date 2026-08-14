# ICPC300 190: Codeforces 1401F - Reverse and Swap

**Source:** [Codeforces 1401F](https://codeforces.com/problemset/problem/1401/F)  
**Pattern:** logical XOR permutation over a segment tree

## Exact contract

Maintain an array of length `2^n`. Type `1 x k` assigns `a[x] = k`. Type `2 k`
reverses every consecutive block of length `2^k`. Type `3 k` swaps the two
halves of every block of length `2^(k+1)`. Type `4 l r` asks for the sum on the
inclusive range `[l,r]`.

## First principles

Reversing every `2^k` block toggles the lowest `k` bits of each zero-based
index. Swapping block halves toggles bit `k`. Keep their cumulative XOR mask
instead of moving values.

The physical segment tree never changes shape. At recursion level `d`, mask bit
`d-1` says whether the logical left and right children map to the physical
right and left children. A point update can map its logical index directly by
XOR with the mask.

## Cases that decide correctness

- Operation parameters are powers, not block lengths.
- Type `2 0` changes nothing.
- All operations accumulate in one XOR mask.
- Query bounds refer to the current logical array.
- Point updates modify the currently visible logical position.

## Brute force: perform every permutation

```python
def reverse_and_swap_brute(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    current = values.copy()
    answers = []
    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, position, value = operation
            current[position - 1] = value
        elif operation_type == 2:
            block_size = 1 << operation[1]
            for start in range(0, len(current), block_size):
                current[start : start + block_size] = reversed(
                    current[start : start + block_size]
                )
        elif operation_type == 3:
            half = 1 << operation[1]
            for start in range(0, len(current), half * 2):
                current[start : start + half * 2] = (
                    current[start + half : start + half * 2]
                    + current[start : start + half]
                )
        else:
            _, left, right = operation
            answers.append(sum(current[left - 1 : right]))
    return answers
```

Reversals and swaps can each take linear time.

## Better insight: every permutation is index XOR

Both bulk operations toggle fixed index bits, so their composition is one mask.
Only tree navigation must interpret that mask.

## Expert solution: swap logical children during queries

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    exponent, query_count = map(int, input_stream.readline().split())
    size = 1 << exponent
    values = list(map(int, input_stream.readline().split()))
    tree = [0] * (2 * size)
    tree[size:] = values
    for node in range(size - 1, 0, -1):
        tree[node] = tree[node * 2] + tree[node * 2 + 1]

    xor_mask = 0

    def update(logical_position: int, value: int) -> None:
        physical_position = logical_position ^ xor_mask
        node = size + physical_position
        tree[node] = value
        node //= 2
        while node:
            tree[node] = tree[node * 2] + tree[node * 2 + 1]
            node //= 2

    def range_sum(
        node: int,
        level: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> int:
        if query_right <= left or right <= query_left:
            return 0
        if query_left <= left and right <= query_right:
            return tree[node]
        middle = (left + right) // 2
        left_node = node * 2
        right_node = node * 2 + 1
        if xor_mask >> (level - 1) & 1:
            left_node, right_node = right_node, left_node
        return range_sum(
            left_node,
            level - 1,
            left,
            middle,
            query_left,
            query_right,
        ) + range_sum(
            right_node,
            level - 1,
            middle,
            right,
            query_left,
            query_right,
        )

    output = []
    for _ in range(query_count):
        operation = list(map(int, input_stream.readline().split()))
        operation_type = operation[0]
        if operation_type == 1:
            update(operation[1] - 1, operation[2])
        elif operation_type == 2:
            xor_mask ^= (1 << operation[1]) - 1
        elif operation_type == 3:
            xor_mask ^= 1 << operation[1]
        else:
            output.append(
                str(
                    range_sum(
                        1,
                        exponent,
                        0,
                        size,
                        operation[1] - 1,
                        operation[2],
                    )
                )
            )
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

The mask maps every logical index to its unchanged physical leaf. Child swaps
apply the same mapping to arbitrary logical query intervals.

**Complexity:** `O(log n)` per point update or sum query, `O(1)` per bulk
permutation, and `O(2^n)` space.
