# 07 - Queries, Pagination, Locking, and Performance

## What, Why, and How

**What:** Query design decides which rows/columns are loaded, their order, and how concurrent updates are protected.

**Why:** Correct entity mappings can still create N+1 queries, unbounded memory use, unstable pages, or lost updates.

**How:** Project required fields, paginate with stable allow-listed sorting, inspect generated SQL/plans, index access paths, and choose locking from real contention behavior.

## 1) Pagination

```java
interface ProductRepository extends JpaRepository<Product, Long> {
    Page<Product> findByNameContainingIgnoreCase(String name, Pageable pageable);
    // Example result: page content plus total count and page metadata.
}
```

```java
Pageable pageable = PageRequest.of(0, 20, Sort.by("id").ascending());
System.out.println(pageable.getPageSize());
// Output: 20
```

Validate maximum page size and allow only approved sort fields.

## 2) Projection

```java
interface ProductSummary {
    Long getId();
    String getName();
    // Result: a query can fetch only id and name instead of the complete entity.
}
```

Use projections or DTO queries for read models that do not need entity behavior.

## 3) Fetch Joins and N+1

```java
@Query("""
        select distinct o
        from Order o
        join fetch o.items
        where o.id = :id
        """)
Optional<Order> findWithItemsById(@Param("id") long id);
// Result: the order and its items are loaded by one query.
```

Do not combine an unbounded collection fetch join with pagination. Inspect generated SQL and query counts.

## 4) Optimistic Locking

```java
@Version
private long version;
// Result: concurrent stale updates fail instead of silently overwriting newer data.
```

Translate an optimistic locking failure into a meaningful conflict response when the client can retry or refresh.

## 5) Pessimistic Locking

```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("select i from Inventory i where i.id = :id")
Optional<Inventory> findForUpdate(@Param("id") long id);
// Result: the database locks the selected row until transaction completion.
```

Use it only when optimistic concurrency is insufficient; lock ordering and short transactions reduce deadlock risk.

## 6) Performance Checklist

- index columns used for selective filters, joins, and ordering
- paginate bounded queries
- avoid loading full entities for read-only projections
- batch writes deliberately and measure flush behavior
- enforce uniqueness in the database, not only with a pre-check
- use migrations such as Flyway or Liquibase; never rely on automatic production schema creation
