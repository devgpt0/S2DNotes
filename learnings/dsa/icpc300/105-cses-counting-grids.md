# ICPC300 105: CSES - Counting Grids

**Source:** [CSES - Counting Grids](https://cses.fi/problemset/task/2210/)  
**Pattern:** Burnside's lemma for quarter-turn rotations  
**Goal:** Count, modulo `1_000_000_007`, binary `n x n` grids where grids that
differ only by rotations of `0`, `90`, `180`, or `270` degrees are equivalent.

## 1. Problem in plain words

There are `2^(n^2)` labeled binary grids. Each rotational equivalence class can
have one, two, or four labeled grids depending on its symmetry, so dividing by
four directly is incorrect.

Burnside averages how many grids each of the four rotations leaves unchanged.

## 2. First principles

A grid fixed by a rotation must give one value to every coordinate cycle of
that rotation. If a rotation has `c` cycles, it fixes `2^c` grids.

- identity: `n^2` one-cell cycles;
- 180 degrees: `(n^2)/2` cycles for even `n`, `(n^2+1)/2` for odd `n`;
- 90 or 270 degrees: `n^2/4` cycles for even `n`, `(n^2+3)/4` for odd `n`.

Average their fixed-grid counts by multiplying the sum by the inverse of four.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| `n = 1` | Two grids. |
| Odd `n` | The center cell is fixed by every rotation. |
| Even `n` | Quarter-turn cycles all have size four. |
| Grid fixed by 180 but not 90 degrees | Its orbit has size two and Burnside handles it. |
| Modular average | Divide with inverse `4`, not integer truncation after reduction. |

## 4. Brute force: canonicalize every binary grid

```python
def count_rotation_classes_brute_force(size: int) -> int:
    if size < 1:
        raise ValueError("grid size must be positive")

    def rotate(grid: tuple[int, ...]) -> tuple[int, ...]:
        result = [0] * (size * size)
        for row in range(size):
            for column in range(size):
                result[column * size + (size - 1 - row)] = grid[row * size + column]
        return tuple(result)

    classes: set[tuple[int, ...]] = set()
    for mask in range(1 << (size * size)):
        grid = tuple((mask >> index) & 1 for index in range(size * size))
        rotations = [grid]
        for _ in range(3):
            rotations.append(rotate(rotations[-1]))
        classes.add(min(rotations))
    return len(classes)
```

**Complexity:** `O(2^(n^2) n^2)` time and exponential memory.

## 5. Better: count coordinate cycles directly

This generic Burnside implementation constructs each rotation permutation and
counts its cycles. It is already polynomial but still touches every cell for
all four rotations.

```python
MODULO = 1_000_000_007


def count_rotation_classes_by_cycles(size: int) -> int:
    if size < 1:
        raise ValueError("grid size must be positive")

    def rotate_index(index: int, turns: int) -> int:
        row, column = divmod(index, size)
        for _ in range(turns):
            row, column = column, size - 1 - row
        return row * size + column

    fixed_sum = 0
    for turns in range(4):
        seen = [False] * (size * size)
        cycle_count = 0
        for start in range(size * size):
            if seen[start]:
                continue
            cycle_count += 1
            position = start
            while not seen[position]:
                seen[position] = True
                position = rotate_index(position, turns)
        fixed_sum += pow(2, cycle_count, MODULO)
    return fixed_sum % MODULO * pow(4, MODULO - 2, MODULO) % MODULO
```

**Complexity:** `O(n^2)` time and `O(n^2)` memory.

## 6. Expert solution: closed-form cycle counts

```python
MODULO = 1_000_000_007


def count_rotation_classes(size: int) -> int:
    if size < 1:
        raise ValueError("grid size must be positive")

    cells = size * size
    identity_cycles = cells
    half_turn_cycles = (cells + size % 2) // 2
    quarter_turn_cycles = (cells + 3 * (size % 2)) // 4

    fixed_sum = (
        pow(2, identity_cycles, MODULO)
        + pow(2, half_turn_cycles, MODULO)
        + 2 * pow(2, quarter_turn_cycles, MODULO)
    ) % MODULO
    return fixed_sum * pow(4, MODULO - 2, MODULO) % MODULO
```

### Why the expert code is correct

- A fixed grid is constant on every coordinate orbit, giving two choices per
  orbit.
- The identity, half-turn, and quarter-turn formulas count those orbits,
  including the single fixed center exactly when `n` is odd.
- The 90- and 270-degree rotations have equal cycle counts, hence the factor
  two.
- Burnside's average over all four rotations counts rotational classes once.

**Complexity:** `O(log(n^2))` modular-exponentiation time and `O(1)` memory.

## 7. What to remember

For binary grids up to rotation, count coordinate cycles under each of four
group elements, raise two to those counts, and average.
