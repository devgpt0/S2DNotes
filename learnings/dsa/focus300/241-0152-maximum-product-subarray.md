# Focus300 241: LeetCode 152 - Maximum Product Subarray

**Source:** [LeetCode 152](https://leetcode.com/problems/maximum-product-subarray/)  
**Difficulty:** Medium  
**Pattern:** running max/min dynamic tracking

## Exact contract

Return the largest product of any contiguous subarray.

## First principles

A negative number can flip a very small product into a very large one, so the best and worst products both matter at every step. Zeros naturally reset the running products.

## Cases that decide correctness

- A zero splits the array into independent regions.
- Two negatives can create a large positive product.
- The answer may be a single element.
- The running minimum is as important as the running maximum.

## Brute force

```python
def max_product_brute(nums):
    best = nums[0]
    for i in range(len(nums)):
        product = 1
        for j in range(i, len(nums)):
            product *= nums[j]
            best = max(best, product)
    return best
```

Check every subarray product directly.

## Better insight

Track the best and worst product ending at each index and update both on every step.

## Expert solution

```python
def max_product(nums):
    best = cur_max = cur_min = nums[0]
    for num in nums[1:]:
        if num < 0:
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(num, cur_max * num)
        cur_min = min(num, cur_min * num)
        best = max(best, cur_max)
    return best
```

Maintain the maximum and minimum product that end at the current position, swap them when the next number is negative, and update the global answer from the maximum tracker.

**Complexity:** O(n) time and O(1) space.
