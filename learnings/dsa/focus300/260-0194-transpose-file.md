# Focus300 260: LeetCode 194 - Transpose File

**Source:** [LeetCode 194](https://leetcode.com/problems/transpose-file/)  
**Difficulty:** Easy  
**Pattern:** SQL ranking and filtering

## Exact contract

Return the requested query result using the table's ordering, grouping, or ranking rule.

## First principles

The answer comes from relational operations rather than procedural loops. Filtering, grouping, ranking, and tie handling are all declarative pieces of the same query.

## Cases that decide correctness

- Ties must follow the problem's ranking rule exactly.
- Missing rows can produce a null-like answer or no row depending on the statement.
- Order by the requested column before taking top or distinct rows.
- Window functions or grouped subqueries are often the clearest way to express the rule.

## Brute force

```python
import sys

newline = chr(10)
tab = chr(9)
rows = [line.rstrip(newline).split(tab) for line in sys.stdin if line.strip()]
cols = list(zip(*rows))
for col in cols:
    print(tab.join(col))
```

Export the table and compute the answer manually.

## Better insight

Express the ranking or grouping directly in SQL so the database does the work.

## Expert solution

```python
import sys

newline = chr(10)
tab = chr(9)
rows = [line.rstrip(newline).split(tab) for line in sys.stdin if line.strip()]
cols = list(zip(*rows))
for col in cols:
    print(tab.join(col))
```

Use the smallest query that matches the requested filter, order, and tie semantics.

**Complexity:** Database-dependent, but typically linear or near-linear in the number of rows scanned.
