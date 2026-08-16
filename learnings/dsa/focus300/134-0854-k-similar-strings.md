# Focus300 134: LeetCode 854 - K-Similar Strings

**Source:** [LeetCode 854](https://leetcode.com/problems/k-similar-strings/)  
**Difficulty:** Hard  
**Pattern:** BFS with first-mismatch pruning

## Exact contract

Given two lowercase anagrams of equal length at most 20, one operation swaps
any two positions in the first string. Return the minimum swaps needed to make
it equal the second string.

## First principles

Strings are vertices in an unweighted swap graph, so BFS gives the minimum.
At the first mismatched position, an optimal next swap can place its required
character there: postponing that correction cannot reduce the number of swaps.
Only positions currently wrong need be considered as donors.


## Classroom board: visit each region or node once

```text
mark what is already seen, expand to neighbors, and stop when the region
is fully explored.
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

- Equal strings need zero swaps.
- Duplicate letters can create many equivalent swap choices.
- Swapping equal characters makes no progress.
- The first-mismatch restriction must still consider every matching donor.
- Non-anagrams cannot be transformed and violate the source contract.

## Brute force: breadth-first search over every unequal swap

```python
from collections import deque


def k_similarity_brute(source: str, target: str) -> int:
    if type(source) is not str or type(target) is not str:
        raise TypeError("source and target must be strings")
    if not 1 <= len(source) == len(target) <= 20:
        raise ValueError("strings must have equal length between 1 and 20")
    if any(not "a" <= character <= "z" for character in source + target):
        raise ValueError("strings must contain only lowercase ASCII letters")
    if sorted(source) != sorted(target):
        raise ValueError("source and target must be anagrams")

    queue = deque([(source, 0)])
    seen = {source}
    while queue:
        current, swaps = queue.popleft()
        if current == target:
            return swaps
        for first in range(len(current)):
            for second in range(first + 1, len(current)):
                if current[first] == current[second]:
                    continue
                characters = list(current)
                characters[first], characters[second] = (
                    characters[second],
                    characters[first],
                )
                candidate = "".join(characters)
                if candidate not in seen:
                    seen.add(candidate)
                    queue.append((candidate, swaps + 1))
    raise RuntimeError("anagrams must be transformable")
```

The state space can contain `n!` permutations and each state tries `O(n^2)`
swaps.

## Better approach: bidirectional search

Expanding from both strings reduces search depth but still generates many
swaps that do not correct a position. First-mismatch pruning removes those
edges while preserving an optimal path.

## Expert solution: swap only a required character into place

```python
from collections import deque


def k_similarity(source: str, target: str) -> int:
    if type(source) is not str or type(target) is not str:
        raise TypeError("source and target must be strings")
    if not 1 <= len(source) == len(target) <= 20:
        raise ValueError("strings must have equal length between 1 and 20")
    if any(not "a" <= character <= "z" for character in source + target):
        raise ValueError("strings must contain only lowercase ASCII letters")
    if sorted(source) != sorted(target):
        raise ValueError("source and target must be anagrams")

    queue = deque([(source, 0)])
    seen = {source}
    while queue:
        current, swaps = queue.popleft()
        if current == target:
            return swaps
        mismatch = next(
            index
            for index, (left, right) in enumerate(zip(current, target, strict=True))
            if left != right
        )
        for donor in range(mismatch + 1, len(current)):
            if current[donor] != target[mismatch] or current[donor] == target[donor]:
                continue
            characters = list(current)
            characters[mismatch], characters[donor] = (
                characters[donor],
                characters[mismatch],
            )
            candidate = "".join(characters)
            if candidate not in seen:
                seen.add(candidate)
                queue.append((candidate, swaps + 1))
    raise RuntimeError("anagrams must be transformable")
```

Every generated edge permanently fixes the earliest mismatch. At least one
optimal path has such a first step, and BFS retains minimum swap depth.

**Complexity:** exponential worst-case time and space, with `O(n)` candidate
swaps per explored state instead of `O(n^2)`.
