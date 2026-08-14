# ICPC300 249: Codeforces 1083E - The Fair Nut and the Rectangles

**Source:** [Codeforces 1083E](https://codeforces.com/problemset/problem/1083/E)  
**Difficulty:** 2200  
**Pattern:** rectangle DP optimized by a maximum Li Chao tree

## Exact contract

Rectangle `i` spans from `(0,0)` to `(x_i,y_i)` and costs `a_i` to choose.
Choose any subset and maximize the area of its union minus the chosen costs.

## First principles

Sort rectangles by width. If rectangle `i` is last, the source recurrence is

`dp[i] = x_i*y_i - a_i + max(0, dp[j] - x_j*y_i)` over earlier `j`.

Each earlier state is a line at `y_i`: slope `-x_j`, intercept `dp[j]`.
The zero line represents starting a new chain.

## Cases that decide correctness

- The answer may use one rectangle; the zero line handles that start.
- Equal dimensions remain valid inputs and are processed in sorted order.
- Costs can make a state unprofitable without making it safe to discard its line.
- Heights are not monotone after sorting by width.
- Products and profits require 64-bit-range integers.

## Brute force: evaluate every earlier transition

```python
def fair_nut_rectangles_brute(
    rectangles: list[tuple[int, int, int]],
) -> int:
    ordered = sorted(rectangles)
    dynamic = [0] * len(ordered)
    answer = 0
    for index, (width, height, cost) in enumerate(ordered):
        previous = 0
        for earlier in range(index):
            previous = max(
                previous,
                dynamic[earlier] - ordered[earlier][0] * height,
            )
        dynamic[index] = width * height - cost + previous
        answer = max(answer, dynamic[index])
    return answer
```

This computes the recurrence in `O(n^2)` time.

## Better insight: the transition is a line evaluated at the new height

Widths determine slopes, dynamic values determine intercepts, and query
heights can arrive in any order. A Li Chao tree removes the inner DP loop.

## Expert solution: sort and maintain transition lines

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    rectangle_count = int(input_stream.readline())
    rectangles = sorted(
        tuple(map(int, input_stream.readline().split())) for _ in range(rectangle_count)
    )
    coordinates = sorted({height for _, height, _ in rectangles})
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
    answer = 0
    for width, height, cost in rectangles:
        best_previous = query(coordinate_index[height])
        dynamic = width * height - cost + best_previous
        answer = max(answer, dynamic)
        add_line((-width, dynamic))
    print(answer)


if __name__ == "__main__":
    solve()
```

Before each query, the tree contains the transition for every earlier
rectangle and the zero start, so the returned maximum is exactly the DP term.

**Complexity:** `O(n log n)` time and `O(n)` space.
