# Focus300 225: LeetCode 128 - Longest Consecutive Sequence

**Source:** [LeetCode 128](https://leetcode.com/problems/longest-consecutive-sequence/)  
**Difficulty:** Medium  
**Pattern:** hash-set streak expansion

## Exact contract

Return the length of the longest run of consecutive integers present in the input.

## First principles

The input order is irrelevant; only membership matters. A value starts a streak only when its predecessor is absent, which prevents counting the same run multiple times.


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

- Duplicates should not change the answer.
- A single number forms a streak of length one.
- The scan should only expand from streak starts.
- Large gaps make sorting unnecessary if membership checks are constant time.

## Brute force

```python
def longest_consecutive_brute(nums):
    nums = sorted(set(nums))
    best = cur = 0
    prev = None
    for num in nums:
        if prev is not None and num == prev + 1:
            cur += 1
        else:
            cur = 1
        best = max(best, cur)
        prev = num
    return best
```

Sort the numbers and scan for adjacent runs.

## Better insight

Store all values in a hash set and expand only from numbers that start a streak.

## Expert solution

```python
def longest_consecutive(nums):
    values = set(nums)
    best = 0
    for num in values:
        if num - 1 not in values:
            cur = num
            length = 1
            while cur + 1 in values:
                cur += 1
                length += 1
            best = max(best, length)
    return best
```

For each value with no predecessor present, walk forward while the next value exists, tracking the longest streak length seen.

**Complexity:** O(n) average time and O(n) space.
