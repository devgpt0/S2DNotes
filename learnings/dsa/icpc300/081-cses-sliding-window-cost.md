# ICPC300 081: CSES - Sliding Window Cost

**Source:** [CSES - Sliding Window Cost](https://cses.fi/problemset/task/1077/)  
**Pattern:** order statistics with Fenwick trees  
**Goal:** For every length-`k` window, return the minimum total adjustment cost
to make all values equal.

## 1. First principles

The sum of absolute differences is minimized at a median. For each window we
need its lower median plus the count and sum of values on both sides:

```text
cost = median * left_count - left_sum
     + right_sum - median * right_count
```

Coordinate compression and two Fenwick trees maintain value counts and sums.
Fenwick binary lifting finds the lower median by rank.

## 2. Cases that decide correctness

- Duplicate medians must retain their full multiplicity.
- For even `k`, either middle value gives the same cost; use the lower one.
- Negative and repeated values are valid.
- `k = 1` produces only zero costs.
- Removing a value must update both count and sum trees.

## 3. Brute force: sort every window

```python
def sliding_window_cost_brute(values: list[int], window_size: int) -> list[int]:
    if window_size <= 0 or window_size > len(values):
        raise ValueError("window_size must be in [1, len(values)]")

    answers: list[int] = []
    for start in range(len(values) - window_size + 1):
        window = sorted(values[start : start + window_size])
        median = window[(window_size - 1) // 2]
        answers.append(sum(abs(value - median) for value in window))
    return answers
```

**Complexity:** `O(n k log k)` time and `O(k)` space.

## 4. Better: maintain one sorted window

Bisect finds insertion/removal positions, but list shifts and the cost scan are
still linear in `k`.

```python
from bisect import bisect_left, insort


def sliding_window_cost_sorted_list(values: list[int], window_size: int) -> list[int]:
    if window_size <= 0 or window_size > len(values):
        raise ValueError("window_size must be in [1, len(values)]")

    window = sorted(values[:window_size])

    def current_cost() -> int:
        median = window[(window_size - 1) // 2]
        return sum(abs(value - median) for value in window)

    answers = [current_cost()]
    for right in range(window_size, len(values)):
        leaving = values[right - window_size]
        window.pop(bisect_left(window, leaving))
        insort(window, values[right])
        answers.append(current_cost())
    return answers
```

**Complexity:** `O(nk)` time and `O(k)` space.

## 5. Expert solution: compressed Fenwick trees

One Fenwick tree stores frequencies and another stores value sums. A rank
search returns the lower median in `O(log n)`.

```python
def sliding_window_cost_fenwick(values: list[int], window_size: int) -> list[int]:
    if window_size <= 0 or window_size > len(values):
        raise ValueError("window_size must be in [1, len(values)]")

    coordinates = sorted(set(values))
    position = {value: index for index, value in enumerate(coordinates)}
    count_tree = [0] * (len(coordinates) + 1)
    sum_tree = [0] * (len(coordinates) + 1)

    def add(tree: list[int], index: int, difference: int) -> None:
        index += 1
        while index < len(tree):
            tree[index] += difference
            index += index & -index

    def prefix_sum(tree: list[int], end: int) -> int:
        total = 0
        while end > 0:
            total += tree[end]
            end -= end & -end
        return total

    def update(value: int, difference: int) -> None:
        index = position[value]
        add(count_tree, index, difference)
        add(sum_tree, index, difference * value)

    def index_by_rank(rank: int) -> int:
        index = 0
        step = 1 << (len(coordinates).bit_length() - 1)
        while step:
            next_index = index + step
            if next_index < len(count_tree) and count_tree[next_index] < rank:
                rank -= count_tree[next_index]
                index = next_index
            step //= 2
        return index

    def current_cost() -> int:
        median_index = index_by_rank((window_size + 1) // 2)
        median = coordinates[median_index]
        left_count = prefix_sum(count_tree, median_index)
        left_sum = prefix_sum(sum_tree, median_index)
        through_median_count = prefix_sum(count_tree, median_index + 1)
        through_median_sum = prefix_sum(sum_tree, median_index + 1)
        total_sum = prefix_sum(sum_tree, len(coordinates))
        right_count = window_size - through_median_count
        right_sum = total_sum - through_median_sum
        return median * left_count - left_sum + right_sum - median * right_count

    for value in values[:window_size]:
        update(value, 1)
    answers = [current_cost()]
    for right in range(window_size, len(values)):
        update(values[right - window_size], -1)
        update(values[right], 1)
        answers.append(current_cost())
    return answers
```

### Why the expert code is correct

The rank search finds a valid median. The two prefix trees partition every
window value into left, median, or right contributions, and the displayed
formula is exactly the sum of absolute differences.

**Complexity:** `O(n log n)` time and `O(n)` space.

## 6. What to remember

```text
absolute-deviation minimum -> median
cost around median -> counts and sums on both sides
dynamic rank + prefix aggregates -> Fenwick trees
```
