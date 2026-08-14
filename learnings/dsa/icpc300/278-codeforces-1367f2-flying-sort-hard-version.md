# ICPC300 278: Codeforces 1367F2 - Flying Sort (Hard Version)

**Source:** [Codeforces 1367F2](https://codeforces.com/problemset/problem/1367/F2)  
**Difficulty:** 2400  
**Pattern:** longest immovable middle over consecutive value ranks

## Exact contract

In one operation, remove any array element and insert it at the beginning or
the end. Find the minimum operations needed to make the array nondecreasing.
Answer multiple test cases.

## First principles

Elements never moved form a middle subsequence in the sorted result. Its values
must occupy consecutive compressed ranks. If it spans at least three ranks,
every internal rank must keep all its occurrences; only the two boundary ranks
may be partial.

Maintain the best keepable sequence ending with all occurrences of rank `v`.
It either begins with the occurrences of `v-1` before the first `v`, or extends
the previous state when every `v-1` occurs before every `v`. Add a suffix of
rank `v+1` after the last `v`. Intervals using only two adjacent ranks need a
separate merged-position scan for their longest nondecreasing subsequence.

## Cases that decide correctness

- Equal values preserve no meaningful internal order.
- A one-rank middle can keep every occurrence of that value.
- Two boundary ranks can both be partial.
- A full-rank chain extends only across strictly separated position lists.
- The answer is `n` minus the longest legal unmoved middle.

## Brute force: breadth-first search over move results

```python
from collections import deque


def flying_sort_brute(values: list[int]) -> int:
    start = tuple(values)
    target = tuple(sorted(values))
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        current, distance = queue.popleft()
        if current == target:
            return distance
        for index, value in enumerate(current):
            remaining = current[:index] + current[index + 1 :]
            for changed in ((value,) + remaining, remaining + (value,)):
                if changed not in seen:
                    seen.add(changed)
                    queue.append((changed, distance + 1))
    raise AssertionError("sorted state must be reachable")
```

This explores exponentially many array states.

## Better insight: maximize what stays in the sorted middle

Position lists make full-rank compatibility a last-before-first comparison.
Each adjacent-rank merge is linear in the two list sizes, so all such scans
together are linear after compression.

## Expert solution: full-rank DP plus adjacent-pair scans

```python
from bisect import bisect_left, bisect_right
import sys


def minimum_moves(values: list[int]) -> int:
    rank = {value: index for index, value in enumerate(sorted(set(values)))}
    positions: list[list[int]] = [[] for _ in range(len(rank))]
    for index, value in enumerate(values):
        positions[rank[value]].append(index)

    state = [0] * len(positions)
    best = max(map(len, positions))
    for value, current_positions in enumerate(positions):
        left_boundary = 0
        if value:
            left_boundary = bisect_left(positions[value - 1], current_positions[0])
        state[value] = len(current_positions) + left_boundary
        if value and positions[value - 1][-1] < current_positions[0]:
            state[value] = max(
                state[value],
                state[value - 1] + len(current_positions),
            )

        right_boundary = 0
        if value + 1 < len(positions):
            right_boundary = len(positions[value + 1]) - bisect_right(
                positions[value + 1], current_positions[-1]
            )
        best = max(best, state[value] + right_boundary)

        if value + 1 == len(positions):
            continue
        lower = current_positions
        upper = positions[value + 1]
        lower_index = 0
        upper_index = 0
        lower_seen = 0
        upper_remaining = len(upper)
        adjacent_best = upper_remaining
        while lower_index < len(lower) or upper_index < len(upper):
            if upper_index == len(upper) or (
                lower_index < len(lower) and lower[lower_index] < upper[upper_index]
            ):
                lower_seen += 1
                lower_index += 1
            else:
                upper_remaining -= 1
                upper_index += 1
            adjacent_best = max(adjacent_best, lower_seen + upper_remaining)
        best = max(best, adjacent_best)
    return len(values) - best


def solve() -> None:
    input_stream = sys.stdin.buffer
    test_count = int(input_stream.readline())
    answers: list[str] = []
    for _ in range(test_count):
        input_stream.readline()
        values = list(map(int, input_stream.readline().split()))
        answers.append(str(minimum_moves(values)))
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

The DP covers every middle with a full internal rank; the adjacent scans cover
the only missing case where both ranks may be partial.

**Complexity:** `O(n log n)` time and `O(n)` space per test case.
