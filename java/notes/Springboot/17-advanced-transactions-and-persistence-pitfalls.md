# 17 - Advanced Transactions and Persistence Pitfalls

## Simple Mental Model

Imagine a bank transfer with two updates. Both must succeed together. A transaction is the database boundary that commits both or rolls both back. Propagation describes what a transactional method should do when another transaction already exists.

**Why it matters:** Incorrect boundaries cause partial changes, long locks, lost updates, unexpected commits, and connection-pool exhaustion.

**How to apply it:** Put the transaction on the public service use case, keep it short, understand rollback/propagation, enforce constraints in the database, and verify behavior with integration tests.

## Propagation

- `REQUIRED`: join an existing transaction or create one
- `REQUIRES_NEW`: suspend current transaction and create another
- `SUPPORTS`: join if present, otherwise run without one
- `MANDATORY`: fail if no transaction exists
- `NOT_SUPPORTED`: suspend and run without a transaction
- `NEVER`: fail if a transaction exists
- `NESTED`: savepoint-based nested behavior when supported

```java
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void writeAudit(AuditRecord record) {
    repository.save(record);
    // Result: audit uses an independent transaction when proxy interception applies.
}
```

Using `REQUIRES_NEW` consumes another connection and is not a guarantee that audit survives every infrastructure failure.

## Rollback Rules

By default, runtime exceptions and errors trigger rollback; checked exceptions do not. Configure explicitly only when business semantics require it.

```java
@Transactional(rollbackFor = IOException.class)
public void importFile(Path path) throws IOException {
    importRows(path);
    // Result: IOException marks the transaction for rollback.
}
```

## Persistence Context

Managed entities have identity within the persistence context and are dirty-checked at flush. Detached objects are no longer tracked. `merge` copies state into a managed instance; it does not reattach the same Java object.

## N+1 and Fetching

- `EAGER` does not guarantee one query
- `LAZY` avoids unnecessary loading but requires a valid transaction when accessed
- use fetch joins, entity graphs, projections, or batch fetching per use case
- verify generated SQL and query counts

## Lost Updates

```java
@Version
private long version;
// Result: an update includes the version and stale concurrent writes fail.
```

Use database constraints as the final protection for uniqueness and invariants. An `exists` pre-check improves the error but remains racy.

## Transaction Boundary Rules

- keep transactions short
- do not call slow remote services while holding database resources
- publish reliable external events through an outbox
- do not use Open Session in View to hide fetch design
- define idempotency for retried commands
- understand database isolation and locking, not just annotations
