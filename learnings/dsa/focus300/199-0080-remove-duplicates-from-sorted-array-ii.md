# Focus300 199: LeetCode 80 - Remove Duplicates from Sorted Array II

**Source:** [LeetCode 80](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)  
**Difficulty:** Medium  
**Pattern:** two-pointer write window

## Exact contract

Remove duplicates from a sorted array in place so that each value appears at most twice, and return the new logical length.

## First principles

A sorted array already groups equal values, so the only question is how many copies of the current value should survive. A write pointer can preserve the allowed prefix while the scan pointer examines the rest.

## Cases that decide correctness

- An array with no duplicates should remain unchanged.
- Three or more equal values must collapse to two copies.
- The first two elements are always safe when the array has length at least two.
- The result is measured by length, not by allocating a new array.

## Brute force

```python
def remove_duplicates_brute(nums):
    result = []
    for num in nums:
        if result.count(num) < 2:
            result.append(num)
    nums[:] = result
    return len(nums)
```

Count every run and rebuild a fresh array with at most two copies per value.

## Better insight

Maintain a write index and copy only values that do not violate the two-copy rule.

## Expert solution

```python
def remove_duplicates(nums):
    write = 0
    for num in nums:
        if write < 2 or num != nums[write - 2]:
            nums[write] = num
            write += 1
    return write
```

Scan left to right, compare against the element two positions behind the write frontier, and overwrite in place only when the new value is still allowed.

**Complexity:** O(n) time and O(1) space.
