# Focus300 199: LeetCode 80 - Remove Duplicates from Sorted Array II

**Source:** [LeetCode 80](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)  
**Difficulty:** Medium  
**Pattern:** two-pointer write window

## Exact contract

Remove duplicates from a sorted array in place so that each value appears at most twice, and return the new logical length.

## First principles

A sorted array already groups equal values, so the only question is how many copies of the current value should survive. A write pointer can preserve the allowed prefix while the scan pointer examines the rest.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

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
