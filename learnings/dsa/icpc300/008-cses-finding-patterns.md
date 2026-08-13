# ICPC300 008: CSES - Finding Patterns

**Source:** [CSES - Finding Patterns](https://cses.fi/problemset/task/2102/)  
**Core pattern:** Aho-Corasick automaton

## First principles

Many pattern searches share prefixes. A trie stores them once; failure links make a mismatch behave like the longest usable suffix.

## Cases to check

- Empty/minimum input, boundary indices, duplicate values, and the largest allowed input.
- Write a tiny brute-force oracle before trusting an optimization.

## 1. Brute force

Start from the definition. It is correct but deliberately too slow at contest limits.

```python
def brute(text, pattern):
    return any(text[index:index + len(pattern)] == pattern for index in range(len(text) - len(pattern) + 1))
```

## 2. Better approach

Remove one repeated computation, but check whether its memory or worst-case time still fits.

```python
def better(text, pattern):
    return pattern in text
```

## 3. Expert solution

Use the stated pattern because it preserves the exact invariant while avoiding repeated work.

```python
from collections import deque
# Expert: build trie transitions, BFS failure links, then scan text once.
def advance(go, fail, state, char):
    while state and char not in go[state]: state = fail[state]
    return go[state].get(char, 0)
```

## Remember

State the invariant aloud, test adversarial boundaries against brute force, then implement the expert version.
