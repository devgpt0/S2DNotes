# Focus300 090: LeetCode 664 - Strange Printer

**Source:** [LeetCode 664](https://leetcode.com/problems/strange-printer/)  
**Difficulty:** Hard  
**Pattern:** interval dynamic programming with equal-character merging

## Exact contract

A printer starts with a blank string and, in one turn, writes one lowercase
letter across any contiguous interval, overwriting previous characters there.
For a nonempty lowercase target of length at most 100, return the minimum turns
needed to print it.

## First principles

Printing the first character of an interval separately costs one turn plus the
rest. If the same character occurs later, the turn printing that later
occurrence can be extended left to print the first occurrence too. The text
between those equal characters must still be completed independently, which
creates an interval split.


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

- One turn prints any nonempty run of one repeated character.
- Overwriting is allowed and is essential for targets such as `aba`.
- Adjacent equal characters never need separate turns.
- The interval recurrence must allow an empty middle between equal neighbors.
- Only lowercase ASCII letters satisfy the source contract.

## Brute force: breadth-first search over printed states

```python
from collections import deque


def strange_printer_turns_brute(target: str) -> int:
    if type(target) is not str:
        raise TypeError("target must be a string")
    if not 1 <= len(target) <= 100:
        raise ValueError("target length must be between 1 and 100")
    if any(not "a" <= character <= "z" for character in target):
        raise ValueError("target must contain only lowercase ASCII letters")

    start = "\0" * len(target)
    queue = deque([(start, 0)])
    seen = {start}
    alphabet = set(target)
    while queue:
        state, turns = queue.popleft()
        for left in range(len(target)):
            for right in range(left, len(target)):
                for character in alphabet:
                    next_state = (
                        state[:left]
                        + character * (right - left + 1)
                        + state[right + 1 :]
                    )
                    if next_state == target:
                        return turns + 1
                    if next_state not in seen:
                        seen.add(next_state)
                        queue.append((next_state, turns + 1))
    raise RuntimeError("every valid target must be printable")
```

The search is exact but has exponentially many string states and
`O(a * n^2)` outgoing operations per state for `a` distinct target letters.

## Better approach: interval dynamic programming

```python
def strange_printer_turns_dp(target: str) -> int:
    if type(target) is not str:
        raise TypeError("target must be a string")
    if not 1 <= len(target) <= 100:
        raise ValueError("target length must be between 1 and 100")
    if any(not "a" <= character <= "z" for character in target):
        raise ValueError("target must contain only lowercase ASCII letters")

    length = len(target)
    turns = [[0] * length for _ in range(length)]
    for left in range(length - 1, -1, -1):
        turns[left][left] = 1
        for right in range(left + 1, length):
            turns[left][right] = 1 + turns[left + 1][right]
            for matching in range(left + 1, right + 1):
                if target[matching] == target[left]:
                    middle = turns[left + 1][matching - 1] if matching > left + 1 else 0
                    turns[left][right] = min(
                        turns[left][right], middle + turns[matching][right]
                    )
    return turns[0][-1]
```

There are `O(n^2)` intervals and up to `O(n)` matching split positions per
interval, for `O(n^3)` time and `O(n^2)` space.

## Expert solution: remove equivalent adjacent states first

```python
def strange_printer_turns(target: str) -> int:
    if type(target) is not str:
        raise TypeError("target must be a string")
    if not 1 <= len(target) <= 100:
        raise ValueError("target length must be between 1 and 100")
    if any(not "a" <= character <= "z" for character in target):
        raise ValueError("target must contain only lowercase ASCII letters")

    compact = "".join(
        character
        for index, character in enumerate(target)
        if index == 0 or character != target[index - 1]
    )
    length = len(compact)
    turns = [[0] * length for _ in range(length)]
    for left in range(length - 1, -1, -1):
        turns[left][left] = 1
        for right in range(left + 1, length):
            turns[left][right] = 1 + turns[left + 1][right]
            for matching in range(left + 1, right + 1):
                if compact[matching] == compact[left]:
                    middle = turns[left + 1][matching - 1] if matching > left + 1 else 0
                    turns[left][right] = min(
                        turns[left][right], middle + turns[matching][right]
                    )
    return turns[0][-1]
```

Extending a print turn across adjacent equal target positions never adds a
turn, so run compression preserves the optimum and can sharply reduce the DP
dimension before applying the same proven recurrence.

**Complexity:** `O(m^3)` time and `O(m^2)` space after compression to `m <= n`
characters.
