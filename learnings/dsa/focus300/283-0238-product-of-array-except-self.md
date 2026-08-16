# Focus300 283: LeetCode 238 - Product of Array Except Self

**Source:** [LeetCode 238](https://leetcode.com/problems/product-of-array-except-self/)  
**Difficulty:** Medium  
**Pattern:** prefix and suffix products

## Exact contract

Return an array where each position contains the product of all other values except the value at that position.

## First principles

The product for one index is the product of everything to its left times the product of everything to its right. Prefix and suffix products expose those two pieces directly without division.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
```



## Step-by-step transformation

1. Compress the input into counts, prefixes, bit masks, or another compact state.
2. Update that state once per element instead of recomputing earlier work.
3. Combine the stored pieces to recover the value the problem asks for.
4. Return the final count, sum, or constructed answer.

These notes transform input into output by reducing the data to a compact invariant first, then rebuilding the answer from that invariant.


## Diagram: compress the input first

```text

            raw values
                |
                v
            counts / prefix / bit state
                |
                v
            combine stored facts
                |
                v
            final answer
```

The algorithm first compresses the input into a small invariant, then rebuilds the answer from that compact state.

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
