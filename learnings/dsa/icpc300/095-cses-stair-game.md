# ICPC300 095: CSES - Stair Game

**Source:** [CSES - Stair Game](https://cses.fi/problemset/task/1099/)  
**Pattern:** staircase game reduced to Nim

## Exact contract

Input gives `t` games. A game has `n` stairs and a number of balls on each
stair. A move chooses a positive number of balls from one stair and moves them
one stair down; balls moved down from stair `1` leave the staircase. The player
unable to move loses. Output `first` or `second` for each game.

## First principles

Pair stairs `(1,2)`, `(3,4)`, and so on. Balls on an even stair can be answered
by moving the same amount from the odd stair immediately below it; they do not
contribute to the Nim value. Balls on odd one-based stairs behave as independent
Nim heaps. The position is losing exactly when their xor is zero.

## Cases that decide correctness

- Stair `1` is included in the xor.
- The final even stair of an even-length staircase is excluded.
- A move may transfer any positive number, not just one ball.
- Zero-ball stairs contribute nothing.

## Brute force: expand every legal transfer

```python
def stair_game_first_wins_brute(stairs: tuple[int, ...]) -> bool:
    if not any(stairs):
        return False
    for stair, ball_count in enumerate(stairs):
        for moved in range(1, ball_count + 1):
            next_stairs = list(stairs)
            next_stairs[stair] -= moved
            if stair > 0:
                next_stairs[stair - 1] += moved
            if not stair_game_first_wins_brute(tuple(next_stairs)):
                return True
    return False
```

The decreasing weighted height guarantees termination, but the tree is
exponential.

## Better: memoize small staircase states

```python
from functools import cache


def stair_game_first_wins_memo(stairs: tuple[int, ...]) -> bool:
    @cache
    def winning(state: tuple[int, ...]) -> bool:
        for stair, ball_count in enumerate(state):
            for moved in range(1, ball_count + 1):
                next_state = list(state)
                next_state[stair] -= moved
                if stair > 0:
                    next_state[stair - 1] += moved
                if not winning(tuple(next_state)):
                    return True
        return False

    return winning(stairs)
```

Memoization removes duplicate states but their count still grows rapidly with
balls and stairs.

## Expert solution: xor odd-numbered stairs

```python
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    test_count = data[0]
    offset = 1
    answers = []

    for _ in range(test_count):
        stair_count = data[offset]
        offset += 1
        nim_sum = 0
        for stair, ball_count in enumerate(data[offset : offset + stair_count]):
            if stair % 2 == 0:
                nim_sum ^= ball_count
        offset += stair_count
        answers.append("first" if nim_sum else "second")
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

The staircase's Sprague-Grundy value equals the xor on odd one-based stairs.
Thus the standard Nim zero/nonzero outcome rule applies directly.

**Complexity:** `O(total stairs)` time and `O(1)` extra space.

