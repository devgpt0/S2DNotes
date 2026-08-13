# ICPC300 004: Codeforces 86D - Powerful Array

**Source:** [Codeforces 86D - Powerful Array](https://codeforces.com/problemset/problem/86/D)  
**Core pattern:** Mo's algorithm

## First principles

Move a query window instead of rebuilding it. Adding or removing one value changes the answer by a constant-time frequency formula.

## Cases to check

- Empty/minimum input, boundary indices, duplicate values, and the largest allowed input.
- Write a tiny brute-force oracle before trusting an optimization.

## 1. Brute force

Start from the definition. It is correct but deliberately too slow at contest limits.

```python
def brute(values, left, right):
    return sum(value * values[left:right + 1].count(value) ** 2 for value in set(values[left:right + 1]))
```

## 2. Better approach

Remove one repeated computation, but check whether its memory or worst-case time still fits.

```python
def better(values, left, right):
    counts = {}
    for value in values[left:right + 1]: counts[value] = counts.get(value, 0) + 1
    return sum(value * count * count for value, count in counts.items())
```

## 3. Expert solution

Use the stated pattern because it preserves the exact invariant while avoiding repeated work.

```python
def add(value, counts, answer):
    answer -= value * counts[value] * counts[value]
    counts[value] += 1
    return answer + value * counts[value] * counts[value]

def remove(value, counts, answer):
    answer -= value * counts[value] * counts[value]
    counts[value] -= 1
    return answer + value * counts[value] * counts[value]
```

## Remember

State the invariant aloud, test adversarial boundaries against brute force, then implement the expert version.
