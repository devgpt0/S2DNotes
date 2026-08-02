# Assertions and Useful Debugging

## First principles

An invariant is useful only if a violation becomes visible near its cause.
Assertions turn silent state corruption into an immediate, reproducible
failure. They should verify programmer assumptions, not replace input handling.

## Why it matters

Good debugging tests your reasoning. Random print statements create noise and
can cause wrong output.

## Technique

Assert invariants at the point they should hold:

```python
assert left <= right
assert all(values[index] <= values[index + 1] for index in range(len(values) - 1))
assert sum(frequency.values()) == right - left
```

Send temporary diagnostics to standard error:

```python
import sys

DEBUG = False


def debug(*values: object) -> None:
    if DEBUG:
        print(*values, file=sys.stderr)
```

## Debugging order

1. Reduce to the smallest failing input.
2. Write the expected state after each step.
3. Find the first step where actual state differs.
4. Fix the violated invariant, not the final symptom.

## Pattern recognition

Use assertions for binary-search boundaries, monotonic structures, DSU roots,
flow conservation, DP state ranges, and index conversions.

## Expert habit

Print structured state with labels, one iteration at a time:

```python
debug('window', left, right, 'sum', total, 'best', answer)
```

## Visual worked example: catch corruption early

A sliding window must contain no duplicate values.

```text
add a -> window [a]       set {a}       valid
add b -> window [a,b]     set {a,b}     valid
add a without shrinking:
        window [a,b,a]    set {a,b}
        len(window)=3 != len(set)=2 -> assertion fails here
```

Without the assertion, the algorithm may return a wrong length much later,
far from the bad update.

## Traps

- Catching broad exceptions and hiding the useful traceback.
- Leaving debug output on standard output.
- Keeping an `O(n)` assertion inside a hot `O(n)` loop for submission.
- Asserting a belief before proving it; a failed assertion may expose a wrong
  model, not only a code bug.
