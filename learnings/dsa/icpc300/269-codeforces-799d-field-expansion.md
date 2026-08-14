# ICPC300 269: Codeforces 799D - Field expansion

**Source:** [Codeforces 799D - Field expansion](https://codeforces.com/problemset/problem/799/D)  
**Rating:** 2300  
**Pattern:** largest multipliers plus a Pareto frontier  
**Goal:** Make a rectangle at least as large as a target rectangle, allowing a
rotation. Each supplied multiplier may multiply exactly one side at most once.
Return the minimum number used, or `-1` if impossible.

## 1. First principles

For a fixed orientation, cap each side at its target because larger dimensions
are equivalent. After each multiplier, retain only nondominated states: state
`(x1, y1)` dominates `(x2, y2)` when both coordinates are at least as large.

For a solution using `t` factors, replacing them by the `t` largest factors
cannot hurt. Multipliers equal to one never help. A dynamic doubling bound also
shows that only a small largest prefix can participate in a minimum solution.

## 2. Cases that decide correctness

- The initial rectangle may already fit, giving zero.
- Either orientation of the target must be tried.
- A multiplier belongs to only one side.
- Dimensions are capped before frontier deduplication.
- Factors equal to one are safely discarded.

## 3. Brute force: enumerate subsets and side assignments

```python
from itertools import combinations


def minimum_expansions_brute(
    target_height: int,
    target_width: int,
    initial_height: int,
    initial_width: int,
    multipliers: list[int],
) -> int:
    dimensions = (target_height, target_width, initial_height, initial_width)
    if any(type(value) is not int or value <= 0 for value in dimensions) or any(
        type(value) is not int or value <= 0 for value in multipliers
    ):
        raise ValueError("dimensions and multipliers must be positive integers")

    def fits(height: int, width: int) -> bool:
        return (height >= target_height and width >= target_width) or (
            height >= target_width and width >= target_height
        )

    for used_count in range(len(multipliers) + 1):
        for chosen in combinations(range(len(multipliers)), used_count):
            for side_mask in range(1 << used_count):
                height = initial_height
                width = initial_width
                for offset, index in enumerate(chosen):
                    if side_mask >> offset & 1:
                        height *= multipliers[index]
                    else:
                        width *= multipliers[index]
                if fits(height, width):
                    return used_count
    return -1
```

**Complexity:** `O(3^n n)` time and `O(n)` enumeration space.

## 4. Better approach: capped state DP

Keeping every capped `(height, width)` state removes subset enumeration, but
many states are weaker than another state reached with the same number of
factors. Pruning them is the difference between a large table and a small
frontier.

## 5. Expert solution: two orientations and Pareto pruning

```python
def minimum_expansions(
    target_height: int,
    target_width: int,
    initial_height: int,
    initial_width: int,
    multipliers: list[int],
) -> int:
    dimensions = (target_height, target_width, initial_height, initial_width)
    if any(type(value) is not int or value <= 0 for value in dimensions) or any(
        type(value) is not int or value <= 0 for value in multipliers
    ):
        raise ValueError("dimensions and multipliers must be positive integers")
    useful = sorted((value for value in multipliers if value > 1), reverse=True)

    def solve_orientation(target_x: int, target_y: int) -> int | None:
        start_x = min(initial_height, target_x)
        start_y = min(initial_width, target_y)
        if start_x == target_x and start_y == target_y:
            return 0

        def doubling_steps(start: int, target: int) -> int:
            ratio = (target + start - 1) // start
            return (ratio - 1).bit_length()

        limit = doubling_steps(start_x, target_x) + doubling_steps(start_y, target_y)
        factors = useful[:limit]
        states = {(start_x, start_y)}
        for used_count, factor in enumerate(factors, start=1):
            candidates: set[tuple[int, int]] = set()
            for current_x, current_y in states:
                candidates.add((min(target_x, current_x * factor), current_y))
                candidates.add((current_x, min(target_y, current_y * factor)))
            if (target_x, target_y) in candidates:
                return used_count

            best_y = -1
            states = set()
            for current_x, current_y in sorted(candidates, reverse=True):
                if current_y > best_y:
                    states.add((current_x, current_y))
                    best_y = current_y
        return None

    answers = [
        answer
        for answer in (
            solve_orientation(target_height, target_width),
            solve_orientation(target_width, target_height),
        )
        if answer is not None
    ]
    return min(answers, default=-1)
```

### Why the expert code is correct

For each used-count prefix, the DP tries assigning every selected multiplier to
either side. Largest-factor replacement proves that only the sorted prefix is
needed, and dominance pruning discards no state that could lead to a better
future result. Trying both target orientations covers rotation.

**Complexity:** `O(L S log S)` time and `O(S)` space, where `L` is the dynamic
doubling bound and `S` is the maximum Pareto-frontier size.

## 6. What to remember

```text
minimum factors -> try largest factors first
cap dimensions -> finite state space
discard coordinate-wise weaker states -> Pareto frontier
```
