# ICPC300 248: Codeforces 660F - Bear and Bowling 4

**Source:** [Codeforces 660F](https://codeforces.com/problemset/problem/660/F)  
**Difficulty:** 2400  
**Pattern:** prefix algebra plus maximum Li Chao tree

## Exact contract

Choose a nonempty contiguous subarray. Its first value has weight one, its
second value has weight two, and so on. Return the maximum weighted sum over
all choices.

## First principles

Use one-based indices and define

- `P[i] = sum(a[j])` for `j <= i`;
- `Q[i] = sum(j*a[j])` for `j <= i`.

For a subarray beginning after `t` and ending at `r`, its score is

`Q[r] - Q[t] - t*(P[r]-P[t])`.

For fixed `t`, this is `Q[r]` plus a line evaluated at `P[r]`: slope `-t`,
intercept `t*P[t]-Q[t]`. Insert earlier starts and query their maximum.

## Cases that decide correctness

- The chosen subarray must be nonempty.
- Values and prefix sums may be negative.
- Equal prefix sums are valid repeated query coordinates.
- The line for `t=0` represents subarrays starting at index one.
- Products require 64-bit-range arithmetic.

## Brute force: extend every left endpoint

```python
def bear_and_bowling_brute(values: list[int]) -> int:
    answer: int | None = None
    for left in range(len(values)):
        score = 0
        for right in range(left, len(values)):
            score += (right - left + 1) * values[right]
            answer = score if answer is None else max(answer, score)
    if answer is None:
        raise ValueError("values must be nonempty")
    return answer
```

This tries all `O(n^2)` subarrays.

## Better insight: each possible start is one line

The transformed score separates into a right-endpoint term and a maximum over
lines from earlier starts. A Li Chao tree supports arbitrary prefix-sum query
order and negative coordinates.

## Expert solution: Li Chao tree on compressed prefix sums

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    values = list(map(int, input_stream.readline().split()))

    prefix = [0] * (size + 1)
    weighted_prefix = [0] * (size + 1)
    for index, value in enumerate(values, start=1):
        prefix[index] = prefix[index - 1] + value
        weighted_prefix[index] = weighted_prefix[index - 1] + index * value

    coordinates = sorted(set(prefix[1:]))
    coordinate_index = {value: index for index, value in enumerate(coordinates)}
    lines: list[tuple[int, int] | None] = [None] * (4 * len(coordinates))

    def evaluate(line: tuple[int, int], value: int) -> int:
        slope, intercept = line
        return slope * value + intercept

    def add_line(
        new_line: tuple[int, int],
        node: int = 1,
        left: int = 0,
        right: int | None = None,
    ) -> None:
        if right is None:
            right = len(coordinates) - 1
        current = lines[node]
        if current is None:
            lines[node] = new_line
            return
        middle = (left + right) // 2
        if evaluate(new_line, coordinates[middle]) > evaluate(
            current, coordinates[middle]
        ):
            current, new_line = new_line, current
            lines[node] = current
        if left == right:
            return
        if evaluate(new_line, coordinates[left]) > evaluate(current, coordinates[left]):
            add_line(new_line, node * 2, left, middle)
        elif evaluate(new_line, coordinates[right]) > evaluate(
            current, coordinates[right]
        ):
            add_line(new_line, node * 2 + 1, middle + 1, right)

    def query(position: int) -> int:
        value = coordinates[position]
        node = 1
        left = 0
        right = len(coordinates) - 1
        answer = -(10**30)
        while True:
            line = lines[node]
            if line is not None:
                answer = max(answer, evaluate(line, value))
            if left == right:
                return answer
            middle = (left + right) // 2
            if position <= middle:
                node *= 2
                right = middle
            else:
                node = node * 2 + 1
                left = middle + 1

    add_line((0, 0))
    answer = -(10**30)
    for right in range(1, size + 1):
        best_start = query(coordinate_index[prefix[right]])
        answer = max(answer, weighted_prefix[right] + best_start)
        add_line(
            (
                -right,
                right * prefix[right] - weighted_prefix[right],
            )
        )
    print(answer)


if __name__ == "__main__":
    solve()
```

At right endpoint `r`, the tree contains exactly the lines for all valid
`t < r`, so its maximum is the best subarray ending at `r`.

**Complexity:** `O(n log n)` time and `O(n)` space.
