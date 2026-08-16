# Focus300 177: LeetCode 47 - Permutations II

**Source:** [LeetCode 47](https://leetcode.com/problems/permutations-ii/)  
**Difficulty:** Medium  
**Pattern:** sorted backtracking with duplicate skipping

## Exact contract

Given a non-empty integer list that may contain duplicates, return every unique
permutation. Each result uses every input index once; result order does not matter.

## First principles

Sort equal values together and track used indices. At one depth, if value `i`
equals value `i - 1`, choose `i` only after the previous equal index has already
been used in the current prefix. This gives identical values one canonical
selection order and removes duplicate branches.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- Equal values from different indices may both appear.
- Skip an equal value only when its previous twin is unused at the same depth.
- Backtracking must clear the exact index it marked.
- Store a copy of each complete permutation.
- All-equal input produces exactly one result.

## Brute force: generate every index permutation and deduplicate

```python
from itertools import permutations


def permute_unique_brute(numbers: list[int]) -> list[list[int]]:
    if not numbers:
        raise ValueError("numbers must be non-empty")
    unique = set(permutations(numbers))
    return [list(candidate) for candidate in sorted(unique)]
```

This generates `n!` tuples even when duplicates make most of them identical.

## Better transition: prevent equivalent branches at each depth

Sorting exposes equal adjacent choices. Requiring the previous equal index to
enter the prefix first canonically orders indistinguishable selections.

## Expert solution: used indices with the twin rule

```python
def permute_unique(numbers: list[int]) -> list[list[int]]:
    if not numbers:
        raise ValueError("numbers must be non-empty")

    ordered = sorted(numbers)
    used = [False] * len(ordered)
    chosen: list[int] = []
    answers: list[list[int]] = []

    def search() -> None:
        if len(chosen) == len(ordered):
            answers.append(chosen.copy())
            return
        for index, value in enumerate(ordered):
            if used[index]:
                continue
            if index > 0 and value == ordered[index - 1] and not used[index - 1]:
                continue
            used[index] = True
            chosen.append(value)
            search()
            chosen.pop()
            used[index] = False

    search()
    return answers
```

The twin rule preserves one branch for each distinct value sequence and rejects
only branches that would spell the same sequence.

**Complexity:** `O(n * U)` time for `U` unique permutations and `O(n)` working
space, excluding returned results.
