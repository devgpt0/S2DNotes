# ICPC300 003: CSES - Distinct Values Queries

**Source:** [CSES - Distinct Values Queries](https://cses.fi/problemset/task/1734/)  
**Core pattern:** offline queries + Fenwick tree

## First principles

Sweep the right endpoint. Store a one at the latest position of each value; a range sum then equals its distinct count.

## Cases to check

- Empty/minimum input, boundary indices, duplicate values, and the largest allowed input.
- Write a tiny brute-force oracle before trusting an optimization.

## 1. Brute force

Start from the definition. It is correct but deliberately too slow at contest limits.

```python
def brute(values, left, right):
    return len(set(values[left:right + 1]))
```

## 2. Better approach

Remove one repeated computation, but check whether its memory or worst-case time still fits.

```python
def better(values, left, right):
    seen = set()
    for value in values[left:right + 1]: seen.add(value)
    return len(seen)
```

## 3. Expert solution

Use the stated pattern because it preserves the exact invariant while avoiding repeated work.

```python
def add(bit, index, value):
    while index < len(bit): bit[index] += value; index += index & -index

def prefix(bit, index):
    total = 0
    while index: total += bit[index]; index -= index & -index
    return total
```

## Remember

State the invariant aloud, test adversarial boundaries against brute force, then implement the expert version.
