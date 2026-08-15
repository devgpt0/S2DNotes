# Focus300 264: LeetCode 201 - Bitwise AND of Numbers Range

**Source:** [LeetCode 201](https://leetcode.com/problems/bitwise-and-of-numbers-range/)  
**Difficulty:** Medium  
**Pattern:** math / bit manipulation / counting

## Exact contract

Solve the numeric problem 'Bitwise AND of Numbers Range' using the arithmetic or bitwise rule that the statement implies.

## First principles

Numeric problems usually hide a compact invariant: counts, prefix products, bit parity, or divisibility. Once that invariant is written down, the implementation becomes straightforward.

## Cases that decide correctness

- Zero values often need special handling.
- Negative values may change sign behavior but not the invariant itself.
- Repeated values can cancel or reinforce the desired quantity.
- The answer should usually be derived from a stable count or recurrence, not brute force.

## Brute force

```python
def range_bitwise_and_brute(left, right):
    result = left
    for num in range(left + 1, right + 1):
        result &= num
    return result
```

Evaluate the full numeric property directly for each candidate.

## Better insight

Track the needed arithmetic state incrementally so each input element is processed once.

## Expert solution

```python
def range_bitwise_and(left, right):
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift
```

Translate the statement into a counting, prefix, parity, or divisibility invariant and update that invariant as you scan.

**Complexity:** Usually O(n) time and O(1) extra space.
