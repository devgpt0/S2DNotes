# 07 - SQL, Database, and Transaction Interviews

## SQL Topics

- inner/left/right/full joins and null behavior
- group by, having, aggregate functions
- subqueries, correlated subqueries, CTEs
- window functions: row_number, rank, lag/lead, running totals
- set operations: union vs union all, intersect, except
- delete vs truncate vs drop
- primary, unique, foreign, check constraints

## Indexes

A B-tree index accelerates selective predicates, joins, and ordering with compatible leading columns. It costs storage and write work. Explain composite left-prefix behavior, covering indexes, selectivity, and why functions/type conversions may prevent index use.

## Window Function Example

```sql
SELECT employee_id, department_id, salary,
       DENSE_RANK() OVER (
           PARTITION BY department_id ORDER BY salary DESC
       ) AS salary_rank
FROM employee;
-- Result: employees receive a salary rank within their department without collapsing rows.
```

## Transactions

- ACID and isolation anomalies
- MVCC and snapshots
- optimistic vs pessimistic locking
- deadlock detection and retry
- transaction log and durability
- connection pooling and timeout
- local transaction vs distributed workflow

## Modeling

- normalization reduces update anomalies
- denormalization can optimize known read patterns
- surrogate vs natural keys
- one-to-many and many-to-many modeling
- soft delete implications for uniqueness, queries, and retention
- audit history vs mutable current state

## Query Diagnosis

Use actual execution plans, cardinality estimates, rows scanned, join algorithm, spills, lock waits, and production-like parameter distributions. Do not claim an index always improves a query.
