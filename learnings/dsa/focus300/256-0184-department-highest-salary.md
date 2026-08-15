# Focus300 256: LeetCode 184 - Department Highest Salary

**Source:** [LeetCode 184](https://leetcode.com/problems/department-highest-salary/)  
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
SELECT d.Name AS Department, e.Name AS Employee, e.Salary
FROM Employee e
JOIN Department d ON e.DepartmentId = d.Id
WHERE (
    SELECT COUNT(DISTINCT e2.Salary)
    FROM Employee e2
    WHERE e2.DepartmentId = e.DepartmentId AND e2.Salary > e.Salary
) = 0;
```

Export the table and compute the answer manually.

## Better insight

Express the ranking or grouping directly in SQL so the database does the work.

## Expert solution

```sql
WITH ranked AS (
    SELECT
        d.Name AS Department,
        e.Name AS Employee,
        e.Salary,
        DENSE_RANK() OVER (PARTITION BY e.DepartmentId ORDER BY e.Salary DESC) AS rnk
    FROM Employee e
    JOIN Department d ON e.DepartmentId = d.Id
)
SELECT Department, Employee, Salary
FROM ranked
WHERE rnk <= 3
ORDER BY Department, Salary DESC, Employee;
```

Use the smallest query that matches the requested filter, order, and tie semantics.

**Complexity:** Database-dependent, but typically linear or near-linear in the number of rows scanned.
