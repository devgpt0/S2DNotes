# Focus300 001: LeetCode 4 - Median of Two Sorted Arrays

**Source:** [LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/)  
**Difficulty:** Hard  
**Pattern:** binary search on a cross-array partition

## Exact contract

Given two individually sorted integer arrays with at least one total element,
return the median of their combined multiset. The required target complexity
is `O(log(m+n))`.

## First principles

The median depends only on a partition with half the values on each side. If
the shorter array contributes `i` values to the left half, the longer array
must contribute `half-i`. The partition is valid when both left boundary
values are no greater than the opposite right boundary values.

If `first[i-1] > second[j]`, move `i` left. Otherwise, if
`second[j-1] > first[i]`, move `i` right.

## Cases that decide correctness

- Either input may be empty, but not both.
- Total length may be odd or even.
- Duplicate and negative values do not change the partition rule.
- A cut may be before the first or after the last array element.
- Binary search must run on the shorter array so the complementary cut is valid.

## Brute force: combine and sort

```python
def median_sort(first: list[int], second: list[int]) -> float:
    merged = sorted(first + second)
    if not merged:
        raise ValueError("at least one array must be nonempty")
    middle = len(merged) // 2
    if len(merged) & 1:
        return float(merged[middle])
    return (merged[middle - 1] + merged[middle]) / 2
```

This is `O((m+n) log(m+n))` time and `O(m+n)` space.

## Better approach: merge only through the middle

```python
def median_partial_merge(first: list[int], second: list[int]) -> float:
    total = len(first) + len(second)
    if total == 0:
        raise ValueError("at least one array must be nonempty")
    first_index = 0
    second_index = 0
    previous = 0
    current = 0
    for _ in range(total // 2 + 1):
        previous = current
        if second_index == len(second) or (
            first_index < len(first) and first[first_index] <= second[second_index]
        ):
            current = first[first_index]
            first_index += 1
        else:
            current = second[second_index]
            second_index += 1
    if total & 1:
        return float(current)
    return (previous + current) / 2
```

This is `O(m+n)` time in the worst case and `O(1)` auxiliary space.

## Expert solution: binary-search the shorter partition

```python
def find_median_sorted_arrays(first: list[int], second: list[int]) -> float:
    if len(first) > len(second):
        first, second = second, first
    if not second:
        raise ValueError("at least one array must be nonempty")

    first_length = len(first)
    second_length = len(second)
    left_size = (first_length + second_length + 1) // 2
    low = 0
    high = first_length
    while low <= high:
        first_cut = (low + high) // 2
        second_cut = left_size - first_cut

        first_left = first[first_cut - 1] if first_cut else float("-inf")
        first_right = first[first_cut] if first_cut < first_length else float("inf")
        second_left = second[second_cut - 1] if second_cut else float("-inf")
        second_right = (
            second[second_cut] if second_cut < second_length else float("inf")
        )

        if first_left <= second_right and second_left <= first_right:
            if (first_length + second_length) & 1:
                return float(max(first_left, second_left))
            return (max(first_left, second_left) + min(first_right, second_right)) / 2
        if first_left > second_right:
            high = first_cut - 1
        else:
            low = first_cut + 1
    raise ValueError("inputs must be sorted")
```

The valid partition contains exactly the lower half and directly exposes the
one or two central values.

**Complexity:** `O(log(min(m,n)))` time and `O(1)` space.
