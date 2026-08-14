# ICPC300 052: CSES - Subarray Sum Queries

**Source:** [CSES - Subarray Sum Queries](https://cses.fi/problemset/task/1190/)  
**Pattern:** maximum-subarray segment-tree monoid  
**Goal:** After each point assignment, report the maximum subarray sum. The
empty subarray is allowed, so the answer is never negative.

Updates are zero-based `(index, value)` pairs.

## 1. First principles

To combine adjacent segments, the best subarray is either entirely left,
entirely right, or crosses the boundary. A segment therefore stores four
values:

| Field | Meaning |
| --- | --- |
| `total` | Sum of the whole segment. |
| `prefix` | Best prefix sum, including the empty prefix. |
| `suffix` | Best suffix sum, including the empty suffix. |
| `best` | Best subarray sum anywhere in the segment. |

```text
combined.best = max(left.best, right.best, left.suffix + right.prefix)
```

These four fields form an associative summary, so a segment tree can rebuild
all affected ancestors after one assignment.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| All values negative | Return `0` for the empty subarray. |
| Best subarray crosses a midpoint | Use left suffix plus right prefix. |
| One positive value | Return that value. |
| Update removes the old optimum | Ancestor summaries must be rebuilt. |
| Update creates a longer optimum | Prefix and suffix fields must propagate it. |

## 3. Brute force: enumerate all subarrays

```python
def subarray_sum_queries_brute(
    values: list[int], updates: list[tuple[int, int]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    current = values.copy()
    answers: list[int] = []
    for index, value in updates:
        current[index] = value
        best = 0
        for left in range(len(current)):
            subarray_sum = 0
            for right in range(left, len(current)):
                subarray_sum += current[right]
                best = max(best, subarray_sum)
        answers.append(best)
    return answers
```

**Complexity:** `O(n^2)` per update and `O(n)` storage.

## 4. Better: rerun Kadane's algorithm

The best subarray ending at the current position is either empty or extends
the previous best ending there.

```python
def subarray_sum_queries_kadane(
    values: list[int], updates: list[tuple[int, int]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    current = values.copy()
    answers: list[int] = []
    for index, value in updates:
        current[index] = value
        best_ending_here = 0
        best = 0
        for element in current:
            best_ending_here = max(0, best_ending_here + element)
            best = max(best, best_ending_here)
        answers.append(best)
    return answers
```

**Complexity:** `O(n)` per update and `O(n)` storage.

## 5. Expert solution: segment tree

Store `(total, prefix, suffix, best)` at every node. Only the assigned leaf
and its `O(log n)` ancestors change.

```python
Summary = tuple[int, int, int, int]


def subarray_sum_queries_segment_tree(
    values: list[int], updates: list[tuple[int, int]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    def leaf(value: int) -> Summary:
        nonnegative = max(0, value)
        return value, nonnegative, nonnegative, nonnegative

    def combine(left: Summary, right: Summary) -> Summary:
        left_total, left_prefix, left_suffix, left_best = left
        right_total, right_prefix, right_suffix, right_best = right
        return (
            left_total + right_total,
            max(left_prefix, left_total + right_prefix),
            max(right_suffix, right_total + left_suffix),
            max(left_best, right_best, left_suffix + right_prefix),
        )

    tree_size = 1
    while tree_size < len(values):
        tree_size *= 2
    identity: Summary = (0, 0, 0, 0)
    tree: list[Summary] = [identity] * (2 * tree_size)

    for index, value in enumerate(values):
        tree[tree_size + index] = leaf(value)
    for node in range(tree_size - 1, 0, -1):
        tree[node] = combine(tree[2 * node], tree[2 * node + 1])

    answers: list[int] = []
    for index, value in updates:
        node = tree_size + index
        tree[node] = leaf(value)
        node //= 2
        while node > 0:
            tree[node] = combine(tree[2 * node], tree[2 * node + 1])
            node //= 2
        answers.append(tree[1][3])
    return answers
```

### Why the expert code is correct

- A leaf summary is exact for one value and includes the permitted empty
  subarray.
- Every subarray of a combined segment belongs to one of the three merge
  cases: left, right, or crossing.
- Rebuilding the unique leaf-to-root path restores exact summaries everywhere.

**Complexity:** `O(n)` construction, `O(log n)` per update, and `O(n)` space.

## 6. What to remember

```text
segment summary = total, best prefix, best suffix, best subarray
crossing candidate = left suffix + right prefix
empty subarray allowed -> prefix, suffix, best are at least zero
```
