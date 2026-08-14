# Focus300 142: LeetCode 887 - Super Egg Drop

**Source:** [LeetCode 887](https://leetcode.com/problems/super-egg-drop/)  
**Difficulty:** Hard  
**Pattern:** invert minimax DP into maximum covered floors

## Exact contract

There are `egg_count` identical eggs and a building with `floor_count` floors.
An unknown threshold `f` is between `0` and `floor_count`: an egg survives drops
at or below `f` and breaks above it. Return the minimum number of drops needed
to determine `f` in the worst case.

## First principles

Choosing a floor splits the uncertainty into a broken-egg interval below and a
surviving-egg interval above, producing a minimax recurrence. Invert the state:
with `m` moves and `e` eggs, one drop covers the current floor, the broken case
below with `e - 1` eggs, and the surviving case above with `e` eggs.

## Cases that decide correctness

- Zero floors require zero drops.
- One egg requires a linear bottom-up search.
- A broken egg cannot be reused; a surviving egg can.
- The answer minimizes the maximum of the two outcomes.
- Coverage is monotone in moves, so stop at the first move count covering all floors.

## Brute force: try every drop floor in every state

```python
def super_egg_drop_brute(egg_count: int, floor_count: int) -> int:
    if egg_count <= 0 or floor_count < 0:
        raise ValueError("egg_count must be positive and floor_count non-negative")
    if floor_count <= 1 or egg_count == 1:
        return floor_count

    previous = list(range(floor_count + 1))
    for _ in range(2, egg_count + 1):
        current = [0] * (floor_count + 1)
        for floors in range(1, floor_count + 1):
            current[floors] = 1 + min(
                max(previous[drop - 1], current[floors - drop])
                for drop in range(1, floors + 1)
            )
        previous = current
    return previous[floor_count]
```

This direct minimax table takes `O(k n^2)` time and `O(n)` space.

## Better transition: ask what a fixed number of moves can cover

Let `covered[e]` be the maximum floors distinguishable with the current number
of moves and `e` eggs. One new move gives
`covered[e] = old_covered[e] + old_covered[e - 1] + 1`.

## Expert solution: grow move coverage

```python
def super_egg_drop(egg_count: int, floor_count: int) -> int:
    if egg_count <= 0 or floor_count < 0:
        raise ValueError("egg_count must be positive and floor_count non-negative")

    covered = [0] * (egg_count + 1)
    moves = 0
    while covered[egg_count] < floor_count:
        moves += 1
        for eggs in range(egg_count, 0, -1):
            covered[eggs] = covered[eggs] + covered[eggs - 1] + 1
    return moves
```

Descending egg order preserves the previous move's `covered[e - 1]`. The first
move count whose coverage reaches `floor_count` is minimal by monotonicity.

**Complexity:** `O(k * answer)` time and `O(k)` space.
