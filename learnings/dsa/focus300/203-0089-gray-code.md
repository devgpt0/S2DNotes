# Focus300 203: LeetCode 89 - Gray Code

**Source:** [LeetCode 89](https://leetcode.com/problems/gray-code/)  
**Difficulty:** Medium  
**Pattern:** reflected sequence generation

## Exact contract

Generate an `n`-bit Gray code sequence in which consecutive numbers differ by exactly one bit.

## First principles

Reflection preserves the one-bit-difference property because the second half is the first half reversed with a new high bit set. Each additional bit doubles the sequence while changing only one bit at each transition.

## Cases that decide correctness

- Zero bits should still produce a valid starting sequence.
- Consecutive outputs must differ by exactly one bit.
- The sequence length must be `2^n`.
- The first and last values are both valid members of the cycle.

## Brute force

```python
def gray_code_brute(n):
    return [i ^ (i >> 1) for i in range(1 << n)]
```

Generate ordinary binary numbers and filter for adjacency, which is wasteful and fragile.

## Better insight

Build the next bit layer by reflecting the current sequence and prefixing the new bit.

## Expert solution

```python
def gray_code(n):
    result = [0]
    for bit in range(n):
        result += [x | (1 << bit) for x in reversed(result)]
    return result
```

Start from `[0]` and repeatedly append the reversed sequence with the new bit set in each reflected value.

**Complexity:** O(2^n) time and O(2^n) space for the output.
