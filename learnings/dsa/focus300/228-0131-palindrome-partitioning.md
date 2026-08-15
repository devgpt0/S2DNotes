# Focus300 228: LeetCode 131 - Palindrome Partitioning

**Source:** [LeetCode 131](https://leetcode.com/problems/palindrome-partitioning/)  
**Difficulty:** Medium  
**Pattern:** backtracking with palindrome checking

## Exact contract

Return every partition of the string such that every piece is a palindrome.

## First principles

The next cut is valid only when the current prefix is already a palindrome. Reusing palindrome knowledge makes the recursion much cheaper than rechecking the same substrings over and over.

## Cases that decide correctness

- A one-character substring is always a palindrome.
- The full string itself may be one valid partition.
- Repeated characters can create many valid cut patterns.
- The result is a collection of partitions, not just a count.

## Brute force

```python
from functools import lru_cache

def partition_brute(s):
    @lru_cache(None)
    def is_pal(i, j):
        return s[i:j] == s[i:j][::-1]

    result = []
    path = []

    def backtrack(start):
        if start == len(s):
            result.append(path.copy())
            return
        for end in range(start + 1, len(s) + 1):
            if is_pal(start, end):
                path.append(s[start:end])
                backtrack(end)
                path.pop()

    backtrack(0)
    return result
```

Try every possible cut position and check each substring from scratch.

## Better insight

Precompute or memoize palindrome checks so the recursion only explores valid prefixes.

## Expert solution

```python
def partition(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for end in range(n):
        for start in range(end + 1):
            pal[start][end] = s[start] == s[end] and (end - start < 2 or pal[start + 1][end - 1])

    result = []
    path = []

    def backtrack(start):
        if start == n:
            result.append(path.copy())
            return
        for end in range(start, n):
            if pal[start][end]:
                path.append(s[start : end + 1])
                backtrack(end + 1)
                path.pop()

    backtrack(0)
    return result
```

Backtrack over cut positions, append the prefix only when it is palindromic, and recurse on the remaining suffix.

**Complexity:** Exponential output size with pruning, plus optional `O(n^2)` palindrome preprocessing.
