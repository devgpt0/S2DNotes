# ICPC300 182: Codeforces 786C - Till I Collapse

**Source:** [Codeforces 786C](https://codeforces.com/problemset/problem/786/C)  
**Pattern:** persistent first-occurrence order statistics

## Exact contract

For every `k` from `1` through `n`, partition the array into the minimum number
of nonempty contiguous segments such that each segment contains at most `k`
distinct values. Output all `n` answers.

## First principles

For a fixed `k`, the optimal next segment is the longest valid prefix of the
remaining suffix. Any shorter choice only leaves more elements and cannot use
fewer later segments.

For every suffix start `l`, mark the first occurrence position of each distinct
value in that suffix. The `(k+1)`-st marked position is the first forbidden
position, so the next segment starts there. Persistent segment-tree version
`l` stores exactly those marks and supports this order statistic.

## Cases that decide correctness

- Segments must be nonempty and cover the whole array.
- Equal values contribute one distinct value, regardless of frequency.
- If a suffix has at most `k` distinct values, it is the final segment.
- Moving the suffix start removes its old first occurrence and exposes the next
  one.
- Coordinate compression is unnecessary because the tree indexes positions.

## Brute force: greedy scan for every limit

```python
def till_i_collapse_brute(values: list[int]) -> list[int]:
    size = len(values)
    answers = []
    for limit in range(1, size + 1):
        segments = 0
        start = 0
        while start < size:
            seen: set[int] = set()
            end = start
            while end < size and (values[end] in seen or len(seen) < limit):
                seen.add(values[end])
                end += 1
            segments += 1
            start = end
        answers.append(segments)
    return answers
```

Greedy is correct, but rescanning for every `k` takes `O(n^2)` time.

## Better insight: jump to the next new value

A suffix needs only its ordered first occurrences, not all element positions.
As `k` grows, the number of greedy jumps is at most `n/k + 1`; summing this
over all limits is harmonic.

## Expert solution: persistent marked positions

```python
import sys
from array import array


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    values = list(map(int, input_stream.readline().split()))

    left_child = array("i", [0])
    right_child = array("i", [0])
    count = array("i", [0])

    def update(
        previous: int,
        left: int,
        right: int,
        position: int,
        present: int,
    ) -> int:
        node = len(count)
        left_child.append(left_child[previous])
        right_child.append(right_child[previous])
        count.append(count[previous])
        if right - left == 1:
            count[node] = present
            return node
        middle = (left + right) // 2
        if position < middle:
            left_child[node] = update(
                left_child[previous], left, middle, position, present
            )
        else:
            right_child[node] = update(
                right_child[previous], middle, right, position, present
            )
        count[node] = count[left_child[node]] + count[right_child[node]]
        return node

    def kth(node: int, left: int, right: int, order: int) -> int:
        if right - left == 1:
            return left
        middle = (left + right) // 2
        left_count = count[left_child[node]]
        if order <= left_count:
            return kth(left_child[node], left, middle, order)
        return kth(right_child[node], middle, right, order - left_count)

    roots = [0] * (size + 1)
    next_position: dict[int, int] = {}
    for position in range(size - 1, -1, -1):
        root = roots[position + 1]
        old_position = next_position.get(values[position])
        if old_position is not None:
            root = update(root, 0, size, old_position, 0)
        root = update(root, 0, size, position, 1)
        roots[position] = root
        next_position[values[position]] = position

    answers = []
    for limit in range(1, size + 1):
        segments = 0
        start = 0
        while start < size:
            segments += 1
            if count[roots[start]] <= limit:
                break
            start = kth(roots[start], 0, size, limit + 1)
        answers.append(segments)
    print(" ".join(map(str, answers)))


if __name__ == "__main__":
    solve()
```

Version `l` marks one position per distinct suffix value. Greedy therefore
jumps exactly past the longest valid segment.

**Complexity:** `O(n log^2 n)` time and `O(n log n)` compact integer storage.
