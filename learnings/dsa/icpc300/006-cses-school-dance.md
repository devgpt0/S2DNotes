# ICPC300 006: CSES - School Dance

**Source:** [CSES - School Dance](https://cses.fi/problemset/task/1696/)  
**Core pattern:** Hopcroft-Karp matching

## First principles

A matching grows only by an augmenting path. BFS groups shortest paths; DFS finds many disjoint ones before the next BFS.

## Cases to check

- Empty/minimum input, boundary indices, duplicate values, and the largest allowed input.
- Write a tiny brute-force oracle before trusting an optimization.

## 1. Brute force

Start from the definition. It is correct but deliberately too slow at contest limits.

```python
def brute(left, right, edges):
    return max((sum((a, b) in edges for a, b in zip(left, permutation)) for permutation in __import__('itertools').permutations(right)), default=0)
```

## 2. Better approach

Remove one repeated computation, but check whether its memory or worst-case time still fits.

```python
def better(graph, matched_right):
    def dfs(left, seen):
        for right in graph[left]:
            if right not in seen:
                seen.add(right)
                if right not in matched_right or dfs(matched_right[right], seen): matched_right[right] = left; return True
        return False
    return sum(dfs(left, set()) for left in range(len(graph)))
```

## 3. Expert solution

Use the stated pattern because it preserves the exact invariant while avoiding repeated work.

```python
# Expert: Hopcroft-Karp alternates BFS layers and DFS only along those layers.
# It improves O(VE) repeated augmenting DFS to O(E * sqrt(V)).
```

## Remember

State the invariant aloud, test adversarial boundaries against brute force, then implement the expert version.
