# ICPC300 092: CSES - Stick Game

**Source:** [CSES - Stick Game](https://cses.fi/problemset/task/1729/)  
**Pattern:** impartial-game winning-state DP

## Exact contract

Input gives a maximum pile size `n`, a count `k`, and `k` allowed positive move
sizes. For every initial size from `1` through `n`, output `W` if the first
player wins under optimal play and `L` otherwise. A move removes one allowed
number of sticks, and a player with no legal move loses.

## First principles

A position is winning exactly when at least one legal move reaches a losing
position. It is losing when every legal move reaches a winning position. Size
zero is losing, so increasing sizes can be computed left to right.

## Cases that decide correctness

- Move sizes larger than the current pile are illegal.
- Size zero is an internal base state but is not printed.
- Duplicate move sizes do not change the game.
- Output contains exactly `n` characters with no separators.

## Brute force: expand the game tree independently

```python
def stick_game_brute(maximum_size: int, moves: list[int]) -> str:
    def winning(sticks: int) -> bool:
        return any(move <= sticks and not winning(sticks - move) for move in moves)

    return "".join(
        "W" if winning(sticks) else "L" for sticks in range(1, maximum_size + 1)
    )
```

Repeated subgames make this exponential.

## Better: memoized recursive states

```python
from functools import cache


def stick_game_memo(maximum_size: int, moves: list[int]) -> str:
    unique_moves = tuple(sorted(set(moves)))

    @cache
    def winning(sticks: int) -> bool:
        return any(
            move <= sticks and not winning(sticks - move) for move in unique_moves
        )

    return "".join(
        "W" if winning(sticks) else "L" for sticks in range(1, maximum_size + 1)
    )
```

This takes `O(nk)` time but recursion can reach `n` and cached Python objects
add avoidable memory overhead.

## Expert solution: iterative byte-array DP

```python
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    maximum_size, move_count = data[0:2]
    moves = sorted(set(data[2 : 2 + move_count]))
    winning = bytearray(maximum_size + 1)

    for sticks in range(1, maximum_size + 1):
        for move in moves:
            if move > sticks:
                break
            if not winning[sticks - move]:
                winning[sticks] = 1
                break

    print(
        "".join(
            "W" if winning[sticks] else "L" for sticks in range(1, maximum_size + 1)
        )
    )


if __name__ == "__main__":
    solve()
```

All transitions point to smaller piles already computed. The first transition
to a losing state proves a win; if none exists, the state is losing.

**Complexity:** `O(nk)` worst-case time and `O(n)` compact space.

