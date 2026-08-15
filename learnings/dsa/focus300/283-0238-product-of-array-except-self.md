# Focus300 283: LeetCode 238 - Product of Array Except Self

**Source:** [LeetCode 238](https://leetcode.com/problems/product-of-array-except-self/)  
**Difficulty:** Medium  
**Pattern:** prefix and suffix products

## Exact contract

Return an array where each position contains the product of all other values except the value at that position.

## First principles

The product for one index is the product of everything to its left times the product of everything to its right. Prefix and suffix products expose those two pieces directly without division.

## Cases that decide correctness

- Arrays with one or more zeros need special care but still work under prefix/suffix products.
- The answer length must match the input length.
- Division is intentionally avoided.
- The current index's own value must never be included in its product.

## Brute force

```python
def product_except_self_brute(nums):
    result = []
    for i in range(len(nums)):
        prod = 1
        for j, num in enumerate(nums):
            if i != j:
                prod *= num
        result.append(prod)
    return result
```

Compute each position's product by multiplying all other values explicitly.

## Better insight

Precompute cumulative products from the left and from the right.

## Expert solution

```python
def product_except_self(nums):
    result = [1] * len(nums)
    prefix = 1
    for i in range(len(nums)):
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result
```

Store the left prefix product for each index, then multiply by a running right suffix product in reverse order.

**Complexity:** O(n) time and O(1) extra space beyond the output array.
