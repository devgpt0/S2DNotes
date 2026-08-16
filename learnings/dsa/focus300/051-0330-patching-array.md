# Focus300 051: LeetCode 330 - Patching Array

**Source:** [LeetCode 330 - Patching Array](https://leetcode.com/problems/patching-array/)  
**Difficulty:** Hard  
**Pattern:** greedy maintenance of a contiguous subset-sum prefix  

## Exact contract

Given a nondecreasing list of positive integers, add the minimum number of
positive integers so every value in `[1, target]` is representable as a subset
sum of the resulting multiset.

## First principles

Suppose every sum in `[1, missing)` is representable. An input value at most
`missing` extends coverage through `missing + value - 1`. If the next input is
larger, no existing value can create `missing`; patching exactly `missing` is
forced and maximally extends coverage through `2*missing - 1`.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
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

- `target = 0` needs no patches.
- Duplicate input values remain separate subset choices.
- An input value larger than the first missing sum cannot help yet.
- Patching any value below `missing` extends less; above it leaves a gap.
- The source array must be positive and nondecreasing.

## Brute force: enumerate patch multisets

```python
from itertools import combinations_with_replacement


def minimum_patches_brute(values: list[int], target: int) -> int:
    if (
        type(target) is not int
        or target < 0
        or any(type(value) is not int or value <= 0 for value in values)
        or values != sorted(values)
    ):
        raise ValueError(
            "values must be sorted positive integers and target nonnegative"
        )

    def covers(patches: tuple[int, ...]) -> bool:
        reachable = {0}
        for value in [*values, *patches]:
            reachable |= {subtotal + value for subtotal in tuple(reachable)}
        return all(value in reachable for value in range(1, target + 1))

    for patch_count in range(target + 1):
        for patches in combinations_with_replacement(range(1, target + 1), patch_count):
            if covers(patches):
                return patch_count
    raise RuntimeError("patching every value from 1 through target always works")
```

**Complexity:** exponential in `target` and the number of patches.

## Better approach: no separate genuine intermediate

A subset-sum table can verify a proposed patch set, but choosing patches by DP
adds a large target dimension. The first-missing invariant directly proves the
optimal linear greedy choice.

## Expert solution: patch the first uncovered sum

```python
def minimum_patches(values: list[int], target: int) -> int:
    if (
        type(target) is not int
        or target < 0
        or any(type(value) is not int or value <= 0 for value in values)
        or values != sorted(values)
    ):
        raise ValueError(
            "values must be sorted positive integers and target nonnegative"
        )
    missing = 1
    value_index = 0
    patches = 0
    while missing <= target:
        if value_index < len(values) and values[value_index] <= missing:
            missing += values[value_index]
            value_index += 1
        else:
            missing += missing
            patches += 1
    return patches
```

The invariant starts with empty coverage `[1, 1)`. Each transition preserves
complete coverage, and when a gap exists only a patch at most `missing` can
close it; choosing `missing` gives the largest possible new interval.

**Complexity:** `O(len(values) + log target)` time and `O(1)` space.

