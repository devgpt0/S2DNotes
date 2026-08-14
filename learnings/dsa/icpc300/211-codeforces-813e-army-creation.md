# ICPC300 211: Codeforces 813E - Army Creation

**Source:** [Codeforces 813E](https://codeforces.com/problemset/problem/813/E)  
**Pattern:** persistent last-`k` occurrence markers

## Exact contract

Given an array and a limit `k`, each online query supplies encoded `x,y`.
With the previous answer `last`, decode
`l=(x+last) mod n + 1` and `r=(y+last) mod n + 1`, then swap if needed.
Output `sum(min(k, frequency(value in a[l..r])))` over all values, and use that
answer as the next `last`.

## First principles

For prefix ending at `r`, mark exactly the last `k` occurrence positions of
every value. In a query range `[l,r]`, the marked positions count all
occurrences when there are at most `k`, and exactly `k` otherwise.

Build one persistent segment-tree version per prefix. Adding position `i`
sets it to one; when the value now has `k+1` retained occurrences, clear its
oldest retained position. A range sum in version `r` is the answer.

## Cases that decide correctness

- Decode both endpoints with the same previous answer.
- Normalize endpoint order only after decoding.
- Duplicates beyond the last `k` must be unmarked.
- Versions are indexed by inclusive prefix length.
- `k=1` retains only each value's latest prefix occurrence.

## Brute force: count the decoded range

```python
from collections import Counter


def army_creation_brute(
    values: list[int], limit: int, encoded_queries: list[tuple[int, int]]
) -> list[int]:
    size = len(values)
    last = 0
    answers = []
    for raw_left, raw_right in encoded_queries:
        left = (raw_left + last) % size
        right = (raw_right + last) % size
        if left > right:
            left, right = right, left
        frequencies = Counter(values[left : right + 1])
        last = sum(min(limit, count) for count in frequencies.values())
        answers.append(last)
    return answers
```

This rebuilds a frequency table for every query.

## Better insight: retain only answer-contributing occurrences

For a fixed right endpoint, occurrences older than the last `k` of their value
can never contribute to any range ending there. Persistent versions preserve
this filtered prefix for every possible online right endpoint.

## Expert solution: persistent range sums

```python
import sys
from array import array
from collections import defaultdict, deque


def solve() -> None:
    input_stream = sys.stdin.buffer
    size, limit = map(int, input_stream.readline().split())
    values = list(map(int, input_stream.readline().split()))

    left_child = array("i", [0])
    right_child = array("i", [0])
    total = array("i", [0])

    def update(
        previous: int,
        left: int,
        right: int,
        position: int,
        difference: int,
    ) -> int:
        node = len(total)
        left_child.append(left_child[previous])
        right_child.append(right_child[previous])
        total.append(total[previous] + difference)
        if right - left == 1:
            return node
        middle = (left + right) // 2
        if position < middle:
            left_child[node] = update(
                left_child[previous], left, middle, position, difference
            )
        else:
            right_child[node] = update(
                right_child[previous], middle, right, position, difference
            )
        return node

    def range_sum(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> int:
        if node == 0 or query_right <= left or right <= query_left:
            return 0
        if query_left <= left and right <= query_right:
            return total[node]
        middle = (left + right) // 2
        return range_sum(
            left_child[node], left, middle, query_left, query_right
        ) + range_sum(right_child[node], middle, right, query_left, query_right)

    roots = [0] * (size + 1)
    retained: defaultdict[int, deque[int]] = defaultdict(deque)
    for position, value in enumerate(values):
        root = update(roots[position], 0, size, position, 1)
        retained[value].append(position)
        if len(retained[value]) > limit:
            root = update(root, 0, size, retained[value].popleft(), -1)
        roots[position + 1] = root

    query_count = int(input_stream.readline())
    last = 0
    output = []
    for _ in range(query_count):
        raw_left, raw_right = map(int, input_stream.readline().split())
        left = (raw_left + last) % size
        right = (raw_right + last) % size
        if left > right:
            left, right = right, left
        last = range_sum(roots[right + 1], 0, size, left, right + 1)
        output.append(str(last))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Version `r+1` contains one marker for each of the last `k` prefix occurrences.
Intersecting those markers with `[l,r]` gives exactly the capped frequencies.

**Complexity:** `O((n+q) log n)` time and `O(n log n)` compact storage.
