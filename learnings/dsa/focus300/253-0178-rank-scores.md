# Focus300 253: LeetCode 178 - Rank Scores

**Source:** [LeetCode 178](https://leetcode.com/problems/rank-scores/)  
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
SELECT
    score,
    1 + (SELECT COUNT(DISTINCT score) FROM Scores s2 WHERE s2.score > s1.score) AS rank
FROM Scores s1
ORDER BY score DESC;
```

Export the table and compute the answer manually.

## Better insight

Express the ranking or grouping directly in SQL so the database does the work.

## Expert solution

```sql
SELECT
    score,
    DENSE_RANK() OVER (ORDER BY score DESC) AS rank
FROM Scores
ORDER BY score DESC;
```

Use the smallest query that matches the requested filter, order, and tie semantics.

**Complexity:** Database-dependent, but typically linear or near-linear in the number of rows scanned.
