# ICPC300 155: Codeforces 321E - Ciel and Gondolas

**Source:** [Codeforces 321E - Ciel and Gondolas](https://codeforces.com/problemset/problem/321/E)  
**Rating:** 2500  
**Pattern:** divide-and-conquer optimization for partition DP  
**Goal:** Split people, in their fixed order, into exactly `group_count`
nonempty contiguous gondolas. Minimize the sum of pairwise unfamiliarity inside
each gondola; the input matrix is symmetric and has a zero diagonal.

## 1. First principles

Let `cost[left][right]` be the sum of matrix entries for unordered pairs inside
that interval. The ordinary partition recurrence is

```text
dp[g][right] = min(dp[g-1][cut] + cost[cut][right-1])
```

For interval pair costs, optimal cuts are monotone as `right` increases. A
divide-and-conquer layer searches only the cut interval inherited from its
neighbors.

## 2. Cases that decide correctness

- Every group is nonempty, so layer `g` starts at prefix length `g`.
- Each unordered pair is charged once, not twice from the symmetric matrix.
- `group_count = n` has cost zero.
- The matrix must be square, symmetric, nonnegative, and zero on its diagonal.
- Exactly `group_count` gondolas are required.

## 3. Brute force: enumerate every cut set

```python
from itertools import combinations


def gondola_cost_brute(unfamiliarity: list[list[int]], group_count: int) -> int:
    size = len(unfamiliarity)
    if not 1 <= group_count <= size:
        raise ValueError("group_count must be between one and matrix size")
    if any(len(row) != size for row in unfamiliarity):
        raise ValueError("matrix must be square")
    for first in range(size):
        if unfamiliarity[first][first] != 0:
            raise ValueError("matrix diagonal must be zero")
        for second in range(size):
            if (
                unfamiliarity[first][second] < 0
                or unfamiliarity[first][second] != unfamiliarity[second][first]
            ):
                raise ValueError("matrix must be nonnegative and symmetric")

    def interval_cost(left: int, right: int) -> int:
        return sum(
            unfamiliarity[first][second]
            for first in range(left, right)
            for second in range(first + 1, right)
        )

    answer: int | None = None
    for cuts in combinations(range(1, size), group_count - 1):
        boundaries = (0, *cuts, size)
        total = sum(
            interval_cost(boundaries[index], boundaries[index + 1])
            for index in range(group_count)
        )
        answer = total if answer is None else min(answer, total)
    if answer is None:
        raise RuntimeError("no valid partition")
    return answer
```

**Complexity:** `O(C(n-1,k-1) * n^2)` time and `O(k)` space.

## 4. Better: quadratic transition DP

```python
def gondola_cost_quadratic(unfamiliarity: list[list[int]], group_count: int) -> int:
    size = len(unfamiliarity)
    if not 1 <= group_count <= size:
        raise ValueError("group_count must be between one and matrix size")
    if any(len(row) != size for row in unfamiliarity):
        raise ValueError("matrix must be square")
    for first in range(size):
        if unfamiliarity[first][first] != 0:
            raise ValueError("matrix diagonal must be zero")
        for second in range(size):
            if (
                unfamiliarity[first][second] < 0
                or unfamiliarity[first][second] != unfamiliarity[second][first]
            ):
                raise ValueError("matrix must be nonnegative and symmetric")

    cost = [[0] * size for _ in range(size)]
    for right in range(size):
        running = 0
        for left in range(right - 1, -1, -1):
            running += unfamiliarity[left][right]
            cost[left][right] = cost[left][right - 1] + running

    infinity = 10**30
    previous = [0] + [infinity] * size
    for groups in range(1, group_count + 1):
        current = [infinity] * (size + 1)
        for right in range(groups, size + 1):
            current[right] = min(
                previous[cut] + cost[cut][right - 1] for cut in range(groups - 1, right)
            )
        previous = current
    return previous[size]
```

**Complexity:** `O(n^2 + k n^2)` time and `O(n^2)` space.

## 5. Expert solution: monotone divide-and-conquer layers

```python
def gondola_cost_divide_conquer(
    unfamiliarity: list[list[int]], group_count: int
) -> int:
    size = len(unfamiliarity)
    if not 1 <= group_count <= size:
        raise ValueError("group_count must be between one and matrix size")
    if any(len(row) != size for row in unfamiliarity):
        raise ValueError("matrix must be square")
    for first in range(size):
        if unfamiliarity[first][first] != 0:
            raise ValueError("matrix diagonal must be zero")
        for second in range(size):
            if (
                unfamiliarity[first][second] < 0
                or unfamiliarity[first][second] != unfamiliarity[second][first]
            ):
                raise ValueError("matrix must be nonnegative and symmetric")

    cost = [[0] * size for _ in range(size)]
    for right in range(size):
        running = 0
        for left in range(right - 1, -1, -1):
            running += unfamiliarity[left][right]
            cost[left][right] = cost[left][right - 1] + running

    infinity = 10**30
    previous = [0] + [infinity] * size
    for groups in range(1, group_count + 1):
        current = [infinity] * (size + 1)

        def compute(left: int, right: int, low_cut: int, high_cut: int) -> None:
            if left > right:
                return
            middle = (left + right) // 2
            best_cut = -1
            upper = min(high_cut, middle - 1)
            for cut in range(low_cut, upper + 1):
                candidate = previous[cut] + cost[cut][middle - 1]
                if candidate < current[middle]:
                    current[middle] = candidate
                    best_cut = cut
            if best_cut == -1:
                raise RuntimeError("missing partition transition")
            compute(left, middle - 1, low_cut, best_cut)
            compute(middle + 1, right, best_cut, high_cut)

        compute(groups, size, groups - 1, size - 1)
        previous = current
    return previous[size]
```

### Why the expert code is correct

The recurrence tries every final group boundary. Interval pair costs satisfy the
quadrangle inequality: extending two nested intervals adds only nonnegative
crossing pairs. Therefore minimizing cut indices are monotone. The recursive
search retains every possible optimum while discarding cut ranges that
monotonicity proves cannot win.

**Complexity:** `O(n^2 + k n log n)` time and `O(n^2)` space.

## 6. What to remember

```text
contiguous groups -> prefix partition DP
pair costs on intervals -> monotone optimal cuts
one monotone DP layer -> divide-and-conquer optimization
```
