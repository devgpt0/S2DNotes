# Focus300 244: LeetCode 162 - Find Peak Element

**Source:** [LeetCode 162](https://leetcode.com/problems/find-peak-element/)  
**Difficulty:** Medium  
**Pattern:** binary search on local slope

## Exact contract

Return any index whose value is greater than its neighbors.

## First principles

The array's slope tells us which side must contain a peak. If the middle is rising to the right, a peak must exist on that side; otherwise it must exist on the left.

## Cases that decide correctness

- A single element is trivially a peak.
- The borders can be treated as having negative infinity neighbors.
- Multiple peaks may exist; any one is acceptable.
- Strict inequality matters only against the immediate neighbors.

## Brute force

```python
def find_peak_element_brute(nums):
    for i, num in enumerate(nums):
        left = nums[i - 1] if i > 0 else float("-inf")
        right = nums[i + 1] if i + 1 < len(nums) else float("-inf")
        if num > left and num > right:
            return i
```

Scan all indexes and test each one against its neighbors.

## Better insight

Binary search by comparing the midpoint with its right neighbor and keeping the side that must contain a peak.

## Expert solution

```python
def find_peak_element(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left
```

Use the local slope to cut the search interval in half until one index remains.

**Complexity:** O(log n) time and O(1) space.
