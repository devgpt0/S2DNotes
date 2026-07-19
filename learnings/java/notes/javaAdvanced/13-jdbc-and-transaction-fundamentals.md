# 13 - JDBC and Transaction Fundamentals

## Beginner Meaning

JDBC is Java's standard API for talking to relational databases. The normal flow is: obtain a connection, create a parameterized statement, execute it, read rows, and close every resource.

## Parameterized Query

```java
String sql = "select id, name from customers where email = ?";
try (PreparedStatement statement = connection.prepareStatement(sql)) {
    statement.setString(1, email);
    try (ResultSet rows = statement.executeQuery()) {
        while (rows.next()) {
            System.out.println(rows.getLong("id") + ":" + rows.getString("name"));
        }
    }
}
// Example output: 7:Asha
```

Never concatenate untrusted values into SQL. Identifiers such as column names cannot use ordinary bind parameters; select them from an allow-list.

## Transaction

```java
connection.setAutoCommit(false);
try {
    debit(connection, fromAccount, amount);
    credit(connection, toAccount, amount);
    connection.commit();
    System.out.println("committed");
} catch (SQLException exception) {
    connection.rollback();
    throw exception;
}
// Output on success: committed
```

Restore connection state before returning manually managed pooled connections, or use a framework transaction manager.

## ACID and Isolation

- Atomicity: all changes commit or none do.
- Consistency: constraints remain valid.
- Isolation: concurrent transactions have defined visibility.
- Durability: committed changes survive failures within the database guarantee.

Isolation anomalies include dirty reads, non-repeatable reads, phantoms, and lost updates. Higher isolation reduces anomalies but may reduce concurrency.

## Batch and Generated Keys

Batch compatible statements to reduce round trips, but cap batch size. Request generated keys explicitly and verify driver behavior.

## Connection Pool

A pool bounds expensive database connections. Pool size must match database capacity and workload. Always set query/network timeouts, close resources, expose pool metrics, and avoid holding a connection during remote calls.
