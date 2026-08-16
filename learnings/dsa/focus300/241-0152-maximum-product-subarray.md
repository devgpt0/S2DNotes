# Focus300 241: LeetCode 152 - Maximum Product Subarray

**Source:** [LeetCode 152](https://leetcode.com/problems/maximum-product-subarray/)  
**Difficulty:** Medium  
**Pattern:** running max/min dynamic tracking

## Exact contract

Return the largest product of any contiguous subarray.

## First principles

A negative number can flip a very small product into a very large one, so the best and worst products both matter at every step. Zeros naturally reset the running products.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

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
