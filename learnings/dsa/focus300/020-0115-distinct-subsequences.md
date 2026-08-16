# Focus300 020: LeetCode 115 - Distinct Subsequences

**Source:** [LeetCode 115](https://leetcode.com/problems/distinct-subsequences/)  
**Difficulty:** Hard  
**Pattern:** reverse one-dimensional subsequence DP

## Exact contract

Given nonempty strings `source` and `target` containing English letters, return
the number of distinct index selections in `source` whose selected characters,
in order, equal `target`. The source guarantees the answer fits a signed
32-bit integer.

## First principles

At each source character, either skip it or, when it matches the next target
character, use it. Let `dp[j]` count ways to form the first `j` target
characters from the processed source prefix. A match updates
`dp[j] += dp[j-1]`.


## Classroom board: keep the smallest tail for each length

```text
    nums = [10, 9, 2, 5, 3, 7]

    tails length 1 -> 2
    tails length 2 -> 3
    tails length 3 -> 7
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

- Different index selections count separately even when their text is equal.
- The empty target prefix has one construction: choose nothing.
- A target longer than the source returns zero.
- Character matching is case-sensitive.
- One source character cannot satisfy two target positions.

## Brute force: branch on use or skip

```python
def distinct_subsequences_brute(source: str, target: str) -> int:
    if (
        not source
        or not target
        or any(
            not character.isascii() or not character.isalpha()
            for character in source + target
        )
    ):
        raise ValueError("source and target must contain English letters")

    def count(source_index: int, target_index: int) -> int:
        if target_index == len(target):
            return 1
        if len(source) - source_index < len(target) - target_index:
            return 0
        answer = count(source_index + 1, target_index)
        if source[source_index] == target[target_index]:
            answer += count(source_index + 1, target_index + 1)
        return answer

    return count(0, 0)
```

This mirrors every index-selection decision and takes exponential time.

## Better approach: two-dimensional prefix DP

```python
def distinct_subsequences_table(source: str, target: str) -> int:
    if (
        not source
        or not target
        or any(
            not character.isascii() or not character.isalpha()
            for character in source + target
        )
    ):
        raise ValueError("source and target must contain English letters")

    table = [[0] * (len(target) + 1) for _ in range(len(source) + 1)]
    for source_length in range(len(source) + 1):
        table[source_length][0] = 1
    for source_length in range(1, len(source) + 1):
        for target_length in range(1, min(source_length, len(target)) + 1):
            table[source_length][target_length] = table[source_length - 1][
                target_length
            ]
            if source[source_length - 1] == target[target_length - 1]:
                table[source_length][target_length] += table[source_length - 1][
                    target_length - 1
                ]
    return table[-1][-1]
```

The table stores the exact skip/use recurrence for every pair of prefix lengths
in `O(nm)` time and space.

## Expert solution: update target lengths backward

```python
def distinct_subsequences(source: str, target: str) -> int:
    if (
        not source
        or not target
        or any(
            not character.isascii() or not character.isalpha()
            for character in source + target
        )
    ):
        raise ValueError("source and target must contain English letters")

    ways = [0] * (len(target) + 1)
    ways[0] = 1
    for source_character in source:
        for target_length in range(len(target), 0, -1):
            if source_character == target[target_length - 1]:
                ways[target_length] += ways[target_length - 1]
    return ways[-1]
```

Reverse iteration reads every `ways[j-1]` from the previous source prefix, so
the current character is used at most once. The update is the same recurrence
as the table with all older rows discarded.

**Complexity:** `O(nm)` time and `O(m)` space.
