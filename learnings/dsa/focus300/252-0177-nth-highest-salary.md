# Focus300 252: LeetCode 177 - Nth Highest Salary

**Source:** [LeetCode 177](https://leetcode.com/problems/nth-highest-salary/)  
**Difficulty:** Easy  
**Pattern:** SQL ranking and filtering

## Exact contract

Return the requested query result using the table's ordering, grouping, or ranking rule.

## First principles

The answer comes from relational operations rather than procedural loops. Filtering, grouping, ranking, and tie handling are all declarative pieces of the same query.


## Classroom board: skip the first n-1 distinct salaries

```text
    salaries = [500, 400, 400, 300]

    distinct sorted salaries: [500, 400, 300]
    n = 2 -> answer = 400
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
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
    RETURN (
        SELECT DISTINCT salary
        FROM Employee
        ORDER BY salary DESC
        LIMIT 1 OFFSET N - 1
    );
END
```

Export the table and compute the answer manually.

## Better insight

Express the ranking or grouping directly in SQL so the database does the work.

## Expert solution

```sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
    RETURN (
        SELECT DISTINCT salary
        FROM Employee
        ORDER BY salary DESC
        LIMIT N - 1, 1
    );
END
```

Use the smallest query that matches the requested filter, order, and tie semantics.

**Complexity:** Database-dependent, but typically linear or near-linear in the number of rows scanned.
