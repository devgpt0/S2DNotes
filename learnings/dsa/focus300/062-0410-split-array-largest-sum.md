# Focus300 062: LeetCode 410 - Split Array Largest Sum

**Source:** [LeetCode 410](https://leetcode.com/problems/split-array-largest-sum/)  
**Difficulty:** Hard  
**Pattern:** binary search on a monotone capacity predicate

## Exact contract

Split a nonnegative integer array into exactly `k` nonempty contiguous parts.
Return the smallest possible value of the largest part sum.

## First principles

For a proposed maximum sum `limit`, greedily extend each part until the next
number would exceed the limit, then start a new part. This produces the minimum
number of parts possible under that limit.

If it needs at most `k` parts, further splitting can reach exactly `k` because
all elements are nonnegative and `k <= n`. Feasibility is monotone, so binary
search the answer between `max(nums)` and `sum(nums)`.

## Cases that decide correctness

- Every part is nonempty.
- `k=1` returns the total sum.
- `k=n` returns the maximum element.
- Nonnegativity is what makes greedy feasibility valid.
- Exact `k` is equivalent to at most `k` for a feasible capacity.

## Brute force: enumerate every next cut

```python
def split_array_brute(values: list[int], part_count: int) -> int:
    if not 1 <= part_count <= len(values):
        raise ValueError("part_count must be between one and array length")
    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)

    def search(start: int, remaining_parts: int) -> int:
        if remaining_parts == 1:
            return prefix[-1] - prefix[start]
        answer = 10**30
        last_end = len(values) - remaining_parts + 1
        for end in range(start + 1, last_end + 1):
            first_sum = prefix[end] - prefix[start]
            answer = min(answer, max(first_sum, search(end, remaining_parts - 1)))
        return answer

    return search(0, part_count)
```

This explores every choice of `k-1` cut positions.

## Better approach: prefix-sum partition DP

```python
def split_array_dp(values: list[int], part_count: int) -> int:
    if not 1 <= part_count <= len(values):
        raise ValueError("part_count must be between one and array length")
    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)
    previous = prefix.copy()
    for parts in range(2, part_count + 1):
        current = [10**30] * (len(values) + 1)
        for end in range(parts, len(values) + 1):
            for cut in range(parts - 1, end):
                current[end] = min(
                    current[end],
                    max(previous[cut], prefix[end] - prefix[cut]),
                )
        previous = current
    return previous[-1]
```

This is `O(k n^2)` time and `O(n)` DP space.

## Expert solution: binary-search the minimum feasible largest sum

```python
def split_array(values: list[int], part_count: int) -> int:
    if not 1 <= part_count <= len(values):
        raise ValueError("part_count must be between one and array length")

    def required_parts(limit: int) -> int:
        parts = 1
        current_sum = 0
        for value in values:
            if current_sum + value > limit:
                parts += 1
                current_sum = value
            else:
                current_sum += value
        return parts

    low = max(values)
    high = sum(values)
    while low < high:
        middle = (low + high) // 2
        if required_parts(middle) <= part_count:
            high = middle
        else:
            low = middle + 1
    return low
```

Greedy gives the exact feasibility boundary for each capacity, and binary search
returns the smallest feasible one.

**Complexity:** `O(n log(sum(nums)))` time and `O(1)` space.
