# ICPC300 005: CSES - Path Queries II

**Source:** [CSES - Path Queries II](https://cses.fi/problemset/task/2134/)  
**Core pattern:** heavy-light decomposition

## First principles

A path becomes only logarithmically many contiguous heavy-chain ranges. A segment tree answers each range maximum.

## Cases to check

- Empty/minimum input, boundary indices, duplicate values, and the largest allowed input.
- Write a tiny brute-force oracle before trusting an optimization.

## 1. Brute force

Start from the definition. It is correct but deliberately too slow at contest limits.

```python
def brute(parent, value, first, second):
    seen = set()
    while first != -1: seen.add(first); first = parent[first]
    answer = -10**18
    while second not in seen: answer = max(answer, value[second]); second = parent[second]
    return max(answer, value[second])
```

## 2. Better approach

Remove one repeated computation, but check whether its memory or worst-case time still fits.

```python
def better(path_values):
    return max(path_values)
```

## 3. Expert solution

Use the stated pattern because it preserves the exact invariant while avoiding repeated work.

```python
def path_ranges(head, parent, depth, position, first, second):
    result = []
    while head[first] != head[second]:
        if depth[head[first]] < depth[head[second]]: first, second = second, first
        result.append((position[head[first]], position[first])); first = parent[head[first]]
    if depth[first] > depth[second]: first, second = second, first
    return result + [(position[first], position[second])]
```

## Remember

State the invariant aloud, test adversarial boundaries against brute force, then implement the expert version.
