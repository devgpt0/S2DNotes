# ICPC300 002: CSES - Range Queries and Copies

**Source:** [CSES - Range Queries and Copies](https://cses.fi/problemset/task/1737/)  
**Core pattern:** persistent segment tree

## First principles

Each copy is a snapshot. Updating one index changes only one root-to-leaf path, so share every unchanged subtree.

## Cases to check

- Empty/minimum input, boundary indices, duplicate values, and the largest allowed input.
- Write a tiny brute-force oracle before trusting an optimization.

## 1. Brute force

Start from the definition. It is correct but deliberately too slow at contest limits.

```python
def brute(versions, version, index, value):
    versions[version] = versions[version].copy()
    versions[version][index] = value
```

## 2. Better approach

Remove one repeated computation, but check whether its memory or worst-case time still fits.

```python
def better(values, left, right):
    prefix = [0]
    for value in values: prefix.append(prefix[-1] + value)
    return prefix[right + 1] - prefix[left]
```

## 3. Expert solution

Use the stated pattern because it preserves the exact invariant while avoiding repeated work.

```python
def update(node, low, high, index, value):
    if low == high: return (value, None, None)
    middle = (low + high) // 2
    left, right = node[1], node[2]
    if index <= middle: left = update(left, low, middle, index, value)
    else: right = update(right, middle + 1, high, index, value)
    return (left[0] + right[0], left, right)
```

## Remember

State the invariant aloud, test adversarial boundaries against brute force, then implement the expert version.
