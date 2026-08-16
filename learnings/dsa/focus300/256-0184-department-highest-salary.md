# Focus300 256: LeetCode 184 - Department Highest Salary

**Source:** [LeetCode 184](https://leetcode.com/problems/department-highest-salary/)  
**Difficulty:** Easy  
**Pattern:** SQL ranking and filtering

## Exact contract

Return the requested query result using the table's ordering, grouping, or ranking rule.

## First principles

The answer comes from relational operations rather than procedural loops. Filtering, grouping, ranking, and tie handling are all declarative pieces of the same query.


## Classroom board: rank salaries inside each department

```text
    dept  salary
    A     100
    A     90
    B     80

    keep the top salary per dept, then move to the next ranked row.
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
