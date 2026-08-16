# Focus300 120: LeetCode 801 - Minimum Swaps To Make Sequences Increasing

**Source:** [LeetCode 801](https://leetcode.com/problems/minimum-swaps-to-make-sequences-increasing/)  
**Difficulty:** Hard  
**Pattern:** two-state dynamic programming

## Exact contract

Given equal-length nonempty integer arrays `first` and `second`, one operation
swaps `first[i]` with `second[i]`. Return the minimum operations that make both
arrays strictly increasing. The source guarantees a solution and allows up to
100,000 positions.

## First principles

At index `i`, future feasibility depends only on whether index `i` was swapped,
not the full earlier swap history. There are two transitions: preserve both
current pairings when each array increases straight across, or cross the
pairings when each current value exceeds the other array's previous value.


## Classroom board: store the repeated state once

```text
brute force recomputes the same subproblem many times.
dp keeps the smallest useful state and extends it one step at a time.
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

- Strict increase uses `>`, not `>=`.
- Swapping index zero costs one but has no predecessor constraint.
- Straight and crossed transitions can both be legal at the same index.
- A swapped predecessor and kept current index use crossed comparisons.
- Inputs of different lengths or an impossible instance fail fast here.

## Brute force: enumerate every swap mask

```python
def minimum_increasing_swaps_brute(first: list[int], second: list[int]) -> int:
    if (
        type(first) is not list
        or type(second) is not list
        or any(type(value) is not int for value in first + second)
    ):
        raise TypeError("first and second must be lists of integers")
    if len(first) != len(second) or not 1 <= len(first) <= 100_000:
        raise ValueError("arrays must have equal length between 1 and 100000")

    answer = len(first) + 1
    for mask in range(1 << len(first)):
        first_candidate = [
            second[index] if mask & (1 << index) else first[index]
            for index in range(len(first))
        ]
        second_candidate = [
            first[index] if mask & (1 << index) else second[index]
            for index in range(len(first))
        ]
        if all(
            first_candidate[index - 1] < first_candidate[index]
            and second_candidate[index - 1] < second_candidate[index]
            for index in range(1, len(first))
        ):
            answer = min(answer, mask.bit_count())
    if answer > len(first):
        raise ValueError("the arrays cannot both be made strictly increasing")
    return answer
```

This examines `2^n` masks and validates each in `O(n)` time.

## Better approach: keep two full DP arrays

Store the minimum cost for every prefix ending with its last pair kept or
swapped. This makes the recurrence explicit in `O(n)` time and `O(n)` space,
but only the preceding two costs are needed by the next index.

## Expert solution: roll kept and swapped prefix costs

```python
def minimum_increasing_swaps(first: list[int], second: list[int]) -> int:
    if (
        type(first) is not list
        or type(second) is not list
        or any(type(value) is not int for value in first + second)
    ):
        raise TypeError("first and second must be lists of integers")
    if len(first) != len(second) or not 1 <= len(first) <= 100_000:
        raise ValueError("arrays must have equal length between 1 and 100000")

    infinity = len(first) + 1
    kept = 0
    swapped = 1
    for index in range(1, len(first)):
        next_kept = infinity
        next_swapped = infinity
        if first[index - 1] < first[index] and second[index - 1] < second[index]:
            next_kept = min(next_kept, kept)
            next_swapped = min(next_swapped, swapped + 1)
        if first[index - 1] < second[index] and second[index - 1] < first[index]:
            next_kept = min(next_kept, swapped)
            next_swapped = min(next_swapped, kept + 1)
        kept, swapped = next_kept, next_swapped

    answer = min(kept, swapped)
    if answer >= infinity:
        raise ValueError("the arrays cannot both be made strictly increasing")
    return answer
```

`kept` and `swapped` are the optimal costs for the processed prefix under its
last decision. The two comparison patterns enumerate every legal transition,
so discarding higher costs for the same state is safe.

**Complexity:** `O(n)` time and `O(1)` auxiliary space.
