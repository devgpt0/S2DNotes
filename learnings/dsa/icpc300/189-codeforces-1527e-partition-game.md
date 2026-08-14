# ICPC300 189: Codeforces 1527E - Partition Game

**Source:** [Codeforces 1527E](https://codeforces.com/problemset/problem/1527/E)  
**Pattern:** partition DP with range-add minimum states

## Exact contract

Partition the array into exactly `k` nonempty contiguous segments. A segment's
cost is, for every distinct value in it, the distance between that value's
first and last occurrence; values appearing once contribute zero. Minimize the
sum of segment costs.

## First principles

Let a candidate final segment start at `l` and currently end at `r-1`. Appending
`a[r]`, whose previous occurrence is `p`, increases its cost by `r-p` exactly
when `l <= p`. Thus all candidate starts in one prefix receive the same range
addition.

For one DP layer, leaf `l` stores
`previous_dp[l] + cost(l,current_right)`. A lazy segment tree range-adds the
new repeated-value contribution and returns the minimum over legal starts.

## Cases that decide correctness

- Exactly `k` nonempty segments are required.
- A value's consecutive occurrence gaps telescope to last minus first.
- Candidates whose previous prefix is impossible stay at infinity.
- Previous-occurrence positions reset for every DP layer.
- A first occurrence adds no segment cost.

## Brute force: quadratic transitions

```python
def partition_game_brute(values: list[int], group_count: int) -> int:
    size = len(values)
    cost = [[0] * (size + 1) for _ in range(size)]
    for left in range(size):
        first_position: dict[int, int] = {}
        last_position: dict[int, int] = {}
        current = 0
        for right in range(left, size):
            value = values[right]
            if value not in first_position:
                first_position[value] = right
            else:
                current -= last_position[value] - first_position[value]
            last_position[value] = right
            current += last_position[value] - first_position[value]
            cost[left][right + 1] = current

    infinity = 10**30
    previous = [infinity] * (size + 1)
    previous[0] = 0
    for _ in range(group_count):
        current = [infinity] * (size + 1)
        for right in range(1, size + 1):
            current[right] = min(
                previous[left] + cost[left][right] for left in range(right)
            )
        previous = current
    return previous[size]
```

The DP takes `O(k n^2)` time after quadratic cost preprocessing.

## Better: update all starts sharing one previous occurrence

When the right endpoint moves, candidate costs change on one prefix rather
than independently. Range addition plus range minimum removes the quadratic
transition scan.

## Expert solution: one lazy tree per DP layer

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size, group_count = map(int, input_stream.readline().split())
    values = list(map(int, input_stream.readline().split()))
    infinity = 10**30
    previous = [infinity] * (size + 1)
    previous[0] = 0

    for _ in range(group_count):
        minimum = [infinity] * (4 * size)
        lazy = [0] * (4 * size)

        def build(node: int, left: int, right: int) -> None:
            if right - left == 1:
                minimum[node] = previous[left]
                return
            middle = (left + right) // 2
            build(node * 2, left, middle)
            build(node * 2 + 1, middle, right)
            minimum[node] = min(minimum[node * 2], minimum[node * 2 + 1])

        def add(
            node: int,
            left: int,
            right: int,
            query_left: int,
            query_right: int,
            difference: int,
        ) -> None:
            if query_right <= left or right <= query_left:
                return
            if query_left <= left and right <= query_right:
                minimum[node] += difference
                lazy[node] += difference
                return
            middle = (left + right) // 2
            add(node * 2, left, middle, query_left, query_right, difference)
            add(
                node * 2 + 1,
                middle,
                right,
                query_left,
                query_right,
                difference,
            )
            minimum[node] = lazy[node] + min(minimum[node * 2], minimum[node * 2 + 1])

        def range_minimum(
            node: int,
            left: int,
            right: int,
            query_left: int,
            query_right: int,
            inherited: int = 0,
        ) -> int:
            if query_right <= left or right <= query_left:
                return infinity
            if query_left <= left and right <= query_right:
                return minimum[node] + inherited
            inherited += lazy[node]
            middle = (left + right) // 2
            return min(
                range_minimum(
                    node * 2,
                    left,
                    middle,
                    query_left,
                    query_right,
                    inherited,
                ),
                range_minimum(
                    node * 2 + 1,
                    middle,
                    right,
                    query_left,
                    query_right,
                    inherited,
                ),
            )

        build(1, 0, size)
        current = [infinity] * (size + 1)
        last_position: dict[int, int] = {}
        for right, value in enumerate(values):
            previous_position = last_position.get(value)
            if previous_position is not None:
                add(
                    1,
                    0,
                    size,
                    0,
                    previous_position + 1,
                    right - previous_position,
                )
            current[right + 1] = range_minimum(1, 0, size, 0, right + 1)
            last_position[value] = right
        previous = current

    print(previous[size])


if __name__ == "__main__":
    solve()
```

Every leaf always equals the prior-layer prefix cost plus the current final
segment cost. The queried prefix contains exactly the legal nonempty starts.

**Complexity:** `O(k n log n)` time and `O(n)` extra space.
