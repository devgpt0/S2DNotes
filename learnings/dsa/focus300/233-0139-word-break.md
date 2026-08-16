# Focus300 233: LeetCode 139 - Word Break

**Source:** [LeetCode 139](https://leetcode.com/problems/word-break/)  
**Difficulty:** Medium  
**Pattern:** prefix DP over a dictionary

## Exact contract

Decide whether the string can be segmented into dictionary words.

## First principles

A prefix is valid if some earlier valid prefix can be extended by a dictionary word. That makes the problem a reachability DP over string positions.


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

- The empty string is segmentable by convention.
- Repeated prefixes may be revisited many times without memoization.
- Dictionary words can overlap in many ways.
- The answer is boolean, not the segmentation itself.

## Brute force

```python
from functools import lru_cache

def word_break_brute(s, word_dict):
    words = set(word_dict)

    @lru_cache(None)
    def solve(i):
        if i == len(s):
            return True
        return any(s.startswith(word, i) and solve(i + len(word)) for word in words)

    return solve(0)
```

Try every dictionary word at every position recursively.

## Better insight

Use DP or memoized DFS so each prefix position is solved once.

## Expert solution

```python
def word_break(s, word_dict):
    words = set(word_dict)
    reachable = [False] * (len(s) + 1)
    reachable[0] = True
    for i in range(len(s)):
        if not reachable[i]:
            continue
        for word in words:
            if s.startswith(word, i):
                reachable[i + len(word)] = True
    return reachable[-1]
```

Mark positions that are reachable from valid prefixes, and extend only through dictionary matches.

**Complexity:** O(n^2) time in the usual DP formulation and O(n) space, ignoring dictionary lookup optimizations.
