# Focus300 251: LeetCode 176 - Second Highest Salary

**Source:** [LeetCode 176](https://leetcode.com/problems/second-highest-salary/)  
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
SELECT (
    SELECT MAX(salary)
    FROM Employee
    WHERE salary < (SELECT MAX(salary) FROM Employee)
) AS SecondHighestSalary;
```

Export the table and compute the answer manually.

## Better insight

Express the ranking or grouping directly in SQL so the database does the work.

## Expert solution

```sql
SELECT (
    SELECT DISTINCT salary
    FROM Employee
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
) AS SecondHighestSalary;
```

Use the smallest query that matches the requested filter, order, and tie semantics.

**Complexity:** Database-dependent, but typically linear or near-linear in the number of rows scanned.
