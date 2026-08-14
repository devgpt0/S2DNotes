# Focus300 192: LeetCode 72 - Edit Distance

**Source:** [LeetCode 72](https://leetcode.com/problems/edit-distance/)  
**Difficulty:** Medium  
**Pattern:** dynamic programming on two string prefixes

## Exact contract

Return the minimum number of single-character insertions, deletions, and
replacements needed to transform one lowercase ASCII word into another. Either
word may be empty.

## First principles

For prefixes ending at two characters, equal final characters need no new
operation. Otherwise the final operation is exactly one of delete, insert, or
replace, leaving a smaller prefix pair. This gives the recurrence over a grid
of prefix lengths; each row depends only on the previous row and its own left
cell.

## Cases that decide correctness

- Transforming an empty word costs the other word's length.
- Equal characters follow the diagonal without adding one.
- Replacement advances both prefixes; insertion and deletion advance one.
- Repeated letters do not permit greedy matching.
- The operation count, not an edit script, is required.

## Brute force: recursively try all final operations

```python
def edit_distance_brute(first: str, second: str) -> int:
    if (
        type(first) is not str
        or type(second) is not str
        or len(first) > 500
        or len(second) > 500
        or any(not "a" <= character <= "z" for character in first + second)
    ):
        raise ValueError("words must be lowercase ASCII strings of length at most 500")

    def solve(first_index: int, second_index: int) -> int:
        if first_index == len(first):
            return len(second) - second_index
        if second_index == len(second):
            return len(first) - first_index
        if first[first_index] == second[second_index]:
            return solve(first_index + 1, second_index + 1)
        return 1 + min(
            solve(first_index + 1, second_index),
            solve(first_index, second_index + 1),
            solve(first_index + 1, second_index + 1),
        )

    return solve(0, 0)
```

Without memoization, overlapping suffix states make this exponential.

## Better insight: every recursive state is one prefix-length pair

Fill those states once from shorter prefixes to longer prefixes. Keeping the
shorter word as columns minimizes the rolling-row memory.

## Expert solution: rolling-row dynamic programming

```python
def edit_distance(first: str, second: str) -> int:
    if (
        type(first) is not str
        or type(second) is not str
        or len(first) > 500
        or len(second) > 500
        or any(not "a" <= character <= "z" for character in first + second)
    ):
        raise ValueError("words must be lowercase ASCII strings of length at most 500")

    if len(first) < len(second):
        first, second = second, first
    previous = list(range(len(second) + 1))
    for first_index, first_character in enumerate(first, start=1):
        current = [first_index]
        for second_index, second_character in enumerate(second, start=1):
            if first_character == second_character:
                current.append(previous[second_index - 1])
            else:
                current.append(
                    1
                    + min(
                        previous[second_index],
                        current[second_index - 1],
                        previous[second_index - 1],
                    )
                )
        previous = current
    return previous[-1]
```

Each cell takes the minimum over the three possible final operations, so the
last cell is the optimal complete transformation cost.

**Complexity:** `O(m*n)` time and `O(min(m, n))` space.
