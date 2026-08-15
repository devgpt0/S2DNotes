# Focus300 285: LeetCode 241 - Different Ways to Add Parentheses

**Source:** [LeetCode 241](https://leetcode.com/problems/different-ways-to-add-parentheses/)  
**Difficulty:** Medium  
**Pattern:** divide-and-conquer expression enumeration

## Exact contract

Return every possible result from adding parentheses in all valid ways.

## First principles

Each operator can be the final split of the expression. Recursing on the left and right substrings enumerates all possible parse trees.

## Cases that decide correctness

- A pure number returns a single result.
- Repeated subexpressions should be memoized to avoid recomputation.
- Different parenthesizations may produce the same numeric value.
- The output is a multiset of possible results, not a single optimum.

## Brute force

```python
from functools import lru_cache
import operator

ops = {"+": operator.add, "-": operator.sub, "*": operator.mul}

def diff_ways_to_compute_brute(expression):
    if expression.isdigit():
        return [int(expression)]
    result = []
    for i, ch in enumerate(expression):
        if ch in ops:
            for left in diff_ways_to_compute_brute(expression[:i]):
                for right in diff_ways_to_compute_brute(expression[i + 1 :]):
                    result.append(ops[ch](left, right))
    return result
```

Generate all parenthesized strings first and then evaluate them.

## Better insight

Split on each operator, recurse on both sides, and combine the result lists.

## Expert solution

```python
from functools import lru_cache
import operator

ops = {"+": operator.add, "-": operator.sub, "*": operator.mul}

def diff_ways_to_compute(expression):
    @lru_cache(None)
    def solve(expr):
        if expr.isdigit():
            return (int(expr),)
        result = []
        for i, ch in enumerate(expr):
            if ch in ops:
                for left in solve(expr[:i]):
                    for right in solve(expr[i + 1 :]):
                        result.append(ops[ch](left, right))
        return tuple(result)

    return list(solve(expression))
```

Treat each operator as a partition point, memoize substring results, and combine every left value with every right value.

**Complexity:** Exponential output size with memoized subproblem reuse.
