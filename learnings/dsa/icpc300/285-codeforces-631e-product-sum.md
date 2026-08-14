# ICPC300 285: Codeforces 631E - Product Sum

**Source:** [Codeforces 631E - Product Sum](https://codeforces.com/problemset/problem/631/E)  
**Rating:** 2400  
**Pattern:** one-move gain optimized by Li Chao trees  
**Goal:** Maximize `sum((index + 1) * value[index])` after moving at most one
array element to another position and shifting the intervening block.

## 1. First principles

Let `prefix[k]` be the sum of the first `k` values. Moving `value[i]` right to
`j > i` changes the score by

```text
j * value[i] + prefix[i + 1] - i * value[i] - prefix[j + 1]
```

Moving it left to `j < i` changes the score by

```text
prefix[i] - i * value[i] + j * value[i] - prefix[j]
```

Each maximum is a line query.

## 2. Cases that decide correctness

- Moving no element is allowed.
- Values may be negative.
- Moving right and moving left use different line families.
- Indices in the formulas are zero-based; the original score is one-based.
- A length-one array keeps its original score.

## 3. Brute force: try every final position

```python
def maximum_product_sum_brute(values: list[int]) -> int:
    if not values:
        raise ValueError("values must be nonempty")

    answer = sum((index + 1) * value for index, value in enumerate(values))
    for source in range(len(values)):
        for target in range(len(values)):
            moved = values.copy()
            value = moved.pop(source)
            moved.insert(target, value)
            answer = max(
                answer,
                sum((index + 1) * item for index, item in enumerate(moved)),
            )
    return answer
```

**Complexity:** `O(n^3)` time and `O(n)` space.

## 4. Better transition: turn every possible source into a line

For right moves, source `i` contributes line
`value[i] * x + prefix[i+1] - i*value[i]`, queried at `x=j`. For left moves,
target `j` contributes line `j*x - prefix[j]`, queried at `x=value[i]`.
Discrete Li Chao trees support arbitrary insertion and query order.

## 5. Expert solution: two Li Chao sweeps

```python
from bisect import bisect_left


class MaximumLiChao:
    def __init__(self, coordinates: list[int]) -> None:
        self.coordinates = sorted(set(coordinates))
        self.lines: list[tuple[int, int] | None] = [None] * (4 * len(self.coordinates))

    @staticmethod
    def value(line: tuple[int, int], coordinate: int) -> int:
        slope, intercept = line
        return slope * coordinate + intercept

    def add(
        self,
        line: tuple[int, int],
        node: int = 1,
        left: int = 0,
        right: int | None = None,
    ) -> None:
        if right is None:
            right = len(self.coordinates) - 1
        current = self.lines[node]
        if current is None:
            self.lines[node] = line
            return
        middle = (left + right) // 2
        if self.value(line, self.coordinates[middle]) > self.value(
            current, self.coordinates[middle]
        ):
            line, current = current, line
            self.lines[node] = current
        if left == right:
            return
        if self.value(line, self.coordinates[left]) > self.value(
            current, self.coordinates[left]
        ):
            self.add(line, node * 2, left, middle)
        elif self.value(line, self.coordinates[right]) > self.value(
            current, self.coordinates[right]
        ):
            self.add(line, node * 2 + 1, middle + 1, right)

    def query(self, coordinate: int) -> int:
        index = bisect_left(self.coordinates, coordinate)
        node = 1
        left = 0
        right = len(self.coordinates) - 1
        answer = -(10**30)
        while True:
            line = self.lines[node]
            if line is not None:
                answer = max(answer, self.value(line, coordinate))
            if left == right:
                return answer
            middle = (left + right) // 2
            if index <= middle:
                node *= 2
                right = middle
            else:
                node = node * 2 + 1
                left = middle + 1


def maximum_product_sum(values: list[int]) -> int:
    if not values:
        raise ValueError("values must be nonempty")

    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)
    original = sum((index + 1) * value for index, value in enumerate(values))
    answer = original

    right_hull = MaximumLiChao(list(range(len(values))))
    for index, value in enumerate(values):
        if index > 0:
            gain = right_hull.query(index) - prefix[index + 1]
            answer = max(answer, original + gain)
        right_hull.add((value, prefix[index + 1] - index * value))

    left_hull = MaximumLiChao(values)
    for index, value in enumerate(values):
        if index > 0:
            gain = prefix[index] - index * value + left_hull.query(value)
            answer = max(answer, original + gain)
        left_hull.add((index, -prefix[index]))
    return answer
```

### Why the expert code is correct

The two gain identities account exactly for the moved element and every
one-position shift in the intervening block. Each source-target choice appears
as one line evaluated at one query coordinate. Query-before-insert enforces
`i < j` or `j < i`, and both directions plus the unchanged score exhaust all
allowed results.

**Complexity:** `O(n log n)` time and `O(n)` space.

## 6. What to remember

```text
move one element -> original score plus a range-shift gain
gain separates by source and target -> line evaluation
both move directions -> two line families
```
