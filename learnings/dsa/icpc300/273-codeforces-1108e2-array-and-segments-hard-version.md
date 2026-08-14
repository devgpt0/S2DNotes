# ICPC300 273: Codeforces 1108E2 - Array and Segments (Hard version)

**Source:** [Codeforces 1108E2](https://codeforces.com/problemset/problem/1108/E2)  
**Difficulty:** 2200  
**Pattern:** sweep a protected maximum with lazy range minima

## Exact contract

Choose any listed inclusive segments. For every chosen segment, subtract one
from each covered array value. Maximize the final maximum minus minimum, then
print that difference and one set of chosen segment indices.

## First principles

Fix an index `p` that will remain a maximum. An optimal solution never chooses
a segment containing `p`: removing such an operation restores `p` and cannot
hurt the spread. Every segment not containing `p` should be chosen because it
only lowers other positions.

Thus evaluate

`a[p] - min(array after decrementing all segments not containing p)`.

Sweep `p`. A segment starts or stops being selected only when the sweep crosses
one endpoint, so a lazy minimum tree maintains the transformed array.

## Cases that decide correctness

- Segments are inclusive.
- Several identical segments are separate selectable operations.
- Ties may use any maximizing protected index.
- Segments strictly left or right of `p` are selected.
- Output indices are one-based.

## Brute force: enumerate all segment subsets

```python
def array_and_segments_brute(
    values: list[int],
    segments: list[tuple[int, int]],
) -> tuple[int, list[int]]:
    best_difference = -1
    best_segments: list[int] = []
    for mask in range(1 << len(segments)):
        changed = values.copy()
        selected: list[int] = []
        for index, (left, right) in enumerate(segments):
            if not (mask >> index & 1):
                continue
            selected.append(index + 1)
            for position in range(left, right + 1):
                changed[position] -= 1
        difference = max(changed) - min(changed)
        if difference > best_difference:
            best_difference = difference
            best_segments = selected
    return best_difference, best_segments
```

This takes `O(2^m(n+m))` time.

## Better insight: protect one maximum and select every segment avoiding it

At position one, select exactly the segments starting later. Moving the
protected position right removes segments that now contain it and adds those
whose right endpoint was just crossed.

## Expert solution: endpoint sweep plus lazy minimum tree

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size, segment_count = map(int, input_stream.readline().split())
    values = list(map(int, input_stream.readline().split()))
    segments: list[tuple[int, int]] = []
    starting: list[list[int]] = [[] for _ in range(size)]
    ending: list[list[int]] = [[] for _ in range(size)]
    for index in range(segment_count):
        left, right = map(int, input_stream.readline().split())
        left -= 1
        right -= 1
        segments.append((left, right))
        starting[left].append(index)
        ending[right].append(index)

    minimum = [0] * (4 * size)
    lazy = [0] * (4 * size)

    def build(node: int, left: int, right: int) -> None:
        if right - left == 1:
            minimum[node] = values[left]
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
        delta: int,
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            minimum[node] += delta
            lazy[node] += delta
            return
        middle = (left + right) // 2
        add(node * 2, left, middle, query_left, query_right, delta)
        add(node * 2 + 1, middle, right, query_left, query_right, delta)
        minimum[node] = lazy[node] + min(minimum[node * 2], minimum[node * 2 + 1])

    build(1, 0, size)
    for index, (left, right) in enumerate(segments):
        if left > 0:
            add(1, 0, size, left, right + 1, -1)

    best_difference = -1
    best_position = 0
    for position in range(size):
        if position:
            for index in starting[position]:
                left, right = segments[index]
                add(1, 0, size, left, right + 1, 1)
            for index in ending[position - 1]:
                left, right = segments[index]
                add(1, 0, size, left, right + 1, -1)
        difference = values[position] - minimum[1]
        if difference > best_difference:
            best_difference = difference
            best_position = position

    selected = [
        index + 1
        for index, (left, right) in enumerate(segments)
        if not left <= best_position <= right
    ]
    print(best_difference)
    print(len(selected))
    print(*selected)


if __name__ == "__main__":
    solve()
```

At every sweep position, the tree contains exactly the result of applying all
segments that avoid that position.

**Complexity:** `O((n+m) log n)` time and `O(n+m)` space.
