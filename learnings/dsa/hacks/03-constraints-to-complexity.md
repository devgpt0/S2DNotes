# Turn Constraints into an Algorithm Budget

## First principles

Constraints are a maximum-work contract. Estimate how many states the solution
visits and the work per state before choosing an algorithm. Include every test
case and query, not only the largest single array.

## Why it matters

The constraints often reveal the intended algorithm before the story does.

## Technique

Estimate the dominant operations at the maximum input. Python usually needs a
smaller operation budget than optimized C++, especially for nested Python
loops and object-heavy data structures.

## Quick table

| Maximum size | First techniques to consider |
| ---: | --- |
| `n <= 20` | subsets, bitmask DP, backtracking |
| `n <= 40` | meet in the middle |
| `n <= 400` | `O(n^3)` only with small/simple work; often risky in Python |
| `n <= 5,000` | `O(n^2)` may fit if tight |
| `n <= 200,000` | `O(n log n)` or `O(n)` |
| values `<= 10^6` | sieve, frequency arrays, value-based DP |

## Pattern

```text
read n, q, value range
    -> estimate allowed complexity
    -> list algorithms in that class
    -> use problem structure to choose one
```

## Example

If `n = 200_000` and the problem asks `q = 200_000` range sums:

- scanning every range is `O(nq)`: impossible;
- static array: prefix sums, `O(n + q)`;
- point updates: Fenwick/segment tree, `O((n + q) log n)`;
- range updates offline: difference array, `O(n + q)`.

## Python check

```python
from math import log2

n = 200_000
print(n)                 # linear visits
print(int(n * log2(n))) # about 3.5 million structural steps
print(n * n)             # 40 billion: impossible
```

## Visual worked example: reject the impossible plan

```text
n = 200,000, q = 200,000

scan each query:
n * q = 40,000,000,000 element visits  -> reject

prefix sums:
build n + answer q
= 400,000 structural steps             -> plausible

with updates, Fenwick tree:
(n + q) * log2(n)
about 400,000 * 18                     -> plausible
```

The table narrows the algorithm family; the required operations choose the
actual data structure.

## Traps

- Ignoring `q`; total work often depends on `n + q` or `n*q`.
- Calling `O(n log n)` safe without considering a heavy inner operation.
- Forgetting memory: `O(n^2)` integers are impossible long before loops finish.
- Treating these thresholds as guarantees rather than estimates.
