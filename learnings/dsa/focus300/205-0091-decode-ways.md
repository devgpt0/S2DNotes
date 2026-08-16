# Focus300 205: LeetCode 91 - Decode Ways

**Source:** [LeetCode 91](https://leetcode.com/problems/decode-ways/)  
**Difficulty:** Medium  
**Pattern:** prefix dynamic programming on a digit string

## Exact contract

Count how many valid letter decodings the digit string admits under the `1 -> A` through `26 -> Z` mapping.

## First principles

Each position depends only on the previous one or two positions, because a digit can stand alone or join with its predecessor as a two-digit code. Invalid zero placements are the main failure mode.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
```



## Step-by-step transformation

1. Turn the input into subproblems, prefixes, or states that can be reused.
2. Fill the base cases first so later states have something correct to build on.
3. Update each new state from earlier states while keeping the recurrence valid.
4. Read the answer from the final table entry or the best state collected at the end.

Dynamic-programming style notes transform the input by compressing many repeated choices into a small set of reusable states.


## Diagram: state table to answer

```text

            input
                |
                v
            base states
                |
                v
            reuse smaller states
                |
                v
            final dp answer
```

These notes compress repeated choices into reusable states, then read the answer from the last state that matters.

## Cases that decide correctness

- A leading zero is invalid.
- A `0` must be paired with `1` or `2`.
- Two-digit values above `26` cannot be decoded as a pair.
- A string with no valid split has answer `0`.

## Brute force

```python
from functools import lru_cache

def num_decodings_brute(s):
    @lru_cache(None)
    def solve(i):
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        total = solve(i + 1)
        if i + 1 < len(s) and int(s[i : i + 2]) <= 26:
            total += solve(i + 2)
        return total

    return solve(0)
```

Try every valid split recursively and recompute suffix counts repeatedly.

## Better insight

Use a rolling DP over the string prefixes so each index is solved once.

## Expert solution

```python
def num_decodings(s):
    if not s or s[0] == "0":
        return 0
    prev2 = 1
    prev1 = 1
    for i in range(1, len(s)):
        cur = 0
        if s[i] != "0":
            cur += prev1
        if "10" <= s[i - 1 : i + 1] <= "26":
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1
```

Carry the count of ways to reach the previous two positions and update the current count from single-digit and two-digit transitions.

**Complexity:** O(n) time and O(1) space.
