# Focus300 254: LeetCode 179 - Largest Number

**Source:** [LeetCode 179](https://leetcode.com/problems/largest-number/)  
**Difficulty:** Medium  
**Pattern:** math / bit manipulation / counting

## Exact contract

Solve the numeric problem 'Largest Number' using the arithmetic or bitwise rule that the statement implies.

## First principles

Numeric problems usually hide a compact invariant: counts, prefix products, bit parity, or divisibility. Once that invariant is written down, the implementation becomes straightforward.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
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
