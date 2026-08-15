# Focus300 255: LeetCode 180 - Consecutive Numbers

**Source:** [LeetCode 180](https://leetcode.com/problems/consecutive-numbers/)  
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

```sql
SELECT DISTINCT l1.Num AS ConsecutiveNums
FROM Logs l1
JOIN Logs l2 ON l1.Id = l2.Id - 1 AND l1.Num = l2.Num
JOIN Logs l3 ON l2.Id = l3.Id - 1 AND l2.Num = l3.Num;
```

Export the table and compute the answer manually.

## Better insight

Express the ranking or grouping directly in SQL so the database does the work.

## Expert solution

```sql
SELECT DISTINCT Num AS ConsecutiveNums
FROM (
    SELECT
        Num,
        LAG(Num, 1) OVER (ORDER BY Id) AS prev1,
        LAG(Num, 2) OVER (ORDER BY Id) AS prev2
    FROM Logs
) x
WHERE Num = prev1 AND Num = prev2;
```

Use the smallest query that matches the requested filter, order, and tie semantics.

**Complexity:** Database-dependent, but typically linear or near-linear in the number of rows scanned.
