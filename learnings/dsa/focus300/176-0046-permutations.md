# Focus300 176: LeetCode 46 - Permutations

**Source:** [LeetCode 46](https://leetcode.com/problems/permutations/)  
**Difficulty:** Medium  
**Pattern:** backtracking over unused positions

## Exact contract

Given a non-empty list of distinct integers, return every permutation. Each
result must contain every input value exactly once; result order does not matter.

## First principles

A permutation fixes one position at a time. At depth `d`, swap each remaining
value into position `d`, recurse, then undo the swap. The fixed prefix is the
state, so no separate used set or copied prefix is required.


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

- A one-value input has one permutation.
- Source values are distinct, so no duplicate suppression is needed.
- Append a copy only after all positions are fixed.
- Every recursive swap must be undone.
- The caller's input order must be restored before return.

## Brute force: insert each value into every prior permutation

```python
def permute_brute(numbers: list[int]) -> list[list[int]]:
    if not numbers or len(set(numbers)) != len(numbers):
        raise ValueError("numbers must be non-empty and distinct")

    permutations = [[]]
    for value in numbers:
        next_permutations: list[list[int]] = []
        for current in permutations:
            for index in range(len(current) + 1):
                next_permutations.append(current[:index] + [value] + current[index:])
        permutations = next_permutations
    return permutations
```

This creates a new list for every partial insertion and uses `O(n * n!)` result
storage plus intermediate copies.

## Better transition: reuse one mutable arrangement

Only the current prefix boundary and arrangement are needed. In-place swaps
choose a value, and the inverse swap restores the state for the next choice.

## Expert solution: prefix-fixing swaps

```python
def permute(numbers: list[int]) -> list[list[int]]:
    if not numbers or len(set(numbers)) != len(numbers):
        raise ValueError("numbers must be non-empty and distinct")

    arrangement = numbers.copy()
    answers: list[list[int]] = []

    def search(first: int) -> None:
        if first == len(arrangement):
            answers.append(arrangement.copy())
            return
        for index in range(first, len(arrangement)):
            arrangement[first], arrangement[index] = (
                arrangement[index],
                arrangement[first],
            )
            search(first + 1)
            arrangement[first], arrangement[index] = (
                arrangement[index],
                arrangement[first],
            )

    search(0)
    return answers
```

Every leaf corresponds to one sequence of distinct position choices and thus
one permutation.

**Complexity:** `O(n * n!)` time to copy the outputs and `O(n)` recursion space,
excluding the returned `n!` lists.
