# ICPC300 125: Codeforces 438D - The Child and Sequence

**Source:** [Codeforces 438D](https://codeforces.com/problemset/problem/438/D)  
**Pattern:** segment tree with maximum-pruned nonlinear updates

## Exact contract

Maintain an array under `m` online operations:

- `1 l r`: output the sum of `a[l..r]`;
- `2 l r x`: replace every `a[i]` in `[l,r]` by `a[i] mod x`;
- `3 k x`: assign `a[k] = x`.

All indices are one-based and ranges are inclusive.

## First principles

Range sums compose normally, but modulo is not a lazy operation: applying it to
a segment sum loses the individual remainders. Store both sum and maximum.
When a covered node has `maximum < x`, modulo changes no element, so the entire
subtree is skipped. Otherwise descend until changed leaves and rebuild sums and
maxima.

A successful modulo strictly reduces a positive value to less than half its
old value. Thus an element can force only logarithmically many descents between
point assignments.

## Cases that decide correctness

- Skip on `maximum < x`, not on a condition involving the segment sum.
- If `x = 1`, every updated value becomes zero.
- A modulo range may partially overlap a tree node.
- Point assignment can increase the maximum and must rebuild ancestors.
- Range sums require wide integers.

## Brute force: modify every covered element

```python
def child_sequence_brute(
    initial: list[int],
    queries: list[tuple[int, ...]],
) -> list[int]:
    values = initial.copy()
    answers = []
    for query in queries:
        if query[0] == 1:
            _, left, right = query
            answers.append(sum(values[left - 1 : right]))
        elif query[0] == 2:
            _, left, right, modulus = query
            for index in range(left - 1, right):
                values[index] %= modulus
        else:
            _, index, value = query
            values[index - 1] = value
    return answers
```

One range operation can touch all `n` values.

## Better: square-root blocks with sums and maxima

```python
from math import isqrt


def child_sequence_sqrt(
    initial: list[int],
    queries: list[tuple[int, ...]],
) -> list[int]:
    values = initial.copy()
    size = len(values)
    block_size = isqrt(size) + 1
    block_count = (size + block_size - 1) // block_size
    block_sum = [0] * block_count
    block_maximum = [0] * block_count

    def rebuild(block: int) -> None:
        left = block * block_size
        right = min(size, left + block_size)
        block_sum[block] = sum(values[left:right])
        block_maximum[block] = max(values[left:right], default=0)

    for block in range(block_count):
        rebuild(block)

    answers = []
    for query in queries:
        if query[0] == 1:
            _, raw_left, raw_right = query
            left = raw_left - 1
            right = raw_right
            total = 0
            for block in range(block_count):
                block_left = block * block_size
                block_right = min(size, block_left + block_size)
                overlap_left = max(left, block_left)
                overlap_right = min(right, block_right)
                if overlap_left >= overlap_right:
                    continue
                if overlap_left == block_left and overlap_right == block_right:
                    total += block_sum[block]
                else:
                    total += sum(values[overlap_left:overlap_right])
            answers.append(total)
        elif query[0] == 2:
            _, raw_left, raw_right, modulus = query
            left = raw_left - 1
            right = raw_right
            for block in range(block_count):
                block_left = block * block_size
                block_right = min(size, block_left + block_size)
                overlap_left = max(left, block_left)
                overlap_right = min(right, block_right)
                if overlap_left >= overlap_right:
                    continue
                if (
                    overlap_left == block_left
                    and overlap_right == block_right
                    and block_maximum[block] < modulus
                ):
                    continue
                for index in range(overlap_left, overlap_right):
                    values[index] %= modulus
                rebuild(block)
        else:
            _, raw_index, value = query
            index = raw_index - 1
            values[index] = value
            rebuild(index // block_size)
    return answers
```

Whole blocks answer sums immediately and avoid harmless modulo updates, but a
hard range can still scan many elements.

## Expert solution: maximum-pruned segment tree

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size, query_count = map(int, input_stream.readline().split())
    values = list(map(int, input_stream.readline().split()))
    segment_sum = [0] * (4 * size)
    segment_maximum = [0] * (4 * size)

    def build(node: int, left: int, right: int) -> None:
        if right - left == 1:
            segment_sum[node] = values[left]
            segment_maximum[node] = values[left]
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle, right)
        segment_sum[node] = segment_sum[node * 2] + segment_sum[node * 2 + 1]
        segment_maximum[node] = max(
            segment_maximum[node * 2], segment_maximum[node * 2 + 1]
        )

    def range_sum(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> int:
        if query_right <= left or right <= query_left:
            return 0
        if query_left <= left and right <= query_right:
            return segment_sum[node]
        middle = (left + right) // 2
        return range_sum(node * 2, left, middle, query_left, query_right) + range_sum(
            node * 2 + 1, middle, right, query_left, query_right
        )

    def range_modulo(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        modulus: int,
    ) -> None:
        if (
            query_right <= left
            or right <= query_left
            or segment_maximum[node] < modulus
        ):
            return
        if right - left == 1:
            segment_sum[node] %= modulus
            segment_maximum[node] = segment_sum[node]
            return
        middle = (left + right) // 2
        range_modulo(node * 2, left, middle, query_left, query_right, modulus)
        range_modulo(node * 2 + 1, middle, right, query_left, query_right, modulus)
        segment_sum[node] = segment_sum[node * 2] + segment_sum[node * 2 + 1]
        segment_maximum[node] = max(
            segment_maximum[node * 2], segment_maximum[node * 2 + 1]
        )

    def assign(node: int, left: int, right: int, index: int, value: int) -> None:
        if right - left == 1:
            segment_sum[node] = value
            segment_maximum[node] = value
            return
        middle = (left + right) // 2
        if index < middle:
            assign(node * 2, left, middle, index, value)
        else:
            assign(node * 2 + 1, middle, right, index, value)
        segment_sum[node] = segment_sum[node * 2] + segment_sum[node * 2 + 1]
        segment_maximum[node] = max(
            segment_maximum[node * 2], segment_maximum[node * 2 + 1]
        )

    build(1, 0, size)
    answers = []
    for _ in range(query_count):
        query = list(map(int, input_stream.readline().split()))
        if query[0] == 1:
            _, left, right = query
            answers.append(str(range_sum(1, 0, size, left - 1, right)))
        elif query[0] == 2:
            _, left, right, modulus = query
            range_modulo(1, 0, size, left - 1, right, modulus)
        else:
            _, index, value = query
            assign(1, 0, size, index - 1, value)
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

Every pruned node is unchanged. Every visited leaf receives the exact modulo,
and rebuilt ancestors restore both invariants. The halving argument amortizes
all successful nonlinear updates.

**Complexity:** `O(log n)` per sum or assignment and amortized
`O(log n log A)` per affected value across modulo operations.
