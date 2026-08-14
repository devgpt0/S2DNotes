# Focus300 169: LeetCode 34 - Find First and Last Position in Sorted Array

**Source:** [LeetCode 34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)  
**Difficulty:** Medium  
**Pattern:** paired lower-bound and upper-bound searches

## Exact contract

Given a nondecreasing integer array, return the first and last indices containing
`target`. Return `[-1, -1]` when absent. The required search time is `O(log n)`.

## First principles

One lower-bound search finds the first index whose value is at least the target.
One upper-bound search finds the first index whose value is greater than the
target. If the lower bound contains the target, the answer is
`[lower, upper-1]`; otherwise it is absent.

## Cases that decide correctness

- An empty array returns `[-1, -1]`.
- One occurrence has equal first and last indices.
- A run may touch either array boundary.
- Lower bound alone must be checked before indexing.
- Searching for an insertion boundary differs from stopping on any match.

## Brute force: scan and record matching endpoints

```python
def target_range_brute(numbers: list[int], target: int) -> list[int]:
    if type(numbers) is not list or len(numbers) > 100_000:
        raise ValueError("numbers length must not exceed 100,000")
    if any(
        type(value) is not int or not -1_000_000_000 <= value <= 1_000_000_000
        for value in numbers
    ):
        raise ValueError("numbers must be integers in the source range")
    if any(numbers[index] > numbers[index + 1] for index in range(len(numbers) - 1)):
        raise ValueError("numbers must be sorted in nondecreasing order")
    if type(target) is not int or not -1_000_000_000 <= target <= 1_000_000_000:
        raise ValueError("target must be an integer in the source range")

    first = -1
    last = -1
    for index, value in enumerate(numbers):
        if value == target:
            if first == -1:
                first = index
            last = index
    return [first, last]
```

This takes `O(n)` time even though matching values form one contiguous run.

## Better insight: search for transition boundaries, not a matching element

The predicates `value >= target` and `value > target` are monotone across a
sorted array, so each transition is a lower-bound binary search.

## Expert solution: two boundary searches

```python
def target_range(numbers: list[int], target: int) -> list[int]:
    if type(numbers) is not list or len(numbers) > 100_000:
        raise ValueError("numbers length must not exceed 100,000")
    if any(
        type(value) is not int or not -1_000_000_000 <= value <= 1_000_000_000
        for value in numbers
    ):
        raise ValueError("numbers must be integers in the source range")
    if any(numbers[index] > numbers[index + 1] for index in range(len(numbers) - 1)):
        raise ValueError("numbers must be sorted in nondecreasing order")
    if type(target) is not int or not -1_000_000_000 <= target <= 1_000_000_000:
        raise ValueError("target must be an integer in the source range")

    def boundary(strict: bool) -> int:
        left = 0
        right = len(numbers)
        while left < right:
            middle = (left + right) // 2
            if numbers[middle] > target or not strict and numbers[middle] == target:
                right = middle
            else:
                left = middle + 1
        return left

    first = boundary(strict=False)
    if first == len(numbers) or numbers[first] != target:
        return [-1, -1]
    return [first, boundary(strict=True) - 1]
```

The two monotone searches isolate exactly the half-open run of target values.

**Complexity:** `O(log n)` search time and `O(1)` space after validation.
