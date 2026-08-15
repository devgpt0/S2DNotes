# Focus300 245: LeetCode 164 - Maximum Gap

**Source:** [LeetCode 164](https://leetcode.com/problems/maximum-gap/)  
**Difficulty:** Hard  
**Pattern:** bucket-based linear-time gap detection

## Exact contract

Return the maximum difference between consecutive numbers after sorting the array.

## First principles

The maximum adjacent gap in sorted order must occur between buckets, not inside a bucket, once the values are distributed across the range evenly enough. That observation avoids a full sort.

## Cases that decide correctness

- Fewer than two values give zero gap.
- Duplicate values should not inflate the gap.
- The minimum and maximum values determine the global range.
- One bucket may remain empty without affecting correctness.

## Brute force

```python
def maximum_gap_brute(nums):
    nums = sorted(nums)
    return max((b - a for a, b in zip(nums, nums[1:])), default=0)
```

Sort the entire array and scan adjacent pairs.

## Better insight

Distribute the numbers into value buckets and compare only the bucket boundaries.

## Expert solution

```python
def maximum_gap(nums):
    if len(nums) < 2:
        return 0
    mn, mx = min(nums), max(nums)
    if mn == mx:
        return 0
    n = len(nums)
    size = max(1, (mx - mn) // (n - 1))
    bucket_count = (mx - mn) // size + 1
    buckets = [[None, None] for _ in range(bucket_count)]
    for num in nums:
        i = (num - mn) // size
        lo, hi = buckets[i]
        buckets[i][0] = num if lo is None else min(lo, num)
        buckets[i][1] = num if hi is None else max(hi, num)
    best = prev = None
    for lo, hi in buckets:
        if lo is None:
            continue
        if prev is not None:
            best = max(best or 0, lo - prev)
        prev = hi
    return best or 0
```

Compute bucket size from the global range, track each bucket's min and max, and derive the maximum gap from consecutive non-empty buckets.

**Complexity:** O(n) time and O(n) space.
