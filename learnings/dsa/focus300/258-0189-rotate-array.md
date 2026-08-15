# Focus300 258: LeetCode 189 - Rotate Array

**Source:** [LeetCode 189](https://leetcode.com/problems/rotate-array/)  
**Difficulty:** Easy  
**Pattern:** array rotation by reversal

## Exact contract

Rotate the array to the right by `k` steps in place.

## First principles

A rotation can be decomposed into three reversals: reverse the whole array, reverse the first `k` items, and reverse the remainder. That converts a circular move into simple local swaps.

## Cases that decide correctness

- A rotation by a multiple of the array length leaves the array unchanged.
- Single-element arrays are unchanged.
- Large `k` values should be reduced modulo the array length.
- The operation must preserve the values, only their positions change.

## Brute force

```python
def rotate_brute(nums, k):
    n = len(nums)
    if n == 0:
        return nums

    k %= n
    for _ in range(k):
        nums.insert(0, nums.pop())
    return nums
```

Move one step at a time, repeating `k` times.

## Better insight

Use the three-reversal trick or an auxiliary copy if space is acceptable.

## Expert solution

```python
def rotate(nums, k):
    n = len(nums)
    if n == 0:
        return nums

    k %= n

    def reverse(left, right):
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
    return nums
```

Normalize `k`, reverse the full array, then reverse each segment that should remain internally ordered.

**Complexity:** O(n) time and O(1) space.
