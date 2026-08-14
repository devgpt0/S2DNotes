# ICPC300 259: Codeforces 149D - Coloring Brackets

**Source:** [Codeforces 149D - Coloring Brackets](https://codeforces.com/problemset/problem/149/D)  
**Rating:** 2200  
**Pattern:** balanced-interval DP with boundary colors  
**Goal:** Color brackets red, blue, or uncolored so exactly one bracket in each
matching pair is colored and adjacent brackets never share the same nonzero
color. Count colorings modulo `1_000_000_007`.

## 1. First principles

A balanced interval is either one matched outer pair around a balanced interior,
or the concatenation of two balanced intervals.

For each interval store a `3 x 3` table indexed by the colors of its first and
last bracket (`0` uncolored, `1` red, `2` blue). Boundary colors are sufficient
to enforce adjacency when wrapping or concatenating intervals.

## 2. Cases that decide correctness

- Exactly one endpoint of every matching pair is colored.
- The colored endpoint may use either red or blue.
- Adjacent equal colors are forbidden only when the color is nonzero.
- Nested and consecutive balanced components use different transitions.
- The input must be a nonempty balanced parenthesis string.

## 3. Brute force: enumerate all three-color assignments

```python
from itertools import product


MODULO = 1_000_000_007


def bracket_coloring_count_brute(brackets: str) -> int:
    if not brackets or any(character not in "()" for character in brackets):
        raise ValueError("brackets must contain parentheses")
    matching = [-1] * len(brackets)
    stack: list[int] = []
    for index, character in enumerate(brackets):
        if character == "(":
            stack.append(index)
        elif not stack:
            raise ValueError("brackets must be balanced")
        else:
            opening = stack.pop()
            matching[opening] = index
            matching[index] = opening
    if stack:
        raise ValueError("brackets must be balanced")

    answer = 0
    for colors in product(range(3), repeat=len(brackets)):
        if any(
            (colors[opening] == 0) == (colors[closing] == 0)
            for opening, closing in enumerate(matching)
            if opening < closing
        ):
            continue
        if any(
            colors[index] != 0 and colors[index] == colors[index + 1]
            for index in range(len(brackets) - 1)
        ):
            continue
        answer += 1
    return answer % MODULO
```

**Complexity:** `O(3^n * n)` time and `O(n)` space.

## 4. Better transition: expose only interval boundary colors

All matching-pair constraints are local to a wrapped interval. Once its inside
is valid, the outside world can interact only with its first and last bracket,
so nine boundary states fully describe a component.

## 5. Expert solution: recursive interval composition

```python
from functools import lru_cache


MODULO = 1_000_000_007


def bracket_coloring_count(brackets: str) -> int:
    if not brackets or any(character not in "()" for character in brackets):
        raise ValueError("brackets must contain parentheses")
    matching = [-1] * len(brackets)
    stack: list[int] = []
    for index, character in enumerate(brackets):
        if character == "(":
            stack.append(index)
        elif not stack:
            raise ValueError("brackets must be balanced")
        else:
            opening = stack.pop()
            matching[opening] = index
            matching[index] = opening
    if stack:
        raise ValueError("brackets must be balanced")

    @lru_cache(maxsize=None)
    def solve(left: int, right: int) -> tuple[tuple[int, ...], ...]:
        result = [[0] * 3 for _ in range(3)]
        closing = matching[left]
        if closing == right:
            if left + 1 == right:
                interior = ((1, 0, 0), (0, 0, 0), (0, 0, 0))
            else:
                interior = solve(left + 1, right - 1)
            for first_color in range(3):
                for last_color in range(3):
                    count = interior[first_color][last_color]
                    if count == 0:
                        continue
                    for color in (1, 2):
                        if first_color == 0 or first_color != color:
                            result[color][0] += count
                        if last_color == 0 or last_color != color:
                            result[0][color] += count
            return tuple(tuple(value % MODULO for value in row) for row in result)

        first_part = solve(left, closing)
        second_part = solve(closing + 1, right)
        for first_color in range(3):
            for first_last in range(3):
                first_count = first_part[first_color][first_last]
                if first_count == 0:
                    continue
                for second_first in range(3):
                    if first_last != 0 and first_last == second_first:
                        continue
                    for last_color in range(3):
                        result[first_color][last_color] += (
                            first_count * second_part[second_first][last_color]
                        )
        return tuple(tuple(value % MODULO for value in row) for row in result)

    return sum(map(sum, solve(0, len(brackets) - 1))) % MODULO
```

### Why the expert code is correct

For a wrapped pair, the transition colors exactly one outer endpoint and checks
its sole interior adjacency. For concatenation, both subintervals are already
valid and only their touching boundary colors need checking. The unique balanced
decomposition applies one of these exhaustive transitions at every interval,
so all valid colorings are counted once.

**Complexity:** `O(n)` interval states with constant transition work and `O(n)`
cache space.

## 6. What to remember

```text
balanced string -> wrapped pair or concatenation
outside interaction -> first and last colors only
nine boundary states -> enforce all adjacency constraints
```
