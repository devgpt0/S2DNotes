# ICPC300 184: Codeforces 1093G - Multidimensional Queries

**Source:** [Codeforces 1093G](https://codeforces.com/problemset/problem/1093/G)  
**Pattern:** sign-mask projections in a segment tree

## Exact contract

Maintain `n` points with `k <= 5` coordinates. Type `1 i x1 ... xk` replaces
point `i`. Type `2 l r` asks for the maximum Manhattan distance between any two
points whose indices lie in `[l,r]`.

## First principles

For points `p` and `q`,

`distance(p,q) = max_s dot(s,p-q)`,

where every coordinate sign in `s` is `+1` or `-1`. For one range and sign
mask, the best ordered pair is its maximum projection minus its minimum. The
minimum for a mask is the negated maximum for the complementary mask, so store
only maxima for all `2^k` masks.

## Cases that decide correctness

- A one-point range has answer zero.
- Coordinates and projections may be negative.
- Point replacement changes every sign projection.
- Both endpoints must belong to the queried index range.
- Complementing all signs negates a projection.

## Brute force: compare every point pair

```python
def multidimensional_queries_brute(
    points: list[list[int]], operations: list[tuple[int, ...]]
) -> list[int]:
    current = [point.copy() for point in points]
    answers = []
    for operation in operations:
        if operation[0] == 1:
            current[operation[1] - 1] = list(operation[2:])
            continue
        _, left, right = operation
        answer = 0
        for first in range(left - 1, right):
            for second in range(first + 1, right):
                answer = max(
                    answer,
                    sum(
                        abs(a - b)
                        for a, b in zip(current[first], current[second], strict=True)
                    ),
                )
        answers.append(answer)
    return answers
```

This takes `O(k * range_length^2)` per query.

## Better insight: project before pairing

For one sign mask, independent range extrema replace all pair comparisons.
The segment tree maintains those extrema under point changes.

## Expert solution: one maximum tree per sign mask

```python
import sys
from array import array


def solve() -> None:
    input_stream = sys.stdin.buffer
    point_count, dimension_count = map(int, input_stream.readline().split())
    points = [
        list(map(int, input_stream.readline().split())) for _ in range(point_count)
    ]
    mask_count = 1 << dimension_count
    all_signs = mask_count - 1
    base = 1
    while base < point_count:
        base *= 2
    negative_infinity = -(10**18)
    trees = [array("q", [negative_infinity]) * (2 * base) for _ in range(mask_count)]

    def projection(point: list[int], mask: int) -> int:
        return sum(
            coordinate if mask >> dimension & 1 else -coordinate
            for dimension, coordinate in enumerate(point)
        )

    for index, point in enumerate(points):
        for mask, tree in enumerate(trees):
            tree[base + index] = projection(point, mask)
    for tree in trees:
        for node in range(base - 1, 0, -1):
            tree[node] = max(tree[node * 2], tree[node * 2 + 1])

    def update(position: int, point: list[int]) -> None:
        for mask, tree in enumerate(trees):
            node = base + position
            tree[node] = projection(point, mask)
            node //= 2
            while node:
                tree[node] = max(tree[node * 2], tree[node * 2 + 1])
                node //= 2

    def range_maximum(tree: array, left: int, right: int) -> int:
        left += base
        right += base
        answer = negative_infinity
        while left < right:
            if left & 1:
                answer = max(answer, tree[left])
                left += 1
            if right & 1:
                right -= 1
                answer = max(answer, tree[right])
            left //= 2
            right //= 2
        return answer

    query_count = int(input_stream.readline())
    output = []
    for _ in range(query_count):
        operation = list(map(int, input_stream.readline().split()))
        if operation[0] == 1:
            update(operation[1] - 1, operation[2:])
            continue
        _, left, right = operation
        maxima = [range_maximum(tree, left - 1, right) for tree in trees]
        output.append(
            str(
                max(
                    maxima[mask] + maxima[all_signs ^ mask]
                    for mask in range(mask_count)
                )
            )
        )
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

For each sign choice, the two complementary maxima equal maximum minus minimum
projection. Taking the best choice is exactly Manhattan distance.

**Complexity:** `O(2^k log n)` per operation, `O(2^k n)` time to build, and
`O(2^k n)` compact integer storage.
