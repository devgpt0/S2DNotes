# Focus300 111: LeetCode 765 - Couples Holding Hands

**Source:** [LeetCode 765](https://leetcode.com/problems/couples-holding-hands/)  
**Difficulty:** Hard  
**Pattern:** greedy swap with inverse positions

## Exact contract

`row` is an even-length permutation of `0..len(row)-1`. People `2c` and
`2c + 1` form couple `c`, and seats are paired as `(0, 1), (2, 3), ...`.
Return the minimum number of swaps of any two people needed to seat every
couple together. The source allows 2 through 60 people.

## First principles

The partner of person `x` is `x ^ 1`. At the first incorrect seat pair, the
first person must eventually be paired with that unique partner. Swapping the
current second person with the partner fixes this pair in one move without
disturbing any earlier fixed pair. No solution can fix the pair in zero moves.

## Cases that decide correctness

- An already paired row needs zero swaps.
- Couple labels are defined by adjacent numbers, not current positions.
- Swapping can involve any two seats, not only neighboring seats.
- After a swap, both affected entries in the inverse-position table change.
- Duplicate, missing, or out-of-range people violate the permutation contract.

## Brute force: breadth-first search over permutations

```python
from collections import deque


def minimum_couple_swaps_brute(row: list[int]) -> int:
    if type(row) is not list or any(type(person) is not int for person in row):
        raise TypeError("row must be a list of integers")
    if not 2 <= len(row) <= 60 or len(row) % 2:
        raise ValueError("row must contain an even number of 2..60 people")
    if set(row) != set(range(len(row))):
        raise ValueError("row must be a permutation of 0..len(row)-1")

    start = tuple(row)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        seating, swaps = queue.popleft()
        if all(
            seating[index] ^ 1 == seating[index + 1] for index in range(0, len(row), 2)
        ):
            return swaps
        for first in range(len(row)):
            for second in range(first + 1, len(row)):
                next_seating = list(seating)
                next_seating[first], next_seating[second] = (
                    next_seating[second],
                    next_seating[first],
                )
                state = tuple(next_seating)
                if state not in seen:
                    seen.add(state)
                    queue.append((state, swaps + 1))
    raise RuntimeError("a valid permutation must be solvable")
```

This exact search has up to `(2n)!` states and `O(n^2)` swaps per state.

## Better approach: count connected couple components

Treat each couple as a graph vertex and each adjacent seat pair as an edge
between the two couples occupying it. A component containing `k` couples needs
`k - 1` swaps, so a disjoint-set solution returns `couples - components`.
The direct greedy construction below is shorter and also realizes the swaps.

## Expert solution: place each missing partner directly

```python
def minimum_couple_swaps(row: list[int]) -> int:
    if type(row) is not list or any(type(person) is not int for person in row):
        raise TypeError("row must be a list of integers")
    if not 2 <= len(row) <= 60 or len(row) % 2:
        raise ValueError("row must contain an even number of 2..60 people")
    if set(row) != set(range(len(row))):
        raise ValueError("row must be a permutation of 0..len(row)-1")

    seating = row.copy()
    position = [0] * len(seating)
    for seat, person in enumerate(seating):
        position[person] = seat

    swaps = 0
    for first_seat in range(0, len(seating), 2):
        second_seat = first_seat + 1
        partner = seating[first_seat] ^ 1
        if seating[second_seat] == partner:
            continue

        partner_seat = position[partner]
        displaced = seating[second_seat]
        seating[second_seat], seating[partner_seat] = (
            seating[partner_seat],
            seating[second_seat],
        )
        position[partner] = second_seat
        position[displaced] = partner_seat
        swaps += 1
    return swaps
```

Each incorrect pair has a one-swap lower bound, and the greedy step meets that
bound while permanently fixing the pair. The sum of these forced steps is
therefore globally minimal.

**Complexity:** `O(n)` time and `O(n)` space for `n` people.
