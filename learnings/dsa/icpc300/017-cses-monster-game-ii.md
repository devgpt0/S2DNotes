# ICPC300 017: CSES - Monster Game II

**Source:** [CSES - Monster Game II](https://cses.fi/problemset/task/2085/)  
**Pattern:** dynamic programming optimized by a Li Chao tree  
**Goal:** Evaluate the source recurrence for arbitrary strength and cost-factor
orders fast enough for all `n` monsters.

## 1. Problem in plain words

Let monster `i` have strength `s[i]` and cost factor `f[i]`. State `0` has
cost `dp[0] = 0` and factor `f[0] = x`, the initial factor. For `i >= 1`:

`dp[i] = min(dp[j] + s[i] * f[j])` over `0 <= j < i`.

The required answer is `dp[n]`. The input order is significant, and Monster
Game II does not provide the monotone ordering that makes the simpler deque
convex-hull trick safe.

## 2. First principles

For a fixed earlier state `j`, the transition as a function of current strength
`z` is a line:

`y = f[j] * z + dp[j]`.

Before processing monster `i`, insert all lines for states `0..i-1`. Query the
minimum line value at `z = s[i]` to obtain `dp[i]`, then insert the new line
with slope `f[i]` and intercept `dp[i]`.

Thus the DP is exactly an online sequence of line insertions and minimum
queries. A Li Chao tree supports both with no slope or query-order assumption.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| One monster | Answer `x * s[0]`. |
| Equal slopes | Keep the line with the smaller intercept. |
| Equal strengths | Query the same coordinate correctly more than once. |
| Slopes in arbitrary order | Do not use a monotone deque assumption. |
| A line useful only far left or right | Li Chao insertion must keep it on that side. |

## 4. Brute force: test every previous state

```python
def minimum_monster_cost_brute_force(
    strengths: list[int], cost_factors: list[int], initial_factor: int
) -> int:
    if len(strengths) != len(cost_factors) or not strengths:
        raise ValueError("strengths and cost factors must have equal positive length")

    dp = [0] * len(strengths)
    for monster, strength in enumerate(strengths):
        best = initial_factor * strength
        for previous in range(monster):
            best = min(
                best,
                dp[previous] + cost_factors[previous] * strength,
            )
        dp[monster] = best
    return dp[-1]
```

**Why it works:** the inner loop evaluates every legal predecessor `j`,
including the initial state through `initial_factor * strength`.

**Complexity:** `O(n^2)` time and `O(n)` memory.

## 5. Better approach: why the monotone deque shortcut is invalid here

A deque hull can answer increasing query coordinates when lines also arrive in
sorted slope order. Monster Game II allows both arrays in arbitrary order.
Sorting either array would change the DP's `j < i` rule, so it would solve a
different problem.

The quadratic recurrence is the useful oracle; the next generally correct
step is a dynamic hull such as Li Chao. This is a genuine case where inventing
a cosmetic middle solution would hide an invalid assumption.

## 6. Expert solution: coordinate-compressed Li Chao tree

Queries occur only at the given strengths, so tree intervals contain sorted
distinct query coordinates instead of the entire numeric range. At each node,
store the line better at the middle coordinate. Two lines cross at most once,
so the losing line can still matter on at most one child interval.

```python
Line = tuple[int, int]


def minimum_monster_cost(
    strengths: list[int], cost_factors: list[int], initial_factor: int
) -> int:
    if len(strengths) != len(cost_factors) or not strengths:
        raise ValueError("strengths and cost factors must have equal positive length")

    coordinates = sorted(set(strengths))
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    tree: list[Line | None] = [None] * (4 * len(coordinates))

    def evaluate(line: Line, coordinate: int) -> int:
        slope, intercept = line
        return slope * coordinate + intercept

    def add_line(
        new_line: Line,
        node: int = 1,
        left: int = 0,
        right: int | None = None,
    ) -> None:
        if right is None:
            right = len(coordinates) - 1
        current = tree[node]
        if current is None:
            tree[node] = new_line
            return

        middle = (left + right) // 2
        middle_coordinate = coordinates[middle]
        if evaluate(new_line, middle_coordinate) < evaluate(current, middle_coordinate):
            tree[node], new_line = new_line, current

        if left == right:
            return

        stored = tree[node]
        if stored is None:
            raise RuntimeError("Li Chao node unexpectedly has no line")
        if evaluate(new_line, coordinates[left]) < evaluate(stored, coordinates[left]):
            add_line(new_line, 2 * node, left, middle)
        elif evaluate(new_line, coordinates[right]) < evaluate(
            stored, coordinates[right]
        ):
            add_line(new_line, 2 * node + 1, middle + 1, right)

    def query(coordinate: int) -> int:
        index = coordinate_index[coordinate]
        node = 1
        left = 0
        right = len(coordinates) - 1
        best: int | None = None

        while True:
            line = tree[node]
            if line is not None:
                value = evaluate(line, coordinate)
                best = value if best is None else min(best, value)
            if left == right:
                break
            middle = (left + right) // 2
            if index <= middle:
                node = 2 * node
                right = middle
            else:
                node = 2 * node + 1
                left = middle + 1

        if best is None:
            raise RuntimeError("cannot query an empty Li Chao tree")
        return best

    add_line((initial_factor, 0))
    answer = 0
    for strength, cost_factor in zip(strengths, cost_factors, strict=True):
        answer = query(strength)
        add_line((cost_factor, answer))
    return answer
```

### Why the expert code is correct

- Every legal predecessor becomes one line before it can be queried.
- A query takes the minimum among the lines stored along its root-to-leaf path.
- At an insertion node, the line better at the midpoint stays there. Since two
  lines cross once at most, the other line can beat it on at most one side and
  is recursively stored on exactly that relevant side.
- Therefore every query equals the original DP minimum, and inserted
  intercepts are the correct earlier `dp` values.

**Complexity:** `O(n log n)` time and `O(n)` memory.

## 7. What to remember

Read `dp[j] + x * f[j]` as a line with slope `f[j]` and intercept `dp[j]`.
When slopes and queries are not monotone, use a hull that does not assume they
are.
