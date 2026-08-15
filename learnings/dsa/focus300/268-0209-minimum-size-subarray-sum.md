# Focus300 268: LeetCode 209 - Minimum Size Subarray Sum

**Source:** [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/)  
**Difficulty:** Medium  
**Pattern:** math / bit manipulation / counting

## Exact contract

Solve the numeric problem 'Minimum Size Subarray Sum' using the arithmetic or bitwise rule that the statement implies.

## First principles

Numeric problems usually hide a compact invariant: counts, prefix products, bit parity, or divisibility. Once that invariant is written down, the implementation becomes straightforward.

## Cases that decide correctness

- Zero values often need special handling.
- Negative values may change sign behavior but not the invariant itself.
- Repeated values can cancel or reinforce the desired quantity.
- The answer should usually be derived from a stable count or recurrence, not brute force.

## Brute force

```python
def min_sub_array_len_brute(target, nums):
    best = float("inf")
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= target:
                best = min(best, j - i + 1)
                break
    return 0 if best == float("inf") else best
```

Evaluate the full numeric property directly for each candidate.

## Better insight

Track the needed arithmetic state incrementally so each input element is processed once.

## Expert solution

```python
def min_sub_array_len(target, nums):
    left = total = 0
    best = float("inf")
    for right, num in enumerate(nums):
        total += num
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == float("inf") else best
```

Translate the statement into a counting, prefix, parity, or divisibility invariant and update that invariant as you scan.

**Complexity:** Usually O(n) time and O(1) extra space.
