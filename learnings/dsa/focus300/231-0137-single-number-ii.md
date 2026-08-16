# Focus300 231: LeetCode 137 - Single Number II

**Source:** [LeetCode 137](https://leetcode.com/problems/single-number-ii/)  
**Difficulty:** Medium  
**Pattern:** bit-counting modulo three

## Exact contract

Return the unique value that appears once when every other value appears exactly three times.

## First principles

Each bit position is independent. Counting set bits modulo three removes the repeated triples and leaves the bits that belong to the singleton.


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

- Negative values require a signed representation to be handled consistently.
- The unique value may have any bit pattern.
- Triples of the same value must vanish completely.
- Bit arithmetic is enough; no sorting is needed.

## Brute force

```python
from collections import Counter

def single_number_brute(nums):
    counts = Counter(nums)
    for num, count in counts.items():
        if count == 1:
            return num
```

Sort or hash-count all values and then scan for the singleton.

## Better insight

Accumulate bit counts or maintain bitwise state machines that cancel after three hits.

## Expert solution

```python
def single_number(nums):
    ones = twos = 0
    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones
    return ones
```

Track per-bit counts modulo three, then reconstruct the remaining bit pattern as the answer.

**Complexity:** O(n) time and O(1) space for fixed integer width.
