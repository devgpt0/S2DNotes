# Focus300 049: LeetCode 327 - Count of Range Sum

**Source:** [LeetCode 327](https://leetcode.com/problems/count-of-range-sum/)  
**Difficulty:** Hard  
**Pattern:** prefix sums counted during merge sort

## Exact contract

Given a nonempty integer array and inclusive bounds `lower <= upper`, return the
number of index pairs `start <= end` whose subarray sum lies in
`[lower, upper]`.

## First principles

With prefix sums, a subarray sum is `prefix[right] - prefix[left]`. For each
left prefix, count later prefixes inside
`[prefix[left] + lower, prefix[left] + upper]`. Sorting prefix halves makes both
range boundaries advance monotonically.

## Cases that decide correctness

- Bounds and values may be negative.
- Both bounds are inclusive.
- Equal prefix sums represent different indices and must be counted separately.
- The initial zero prefix enables subarrays starting at index zero.
- Only later prefixes may pair with the current left prefix.

## Brute force: enumerate all subarrays

```python
def count_range_sum_brute(numbers: list[int], lower: int, upper: int) -> int:
    if not numbers or lower > upper:
        raise ValueError("numbers must be nonempty and bounds ordered")

    answer = 0
    for left in range(len(numbers)):
        total = 0
        for right in range(left, len(numbers)):
            total += numbers[right]
            answer += lower <= total <= upper
    return answer
```

This takes `O(n^2)` time and `O(1)` auxiliary space.

## Better approach: compressed Fenwick prefix counts

```python
from bisect import bisect_left, bisect_right


def count_range_sum_fenwick(numbers: list[int], lower: int, upper: int) -> int:
    if not numbers or lower > upper:
        raise ValueError("numbers must be nonempty and bounds ordered")

    prefixes = [0]
    for number in numbers:
        prefixes.append(prefixes[-1] + number)
    coordinates = sorted(set(prefixes))
    tree = [0] * (len(coordinates) + 1)

    def add(index: int) -> None:
        index += 1
        while index < len(tree):
            tree[index] += 1
            index += index & -index

    def count_first(length: int) -> int:
        answer = 0
        while length:
            answer += tree[length]
            length -= length & -length
        return answer

    answer = 0
    for prefix in prefixes:
        left = bisect_left(coordinates, prefix - upper)
        right = bisect_right(coordinates, prefix - lower)
        answer += count_first(right) - count_first(left)
        add(bisect_left(coordinates, prefix))
    return answer
```

The Fenwick tree contains exactly earlier prefix sums and answers each numeric
interval count in `O(log n)` time.

## Expert solution: count cross-half ranges while merging

```python
def count_range_sum(numbers: list[int], lower: int, upper: int) -> int:
    if not numbers or lower > upper:
        raise ValueError("numbers must be nonempty and bounds ordered")

    prefixes = [0]
    for number in numbers:
        prefixes.append(prefixes[-1] + number)

    def sort_count(left: int, right: int) -> int:
        if right - left <= 1:
            return 0
        middle = (left + right) // 2
        answer = sort_count(left, middle) + sort_count(middle, right)
        first_valid = middle
        after_valid = middle
        for first in prefixes[left:middle]:
            while first_valid < right and prefixes[first_valid] - first < lower:
                first_valid += 1
            while after_valid < right and prefixes[after_valid] - first <= upper:
                after_valid += 1
            answer += after_valid - first_valid

        merged: list[int] = []
        first_index = left
        second_index = middle
        while first_index < middle and second_index < right:
            if prefixes[first_index] <= prefixes[second_index]:
                merged.append(prefixes[first_index])
                first_index += 1
            else:
                merged.append(prefixes[second_index])
                second_index += 1
        merged.extend(prefixes[first_index:middle])
        merged.extend(prefixes[second_index:right])
        prefixes[left:right] = merged
        return answer

    return sort_count(0, len(prefixes))
```

Recursive halves count ranges entirely inside themselves. Because both halves
are sorted, the two right-half bounds only advance for cross pairs, counting
each valid earlier-later prefix pair once before the halves merge.

**Complexity:** `O(n log n)` time and `O(n)` merge space.
