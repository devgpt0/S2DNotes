# 135. Kalila and Dimna in the Logging Industry — Codeforces 319C

**Source:** [Codeforces 319C - Kalila and Dimna in the Logging Industry](https://codeforces.com/problemset/problem/319/C)  
**Difficulty:** 2300

## 1. Problem in plain words

Arrays `a` and `b` have equal length. In the source, `a` is strictly increasing and `b` is strictly decreasing. Compute

`dp[0] = 0` and `dp[i] = min(dp[j] + b[j] * a[i])` over every `j < i`.

Print `dp[n - 1]`.

## 2. First principles

For a fixed earlier index `j`, the expression `b[j] * x + dp[j]` is a line evaluated at `x = a[i]`. Each DP step asks for the minimum among all lines inserted so far, then inserts one new line.

The source ordering is especially valuable: slopes are inserted decreasingly and query coordinates increase. A deque can discard lines that will never again be optimal.

## 3. Cases that define correctness

- For one item, the answer is `dp[0] = 0`.
- Large products require 64-bit-or-larger integers; Python integers are exact.
- A line that loses at the current increasing `x` can never beat the winner later when its slope is larger.
- Obsolescence tests must use integer cross-products, not floating-point intersections.

## 4. Brute force

Evaluate every earlier transition directly.

```python
def logging_cost_brute_force(a: list[int], b: list[int]) -> int:
    if len(a) != len(b) or not a:
        raise ValueError("a and b must have the same positive length")

    size = len(a)
    dp = [0] * size
    for index in range(1, size):
        dp[index] = min(
            dp[previous] + b[previous] * a[index] for previous in range(index)
        )
    return dp[-1]
```

Time is `O(n²)` and space is `O(n)`.

## 5. Better approach: Li Chao tree

A Li Chao tree keeps the better line at each coordinate midpoint and sends the losing line only toward the side where it can still win. Using the known query coordinates avoids a huge numeric domain.

```python
def logging_cost_li_chao(a: list[int], b: list[int]) -> int:
    if len(a) != len(b) or not a:
        raise ValueError("a and b must have the same positive length")
    if any(a[index] >= a[index + 1] for index in range(len(a) - 1)):
        raise ValueError("a must be strictly increasing")
    if len(a) == 1:
        return 0

    coordinates = a[1:]
    tree: list[tuple[int, int] | None] = [None] * (4 * len(coordinates))

    def value(line: tuple[int, int], x_value: int) -> int:
        slope, intercept = line
        return slope * x_value + intercept

    def insert(node: int, left: int, right: int, line: tuple[int, int]) -> None:
        current = tree[node]
        if current is None:
            tree[node] = line
            return
        middle = (left + right) // 2
        left_better = value(line, coordinates[left]) < value(current, coordinates[left])
        middle_better = value(line, coordinates[middle]) < value(
            current, coordinates[middle]
        )
        if middle_better:
            tree[node], line = line, current
        if left == right:
            return
        if left_better != middle_better:
            insert(node * 2, left, middle, line)
        else:
            insert(node * 2 + 1, middle + 1, right, line)

    def query(node: int, left: int, right: int, position: int) -> int:
        line = tree[node]
        answer = 10**40 if line is None else value(line, coordinates[position])
        if left == right:
            return answer
        middle = (left + right) // 2
        if position <= middle:
            return min(answer, query(node * 2, left, middle, position))
        return min(answer, query(node * 2 + 1, middle + 1, right, position))

    insert(1, 0, len(coordinates) - 1, (b[0], 0))
    answer = 0
    for index in range(1, len(a)):
        answer = query(1, 0, len(coordinates) - 1, index - 1)
        insert(1, 0, len(coordinates) - 1, (b[index], answer))
    return answer
```

Time is `O(n log n)` and space is `O(n)`; this method does not need monotone slopes.

## 6. Expert solution: monotone convex hull trick

Keep candidate lines in decreasing slope order. Remove the front while the next line is no worse at the current increasing coordinate. Remove a middle line at the back when its two intersection boundaries are out of order.

```python
from collections import deque


def logging_cost(a: list[int], b: list[int]) -> int:
    if len(a) != len(b) or not a:
        raise ValueError("a and b must have the same positive length")
    if any(a[index] >= a[index + 1] for index in range(len(a) - 1)):
        raise ValueError("a must be strictly increasing")
    if any(b[index] <= b[index + 1] for index in range(len(b) - 1)):
        raise ValueError("b must be strictly decreasing")

    def value(line: tuple[int, int], x_value: int) -> int:
        slope, intercept = line
        return slope * x_value + intercept

    def obsolete(
        first: tuple[int, int],
        second: tuple[int, int],
        third: tuple[int, int],
    ) -> bool:
        first_slope, first_intercept = first
        second_slope, second_intercept = second
        third_slope, third_intercept = third
        return (second_intercept - first_intercept) * (second_slope - third_slope) >= (
            third_intercept - second_intercept
        ) * (first_slope - second_slope)

    hull: deque[tuple[int, int]] = deque([(b[0], 0)])
    answer = 0
    for index in range(1, len(a)):
        x_value = a[index]
        while len(hull) >= 2 and value(hull[0], x_value) >= value(hull[1], x_value):
            hull.popleft()
        answer = value(hull[0], x_value)
        new_line = (b[index], answer)
        while len(hull) >= 2 and obsolete(hull[-2], hull[-1], new_line):
            hull.pop()
        hull.append(new_line)
    return answer
```

## 7. Why the expert solution is correct

Every DP predecessor is represented by its line. With decreasing slopes, once the second front line is at least as good at the current `x`, it stays better for every larger `x`, so removing the first is safe. The cross-product test removes exactly a line whose optimal interval is empty. The remaining front therefore gives the minimum transition at every step.

Each line enters and leaves the deque at most once, giving `O(n)` time and `O(n)` space.
