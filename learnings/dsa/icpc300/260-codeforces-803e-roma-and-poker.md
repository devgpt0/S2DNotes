# ICPC300 260: Codeforces 803E - Roma and Poker

**Source:** [Codeforces 803E - Roma and Poker](https://codeforces.com/problemset/problem/803/E)  
**Rating:** 2200  
**Pattern:** bounded score DP with parent reconstruction  
**Goal:** Replace every `?` with win `W`, draw `D`, or loss `L`. Score changes
by `+1`, `0`, or `-1`; its absolute value must stay below `limit` before the
last game and equal `limit` after the last game. Return one completion or
`None`.

## 1. First principles

After a prefix, only its current score affects future feasibility. Keep every
reachable score in `[-limit, limit]` and record one predecessor.

For all non-final positions reject scores with absolute value at least the
limit. At the final position retain only `+limit` and `-limit`, then follow
parent pointers backward to reconstruct the outcomes.

## 2. Cases that decide correctness

- A fixed `W`, `D`, or `L` cannot be changed.
- Reaching either boundary before the final game is invalid.
- The final score may be either positive or negative limit.
- Draws preserve the score but still consume one game.
- Every question mark must receive exactly one outcome.

## 3. Brute force: enumerate all question-mark replacements

```python
from itertools import product


def poker_completion_brute(outcomes: str, limit: int) -> str | None:
    if (
        not outcomes
        or limit <= 0
        or any(character not in "WDL?" for character in outcomes)
    ):
        raise ValueError("invalid outcomes or limit")

    unknown = [index for index, character in enumerate(outcomes) if character == "?"]
    change = {"W": 1, "D": 0, "L": -1}
    for replacements in product("WDL", repeat=len(unknown)):
        completed = list(outcomes)
        for index, character in zip(unknown, replacements):
            completed[index] = character
        score = 0
        valid = True
        for index, character in enumerate(completed):
            score += change[character]
            if index + 1 < len(completed) and abs(score) >= limit:
                valid = False
                break
        if valid and abs(score) == limit:
            return "".join(completed)
    return None
```

**Complexity:** `O(3^unknown * n)` time and `O(n)` space.

## 4. Better transition: merge prefixes with equal scores

All prefixes ending at the same score have identical possible futures, so one
representative parent is enough. This reduces exponential outcome histories to
at most `2 * limit + 1` scores per position.

## 5. Expert solution: reachable-score DP and backtracking

```python
def poker_completion(outcomes: str, limit: int) -> str | None:
    if (
        not outcomes
        or limit <= 0
        or any(character not in "WDL?" for character in outcomes)
    ):
        raise ValueError("invalid outcomes or limit")

    change = {"W": 1, "D": 0, "L": -1}
    reachable = {0}
    parents: list[dict[int, tuple[int, str]]] = [{}]
    for position, given in enumerate(outcomes, start=1):
        choices = "WDL" if given == "?" else given
        next_parents: dict[int, tuple[int, str]] = {}
        for previous_score in reachable:
            for character in choices:
                score = previous_score + change[character]
                if position < len(outcomes):
                    if abs(score) >= limit:
                        continue
                elif abs(score) != limit:
                    continue
                next_parents.setdefault(score, (previous_score, character))
        parents.append(next_parents)
        reachable = set(next_parents)
        if not reachable:
            return None

    score = limit if limit in reachable else -limit
    completed = [""] * len(outcomes)
    for position in range(len(outcomes), 0, -1):
        previous_score, character = parents[position][score]
        completed[position - 1] = character
        score = previous_score
    return "".join(completed)
```

### Why the expert code is correct

The DP tries every allowed outcome from every reachable prefix score and applies
the source's boundary rule at exactly the correct position. Equal-score
prefixes have identical continuations, so retaining one parent loses no
feasible completion. A final boundary state exists exactly when a valid string
exists, and its parent chain reconstructs one.

**Complexity:** `O(n * limit)` time and `O(n * limit)` reconstruction space.

## 6. What to remember

```text
game prefix -> current score is sufficient state
boundary allowed -> only after final game
need one witness -> store one parent per reachable score
```
