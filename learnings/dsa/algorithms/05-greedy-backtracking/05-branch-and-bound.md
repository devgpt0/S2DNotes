# Branch and Bound

## Idea

Branch and bound is backtracking with an optimistic bound. If even the best
possible completion cannot beat the current answer, stop exploring that branch.

## Visual model

```text
current score + best possible remaining <= best known -> prune
```

## Classroom board: prove a branch cannot win

```text
best known = 15
current sum = 8
all remaining positive values total 6
even the impossible best case is 8+6=14
14 cannot beat 15 -> prune this whole branch
```

The bound may be optimistic, but it must never underestimate a branch.

## Steps

1. Find any valid answer to create a baseline.
2. At each state, compute a bound that is at least as good as every completion.
3. Prune when the bound cannot improve the baseline.
4. Explore promising choices first so the baseline improves early.

## First-principles derivation

Backtracking explores all possible completions. Branch and bound computes an
optimistic best result a branch could ever achieve.

If even that optimistic result cannot beat the current answer, the real branch
cannot win and is safe to discard.

## Pattern recognition

Use it for exponential optimization such as knapsack, traveling salesperson,
or scheduling when constraints are too large for plain enumeration but small
enough for strong pruning.

## Implementation: maximum subset sum not exceeding a limit

Values must be non-negative; descending order improves pruning.

### C++

```cpp
long long bestSubsetSum(std::vector<int> values, long long limit) {
    std::sort(values.rbegin(), values.rend());
    std::vector<long long> suffix(values.size() + 1, 0);
    for (int index = values.size() - 1; index >= 0; --index) suffix[index] = suffix[index + 1] + values[index];
    long long best = 0;
    std::function<void(int, long long)> search = [&](int index, long long sum) {
        if (sum > limit || sum + suffix[index] <= best) return;
        if (index == static_cast<int>(values.size())) {
            best = std::max(best, sum);
            return;
        }
        search(index + 1, sum + values[index]);
        search(index + 1, sum);
    };
    search(0, 0);
    return best;
}
```

### Python

```python
def best_subset_sum(values: list[int], limit: int) -> int:
    items = sorted(values, reverse=True)
    suffix = [0] * (len(items) + 1)
    for index in range(len(items) - 1, -1, -1):
        suffix[index] = suffix[index + 1] + items[index]
    best = 0

    def search(index: int, total: int) -> None:
        nonlocal best
        if total > limit or total + suffix[index] <= best:
            return
        if index == len(items):
            best = max(best, total)
            return
        search(index + 1, total + items[index])
        search(index + 1, total)

    search(0, 0)
    return best
```

### Java

```java
static long bestSubsetSum(int[] values, long limit) {
    Arrays.sort(values);
    for (int left = 0, right = values.length - 1; left < right; left++, right--) {
        int temporary = values[left];
        values[left] = values[right];
        values[right] = temporary;
    }
    long[] suffix = new long[values.length + 1];
    for (int index = values.length - 1; index >= 0; index--) suffix[index] = suffix[index + 1] + values[index];
    long[] best = {0};
    subsetSearch(values, suffix, 0, 0, limit, best);
    return best[0];
}

static void subsetSearch(int[] values, long[] suffix, int index, long sum, long limit, long[] best) {
    if (sum > limit || sum + suffix[index] <= best[0]) return;
    if (index == values.length) {
        best[0] = Math.max(best[0], sum);
        return;
    }
    subsetSearch(values, suffix, index + 1, sum + values[index], limit, best);
    subsetSearch(values, suffix, index + 1, sum, limit, best);
}
```

## Why it works

`sum + suffix[index]` assumes every remaining value can be taken, so no real
completion can exceed it. Pruning below the best known answer cannot remove an
optimal solution.

## Complexity

Worst-case time remains `O(2^n)` and stack space is `O(n)`; a good bound can
make practical search dramatically smaller.

## Common mistakes

- Using a bound that is not truly optimistic, which can prune the optimum.
- Claiming a better worst-case complexity from pruning.
- Applying the suffix bound when values may be negative.
