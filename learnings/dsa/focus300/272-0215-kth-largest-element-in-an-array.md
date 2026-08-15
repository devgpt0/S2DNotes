# Focus300 272: LeetCode 215 - Kth Largest Element in an Array

**Source:** [LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/)  
**Difficulty:** Medium  
**Pattern:** selection with a heap or quickselect

## Exact contract

Return the `k`th largest value in the array.

## First principles

The answer is defined by rank, not by full ordering. That means a partial-order algorithm can stop as soon as the target rank is isolated.

## Cases that decide correctness

- Duplicates count as separate positions in the ranking.
- `k = 1` returns the maximum value.
- `k = n` returns the minimum value.
- The input need not be sorted globally.

## Brute force

```python
def find_kth_largest_brute(nums, k):
    return sorted(nums, reverse=True)[k - 1]
```

Sort the entire array and index the answer.

## Better insight

Use a size-`k` heap or quickselect so only part of the order needs to be discovered.

## Expert solution

```python
import heapq

def find_kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap[0]
```

Keep the `k` largest seen elements in a heap, or partition the array around pivots until the pivot rank matches `k`.

**Complexity:** O(n log k) with a heap or average O(n) with quickselect.
