# Focus300 260: LeetCode 194 - Transpose File

**Source:** [LeetCode 194](https://leetcode.com/problems/transpose-file/)  
**Difficulty:** Easy  
**Pattern:** SQL ranking and filtering

## Exact contract

Return the requested query result using the table's ordering, grouping, or ranking rule.

## First principles

The answer comes from relational operations rather than procedural loops. Filtering, grouping, ranking, and tie handling are all declarative pieces of the same query.


## Classroom board: transpose a tiny table

```text
    rows:
    name    age
    alice   20
    bob     30

    transpose:
    name    alice   bob
    age     20      30
```



## Step-by-step transformation

1. Read the table rows and keep only the rows that can still contribute to the answer.
2. Use joins, grouping, ranking, or filtering to turn the raw rows into one intermediate result set.
3. Apply tie rules or ordering rules before selecting the final row or value.
4. Project the requested column(s), which is the final output of the query.

In SQL problems, the database performs the transformation by moving rows through `WHERE`, `JOIN`, `GROUP BY`, window functions, and `ORDER BY` until only the requested result remains.


## Diagram: SQL rows to final answer

```text

            raw table rows
                |
                v
            filter / join / group / rank
                |
                v
            ordered result rows
                |
                v
            requested output column
```

The query turns table rows into one final answer by filtering, combining, and ranking the data in SQL.

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
