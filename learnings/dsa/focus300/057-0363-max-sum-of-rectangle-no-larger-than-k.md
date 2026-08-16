# Focus300 057: LeetCode 363 - Max Sum of Rectangle No Larger Than K

**Source:** [LeetCode 363 - Max Sum of Rectangle No Larger Than K](https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/)  
**Difficulty:** Hard  
**Pattern:** dimension compression plus ordered prefix sums  

## Exact contract

Given a nonempty rectangular integer matrix and integer `limit`, return the
largest sum of a nonempty axis-aligned subrectangle whose sum is at most
`limit`. The source guarantees such a rectangle exists.

## First principles

Fix two boundaries along the smaller dimension and compress values between
them into a one-dimensional array. The remaining task is the largest subarray
sum at most `limit`. For current prefix `p`, choose the smallest earlier prefix
at least `p - limit`.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
```



## Step-by-step transformation

1. Compress the input into counts, prefixes, bit masks, or another compact state.
2. Update that state once per element instead of recomputing earlier work.
3. Combine the stored pieces to recover the value the problem asks for.
4. Return the final count, sum, or constructed answer.

These notes transform input into output by reducing the data to a compact invariant first, then rebuilding the answer from that invariant.


## Diagram: compress the input first

```text

            raw values
                |
                v
            counts / prefix / bit state
                |
                v
            combine stored facts
                |
                v
            final answer
```

The algorithm first compresses the input into a small invariant, then rebuilds the answer from that compact state.

## Cases that decide correctness

- Negative values prevent a simple sliding window.
- The optimal rectangle may be one cell.
- A result equal to `limit` is globally optimal and may return immediately.
- Transposing preserves rectangle sums while reducing squared work.
- Prefix ordering must include the empty prefix zero.

## Brute force: sum every rectangle cell by cell

```python
def maximum_rectangle_sum_brute(matrix: list[list[int]], limit: int) -> int:
    if (
        not matrix
        or not matrix[0]
        or any(len(row) != len(matrix[0]) for row in matrix)
        or any(type(value) is not int for row in matrix for value in row)
        or type(limit) is not int
    ):
        raise ValueError("invalid matrix or limit")
    row_count = len(matrix)
    column_count = len(matrix[0])
    answer: int | None = None
    for top in range(row_count):
        for bottom in range(top, row_count):
            for left in range(column_count):
                for right in range(left, column_count):
                    total = sum(
                        matrix[row][column]
                        for row in range(top, bottom + 1)
                        for column in range(left, right + 1)
                    )
                    if total <= limit and (answer is None or total > answer):
                        answer = total
    if answer is None:
        raise ValueError("no rectangle sum is at most limit")
    return answer
```

**Complexity:** `O(r^3 c^3)` time and `O(1)` extra space.

## Better approach: two-dimensional prefix sums

```python
def maximum_rectangle_sum_prefix(matrix: list[list[int]], limit: int) -> int:
    if (
        not matrix
        or not matrix[0]
        or any(len(row) != len(matrix[0]) for row in matrix)
        or any(type(value) is not int for row in matrix for value in row)
        or type(limit) is not int
    ):
        raise ValueError("invalid matrix or limit")
    row_count = len(matrix)
    column_count = len(matrix[0])
    prefix = [[0] * (column_count + 1) for _ in range(row_count + 1)]
    for row in range(row_count):
        for column in range(column_count):
            prefix[row + 1][column + 1] = (
                matrix[row][column]
                + prefix[row][column + 1]
                + prefix[row + 1][column]
                - prefix[row][column]
            )
    answer: int | None = None
    for top in range(row_count):
        for bottom in range(top + 1, row_count + 1):
            for left in range(column_count):
                for right in range(left + 1, column_count + 1):
                    total = (
                        prefix[bottom][right]
                        - prefix[top][right]
                        - prefix[bottom][left]
                        + prefix[top][left]
                    )
                    if total <= limit and (answer is None or total > answer):
                        answer = total
    if answer is None:
        raise ValueError("no rectangle sum is at most limit")
    return answer
```

This reduces each rectangle query to `O(1)`, for `O(r^2 c^2)` total time and
`O(r c)` space.

## Expert solution: compressed bands and Fenwick prefix successor

```python
from bisect import bisect_left


def maximum_rectangle_sum(matrix: list[list[int]], limit: int) -> int:
    if (
        not matrix
        or not matrix[0]
        or any(len(row) != len(matrix[0]) for row in matrix)
        or any(type(value) is not int for row in matrix for value in row)
        or type(limit) is not int
    ):
        raise ValueError("invalid matrix or limit")
    compressed = matrix
    if len(compressed) > len(compressed[0]):
        compressed = [list(column) for column in zip(*compressed, strict=True)]
    row_count = len(compressed)
    column_count = len(compressed[0])

    def best_subarray(values: list[int]) -> int | None:
        prefixes = [0]
        for value in values:
            prefixes.append(prefixes[-1] + value)
        coordinates = sorted(set(prefixes))
        fenwick = [0] * (len(coordinates) + 1)

        def add(rank: int) -> None:
            index = rank + 1
            while index < len(fenwick):
                fenwick[index] += 1
                index += index & -index

        def count_before(end: int) -> int:
            total = 0
            while end:
                total += fenwick[end]
                end -= end & -end
            return total

        def rank_by_order(order: int) -> int:
            index = 0
            step = 1 << (len(coordinates).bit_length() - 1)
            while step:
                next_index = index + step
                if next_index < len(fenwick) and fenwick[next_index] < order:
                    order -= fenwick[next_index]
                    index = next_index
                step >>= 1
            return index

        add(bisect_left(coordinates, 0))
        answer: int | None = None
        for current in prefixes[1:]:
            lower_rank = bisect_left(coordinates, current - limit)
            earlier_count = count_before(lower_rank)
            total_count = count_before(len(coordinates))
            if earlier_count < total_count:
                prefix_rank = rank_by_order(earlier_count + 1)
                candidate = current - coordinates[prefix_rank]
                if answer is None or candidate > answer:
                    answer = candidate
            add(bisect_left(coordinates, current))
        return answer

    answer: int | None = None
    for top in range(row_count):
        column_sums = [0] * column_count
        for bottom in range(top, row_count):
            for column in range(column_count):
                column_sums[column] += compressed[bottom][column]
            candidate = best_subarray(column_sums)
            if candidate == limit:
                return limit
            if candidate is not None and (answer is None or candidate > answer):
                answer = candidate
    if answer is None:
        raise ValueError("no rectangle sum is at most limit")
    return answer
```

The Fenwick tree stores seen compressed prefixes. Its order-statistic search
returns the smallest seen prefix meeting `prefix >= current - limit`, which
maximizes the legal subarray sum for that endpoint.

**Complexity:** `O(min(r,c)^2 * max(r,c) log max(r,c))` time and
`O(max(r,c))` working space.

