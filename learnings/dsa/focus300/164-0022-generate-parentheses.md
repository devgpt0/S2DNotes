# Focus300 164: LeetCode 22 - Generate Parentheses

**Source:** [LeetCode 22](https://leetcode.com/problems/generate-parentheses/)  
**Difficulty:** Medium  
**Pattern:** constrained prefix backtracking

## Exact contract

Given `n` from `1` through `8`, return every distinct well-formed string using
exactly `n` opening and `n` closing parentheses. Output order is unrestricted.

## First principles

A prefix can still become valid only when it has used at most `n` openings and
never has more closings than openings. Add `(` while openings remain; add `)`
only while `closed < opened`. A length-`2*n` path satisfying those invariants is
automatically a complete well-formed string.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
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

- `n = 1` returns only `"()"`.
- A prefix beginning with `)` is permanently invalid.
- Equal total counts are insufficient if any prefix has negative balance.
- Every output must contain exactly `2*n` characters.
- No set-based deduplication is needed when choices follow prefix counts.

## Brute force: generate all binary parenthesis strings

```python
from itertools import product


def generate_parentheses_brute(pair_count: int) -> list[str]:
    if type(pair_count) is not int or not 1 <= pair_count <= 8:
        raise ValueError("pair_count must be an integer from 1 through 8")

    answer: list[str] = []
    for characters in product("()", repeat=2 * pair_count):
        balance = 0
        valid = True
        for character in characters:
            balance += 1 if character == "(" else -1
            if balance < 0:
                valid = False
                break
        if valid and balance == 0:
            answer.append("".join(characters))
    return answer
```

This explores all `2^(2*n)` strings, including prefixes that can never recover.

## Better insight: reject invalid prefixes before extending them

The counts of opened and closed pairs are a complete state. Branch only to
states that preserve `closed <= opened <= n`.

## Expert solution: invariant-guided backtracking

```python
def generate_parentheses(pair_count: int) -> list[str]:
    if type(pair_count) is not int or not 1 <= pair_count <= 8:
        raise ValueError("pair_count must be an integer from 1 through 8")

    answer: list[str] = []
    path: list[str] = []

    def build(opened: int, closed: int) -> None:
        if closed == pair_count:
            answer.append("".join(path))
            return
        if opened < pair_count:
            path.append("(")
            build(opened + 1, closed)
            path.pop()
        if closed < opened:
            path.append(")")
            build(opened, closed + 1)
            path.pop()

    build(0, 0)
    return answer
```

Every visited prefix is completable, and every valid full string has exactly one
sequence of these opening/closing choices.

**Complexity:** `O(C_n * n)` time for Catalan number `C_n` outputs and `O(n)`
auxiliary recursion space, excluding output.
