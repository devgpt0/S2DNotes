# Focus300 172: LeetCode 39 - Combination Sum

**Source:** [LeetCode 39](https://leetcode.com/problems/combination-sum/)  
**Difficulty:** Medium  
**Pattern:** sorted backtracking with reusable choices

## Exact contract

Given distinct positive integers `candidates` and a positive `target`, return
all unique combinations whose sum is `target`. A candidate may be selected any
number of times. Combination order and result order do not matter.

## First principles

Choose candidates in nondecreasing index order. Reusing the current index allows
unlimited copies; never returning to an earlier index prevents permutations of
one multiset from becoming duplicate answers. Sorting permits immediate pruning
when a candidate exceeds the remaining sum.

## Cases that decide correctness

- Candidates are distinct and positive.
- A recursive reuse stays at the same index, not the next one.
- A zero remainder records one complete combination.
- A negative remainder is unnecessary after sorted pruning.
- `[2, 2, 3]` and `[3, 2, 2]` are the same combination.

## Brute force: enumerate every candidate multiplicity

```python
from itertools import product


def combination_sum_brute(candidates: list[int], target: int) -> list[list[int]]:
    if (
        not candidates
        or len(set(candidates)) != len(candidates)
        or any(value <= 0 for value in candidates)
        or target <= 0
    ):
        raise ValueError("candidates must be distinct positive integers")

    ordered = sorted(candidates)
    answers: list[list[int]] = []
    ranges = (range(target // value + 1) for value in ordered)
    for counts in product(*ranges):
        if sum(count * value for count, value in zip(counts, ordered)) == target:
            answers.append(
                [value for count, value in zip(counts, ordered) for _ in range(count)]
            )
    return answers
```

This examines the Cartesian product of every feasible multiplicity range.

## Better transition: build only prefixes that can still reach the target

Backtracking maintains a remaining sum. Sorted candidates larger than that
remainder cannot appear now or later, so the loop can stop immediately.

## Expert solution: monotone-index backtracking

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    if (
        not candidates
        or len(set(candidates)) != len(candidates)
        or any(value <= 0 for value in candidates)
        or target <= 0
    ):
        raise ValueError("candidates must be distinct positive integers")

    ordered = sorted(candidates)
    answers: list[list[int]] = []
    chosen: list[int] = []

    def search(start: int, remaining: int) -> None:
        if remaining == 0:
            answers.append(chosen.copy())
            return
        for index in range(start, len(ordered)):
            value = ordered[index]
            if value > remaining:
                break
            chosen.append(value)
            search(index, remaining - value)
            chosen.pop()

    search(0, target)
    return answers
```

Every path is nondecreasing and therefore represents one multiset exactly once.

**Complexity:** Output-sensitive exponential time, `O(target / min(candidates))`
recursion depth, excluding returned combinations.
