# Focus300 286: LeetCode 260 - Single Number III

**Source:** [LeetCode 260](https://leetcode.com/problems/single-number-iii/)  
**Difficulty:** Medium  
**Pattern:** bit-counting modulo three

## Exact contract

Return the unique value that appears once when every other value appears exactly three times.

## First principles

Each bit position is independent. Counting set bits modulo three removes the repeated triples and leaves the bits that belong to the singleton.

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
