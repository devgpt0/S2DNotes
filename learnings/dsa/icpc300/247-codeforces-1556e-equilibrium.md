# ICPC300 247: Codeforces 1556E - Equilibrium

**Source:** [Codeforces 1556E](https://codeforces.com/problemset/problem/1556/E)  
**Difficulty:** 2200  
**Pattern:** prefix balance with static range minimum and maximum

## Exact contract

For arrays `a` and `b`, each query isolates an inclusive segment `[l,r]`.
Under the source's left-to-right balancing rule, a segment is feasible exactly
when its total difference is zero and no running difference `a-b` is negative.
Print `-1` if it is infeasible; otherwise print the largest running difference.

## First principles

Define `prefix[i] = sum(a[j]-b[j])` for `j <= i`. Relative to the balance just
before `l`, a query needs:

- `prefix[r] == prefix[l-1]`, so the final balance is zero;
- `min(prefix[l..r]) >= prefix[l-1]`, so no prefix needs unavailable units.

When both hold, the requested answer is
`max(prefix[l..r]) - prefix[l-1]`.

## Cases that decide correctness

- A zero total is necessary but does not prevent a negative intermediate sum.
- Query comparisons use the baseline at `l-1`, not zero.
- A one-element segment is feasible only when its values are equal.
- Negative array differences are represented directly in the prefix sums.
- Arrays never change, so static range queries are sufficient.

## Brute force: scan each queried segment

```python
def equilibrium_brute(
    first: list[int],
    second: list[int],
    queries: list[tuple[int, int]],
) -> list[int]:
    answers: list[int] = []
    for left, right in queries:
        balance = 0
        maximum = 0
        valid = True
        for index in range(left, right + 1):
            balance += first[index] - second[index]
            maximum = max(maximum, balance)
            if balance < 0:
                valid = False
        answers.append(maximum if valid and balance == 0 else -1)
    return answers
```

This takes `O(nq)` time in the worst case.

## Better insight: every query asks for two extrema of one prefix array

Build range-minimum and range-maximum structures once. The endpoint equality
checks total balance; the two range extrema decide feasibility and the answer.

## Expert solution: iterative min/max segment tree

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size, query_count = map(int, input_stream.readline().split())
    first = list(map(int, input_stream.readline().split()))
    second = list(map(int, input_stream.readline().split()))

    prefix = [0] * (size + 1)
    for index, (first_value, second_value) in enumerate(
        zip(first, second, strict=True), start=1
    ):
        prefix[index] = prefix[index - 1] + first_value - second_value

    base = 1
    while base < size + 1:
        base *= 2
    minimum_tree = [10**30] * (2 * base)
    maximum_tree = [-(10**30)] * (2 * base)
    for index, value in enumerate(prefix):
        minimum_tree[base + index] = value
        maximum_tree[base + index] = value
    for node in range(base - 1, 0, -1):
        minimum_tree[node] = min(minimum_tree[node * 2], minimum_tree[node * 2 + 1])
        maximum_tree[node] = max(maximum_tree[node * 2], maximum_tree[node * 2 + 1])

    def range_extrema(left: int, right: int) -> tuple[int, int]:
        minimum = 10**30
        maximum = -(10**30)
        left += base
        right += base
        while left < right:
            if left & 1:
                minimum = min(minimum, minimum_tree[left])
                maximum = max(maximum, maximum_tree[left])
                left += 1
            if right & 1:
                right -= 1
                minimum = min(minimum, minimum_tree[right])
                maximum = max(maximum, maximum_tree[right])
            left //= 2
            right //= 2
        return minimum, maximum

    answers: list[str] = []
    for _ in range(query_count):
        left, right = map(int, input_stream.readline().split())
        baseline = prefix[left - 1]
        if prefix[right] != baseline:
            answers.append("-1")
            continue
        minimum, maximum = range_extrema(left, right + 1)
        if minimum < baseline:
            answers.append("-1")
        else:
            answers.append(str(maximum - baseline))
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

The data structure returns exactly the two prefix extrema in each segment, so
the implementation applies the feasibility conditions directly.

**Complexity:** `O((n+q) log n)` time and `O(n)` space.
