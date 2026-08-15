# Focus300 254: LeetCode 179 - Largest Number

**Source:** [LeetCode 179](https://leetcode.com/problems/largest-number/)  
**Difficulty:** Medium  
**Pattern:** math / bit manipulation / counting

## Exact contract

Solve the numeric problem 'Largest Number' using the arithmetic or bitwise rule that the statement implies.

## First principles

Numeric problems usually hide a compact invariant: counts, prefix products, bit parity, or divisibility. Once that invariant is written down, the implementation becomes straightforward.

## Cases that decide correctness

- Zero values often need special handling.
- Negative values may change sign behavior but not the invariant itself.
- Repeated values can cancel or reinforce the desired quantity.
- The answer should usually be derived from a stable count or recurrence, not brute force.

## Brute force

```python
from itertools import permutations


def largest_number_brute(nums):
    if not nums:
        return ""

    best = ""
    for perm in permutations(map(str, nums)):
        candidate = "".join(perm)
        if candidate > best:
            best = candidate
    return "0" if best and best[0] == "0" else best
```

Evaluate the full numeric property directly for each candidate.

## Better insight

Track the needed arithmetic state incrementally so each input element is processed once.

## Expert solution

```python
from functools import cmp_to_key


def largest_number(nums):
    parts = list(map(str, nums))

    def compare(a, b):
        if a + b > b + a:
            return -1
        if a + b < b + a:
            return 1
        return 0

    parts.sort(key=cmp_to_key(compare))
    result = "".join(parts)
    return "0" if result and result[0] == "0" else result
```

Translate the statement into a counting, prefix, parity, or divisibility invariant and update that invariant as you scan.

**Complexity:** Usually O(n) time and O(1) extra space.
