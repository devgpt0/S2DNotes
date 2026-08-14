# Focus300 173: LeetCode 40 - Combination Sum II

**Source:** [LeetCode 40](https://leetcode.com/problems/combination-sum-ii/)  
**Difficulty:** Medium  
**Pattern:** duplicate-aware one-use backtracking

## Exact contract

Given positive integer `candidates`, possibly with duplicates, and a positive
`target`, return every unique combination summing to `target`. Each input index
may be used at most once. Combination order and result order do not matter.

## First principles

Sort the values. After choosing index `i`, recurse from `i + 1` to enforce
one-time use. At one recursion depth, equal adjacent values create identical
subtrees, so explore only the first; the same value remains available at deeper
levels when it comes from a different input index.

## Cases that decide correctness

- Equal values at different indices may both appear in one combination.
- One input index can never be reused.
- Skip duplicates only among sibling choices at the same depth.
- Sorted values allow pruning when a value exceeds the remainder.
- Store value sequences, not index sequences.

## Brute force: enumerate index subsets and deduplicate values

```python
def combination_sum_two_brute(
    candidates: list[int],
    target: int,
) -> list[list[int]]:
    if not candidates or any(value <= 0 for value in candidates) or target <= 0:
        raise ValueError("candidates and target must be positive")

    answers: set[tuple[int, ...]] = set()
    for mask in range(1, 1 << len(candidates)):
        chosen = tuple(
            sorted(
                value for index, value in enumerate(candidates) if mask & (1 << index)
            )
        )
        if sum(chosen) == target:
            answers.add(chosen)
    return [list(answer) for answer in sorted(answers)]
```

This takes `O(n * 2^n)` time and may store exponentially many subset tuples.

## Better transition: eliminate duplicate subtrees before exploring them

Sorting puts equal choices together. A sibling equality check prevents duplicate
answers at their source instead of generating and hashing them afterward.

## Expert solution: sorted one-use backtracking

```python
def combination_sum_two(
    candidates: list[int],
    target: int,
) -> list[list[int]]:
    if not candidates or any(value <= 0 for value in candidates) or target <= 0:
        raise ValueError("candidates and target must be positive")

    ordered = sorted(candidates)
    answers: list[list[int]] = []
    chosen: list[int] = []

    def search(start: int, remaining: int) -> None:
        if remaining == 0:
            answers.append(chosen.copy())
            return
        for index in range(start, len(ordered)):
            if index > start and ordered[index] == ordered[index - 1]:
                continue
            value = ordered[index]
            if value > remaining:
                break
            chosen.append(value)
            search(index + 1, remaining - value)
            chosen.pop()

    search(0, target)
    return answers
```

Increasing indices enforce one use, and skipping equal siblings gives each
value multiset one canonical search path.

**Complexity:** `O(2^n * n)` worst-case time including copied outputs and
`O(n)` recursion space, excluding results.
