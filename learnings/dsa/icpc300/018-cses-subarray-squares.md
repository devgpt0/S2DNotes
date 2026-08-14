# ICPC300 018: CSES - Subarray Squares

**Source:** [CSES - Subarray Squares](https://cses.fi/problemset/task/2086/)  
**Pattern:** partition DP, divide-and-conquer optimization, convex hull trick  
**Goal:** Split a positive integer array into exactly `k` nonempty contiguous
subarrays and minimize the sum of the squares of their sums.

## 1. Problem in plain words

For values `[1, 2, 3]` and `k = 2`, the two split positions give:

- `[1] | [2, 3]`: `1^2 + 5^2 = 26`;
- `[1, 2] | [3]`: `3^2 + 3^2 = 18`.

The answer is `18`. Exactly `k` groups are required; empty groups are illegal.

## 2. First principles

Let `prefix[i]` be the sum of the first `i` values. The sum of subarray
`[j, i)` is `prefix[i] - prefix[j]`.

Define `dp[g][i]` as the minimum cost to divide the first `i` values into
exactly `g` nonempty groups:

`dp[g][i] = min(dp[g-1][j] + (prefix[i] - prefix[j])^2)` for `g-1 <= j < i`.

This recurrence is already correct. The challenge is reducing its quadratic
transition scan.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| `k = 1` | Square of the whole-array sum. |
| `k = n` | Sum of the squares of individual values. |
| Equal prefix coordinates | Keep the cheaper equal-slope hull line. |
| `k > n` or `k < 1` | Reject: nonempty groups are impossible. |
| Positive source values | Prefix sums and hull queries are nondecreasing. |

## 4. Brute force: scan every final split

```python
def minimum_subarray_square_sum_brute_force(values: list[int], group_count: int) -> int:
    value_count = len(values)
    if not 1 <= group_count <= value_count:
        raise ValueError("group count must be between one and the array length")

    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)

    infinity = 10**100
    previous = [infinity] * (value_count + 1)
    previous[0] = 0

    for groups in range(1, group_count + 1):
        current = [infinity] * (value_count + 1)
        for end in range(groups, value_count + 1):
            current[end] = min(
                previous[split] + (prefix[end] - prefix[split]) ** 2
                for split in range(groups - 1, end)
            )
        previous = current

    return previous[value_count]
```

**Why it works:** every partition has one unique final split `j`; the
recurrence tries it and combines it with an optimal partition of the prefix.

**Complexity:** `O(k n^2)` time and `O(n)` DP memory.

## 5. Better: divide-and-conquer DP optimization

The segment cost is Monge for nonnegative values. Consequently, the optimal
split index for `dp[g][i]` never moves left as `i` increases. Divide the range
of end positions, find the midpoint's best split, and use it to narrow both
recursive searches.

```python
def minimum_subarray_square_sum_divide_and_conquer(
    values: list[int], group_count: int
) -> int:
    value_count = len(values)
    if not 1 <= group_count <= value_count:
        raise ValueError("group count must be between one and the array length")
    if any(value < 0 for value in values):
        raise ValueError("divide-and-conquer monotonicity requires nonnegative values")

    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)

    infinity = 10**100
    previous = [infinity] * (value_count + 1)
    previous[0] = 0

    for groups in range(1, group_count + 1):
        current = [infinity] * (value_count + 1)

        def compute(
            left: int,
            right: int,
            option_left: int,
            option_right: int,
        ) -> None:
            if left > right:
                return
            middle = (left + right) // 2
            best_value = infinity
            best_split = -1
            last_split = min(middle - 1, option_right)

            for split in range(option_left, last_split + 1):
                candidate = previous[split] + (prefix[middle] - prefix[split]) ** 2
                if candidate < best_value:
                    best_value = candidate
                    best_split = split

            if best_split == -1:
                raise RuntimeError("no legal nonempty final group")
            current[middle] = best_value
            compute(left, middle - 1, option_left, best_split)
            compute(middle + 1, right, best_split, option_right)

        compute(groups, value_count, groups - 1, value_count - 1)
        previous = current

    return previous[value_count]
```

**Complexity:** `O(k n log n)` time and `O(n)` DP memory, plus `O(log n)`
recursion depth.

## 6. Expert solution: monotone convex hull trick

Expand one transition:

`dp[g-1][j] + prefix[j]^2 - 2*prefix[i]*prefix[j] + prefix[i]^2`.

For fixed `j`, the first three terms except `prefix[i]^2` form a line queried
at `x = prefix[i]`:

- slope `m = -2 * prefix[j]`;
- intercept `b = dp[g-1][j] + prefix[j]^2`.

Positive values make query coordinates increase and inserted slopes decrease,
so a deque hull gives amortized constant time per transition.

```python
from collections import deque

Line = tuple[int, int]


def minimum_subarray_square_sum(values: list[int], group_count: int) -> int:
    value_count = len(values)
    if not 1 <= group_count <= value_count:
        raise ValueError("group count must be between one and the array length")
    if any(value < 0 for value in values):
        raise ValueError("source values must be nonnegative")

    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)

    infinity = 10**100
    previous = [infinity] * (value_count + 1)
    previous[0] = 0

    def evaluate(line: Line, coordinate: int) -> int:
        slope, intercept = line
        return slope * coordinate + intercept

    def is_redundant(first: Line, second: Line, third: Line) -> bool:
        first_slope, first_intercept = first
        second_slope, second_intercept = second
        third_slope, third_intercept = third
        return (second_intercept - first_intercept) * (second_slope - third_slope) >= (
            third_intercept - second_intercept
        ) * (first_slope - second_slope)

    for groups in range(1, group_count + 1):
        current = [infinity] * (value_count + 1)
        hull: deque[Line] = deque()

        def add_line(line: Line) -> None:
            if hull and hull[-1][0] == line[0]:
                if hull[-1][1] <= line[1]:
                    return
                hull.pop()
            while len(hull) >= 2 and is_redundant(hull[-2], hull[-1], line):
                hull.pop()
            hull.append(line)

        def query(coordinate: int) -> int:
            while len(hull) >= 2 and evaluate(hull[0], coordinate) >= evaluate(
                hull[1], coordinate
            ):
                hull.popleft()
            return evaluate(hull[0], coordinate)

        for end in range(groups, value_count + 1):
            split = end - 1
            add_line(
                (
                    -2 * prefix[split],
                    previous[split] + prefix[split] ** 2,
                )
            )
            current[end] = prefix[end] ** 2 + query(prefix[end])
        previous = current

    return previous[value_count]
```

### Why the expert code is correct

- Algebra turns every legal split into one line with exactly the same value.
- Line `j = end - 1` is inserted before querying `end`, so the hull contains
  precisely all legal splits for that state.
- The cross-product test removes a line only when its useful intersection
  interval is empty; it uses exact integer arithmetic.
- With increasing queries, once the second line is no worse than the first,
  the first can never become optimal again.

**Complexity:** `O(kn)` time and `O(n)` memory.

## 7. What to remember

For squared segment sums, expand the square. A partition transition often
becomes `query a line + prefix[i]^2`, exposing convex-hull optimization.
