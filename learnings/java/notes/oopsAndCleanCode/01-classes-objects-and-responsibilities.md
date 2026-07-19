# 01 - Classes, Objects, and Responsibilities

## 1) Class vs Object

A class defines structure and behavior. An object is a runtime instance with identity and state.

```java
final class Counter {
    private int value;

    void increment() {
        value++;
    }

    int value() {
        return value;
    }
}

Counter counter = new Counter();
counter.increment();
System.out.println(counter.value());
// Output: 1
```

## 2) Give a Class One Cohesive Responsibility

```java
final class Invoice {
    private final List<Integer> lineAmounts;

    Invoice(List<Integer> lineAmounts) {
        this.lineAmounts = List.copyOf(lineAmounts);
    }

    int total() {
        return lineAmounts.stream().mapToInt(Integer::intValue).sum();
    }
}

System.out.println(new Invoice(List.of(100, 50)).total());
// Output: 150
```

Calculating an invoice belongs here. Sending email, saving to a database, and rendering PDF are separate responsibilities.

## 3) Tell, Do Not Ask

Place behavior near the state whose rules it protects.

```java
final class BankAccount {
    private long balance;

    BankAccount(long openingBalance) {
        if (openingBalance < 0) {
            throw new IllegalArgumentException("openingBalance must be non-negative");
        }
        balance = openingBalance;
    }

    void withdraw(long amount) {
        if (amount <= 0 || amount > balance) {
            throw new IllegalArgumentException("invalid withdrawal");
        }
        balance -= amount;
    }

    long balance() {
        return balance;
    }
}

BankAccount account = new BankAccount(500);
account.withdraw(200);
System.out.println(account.balance());
// Output: 300
```

The account enforces its own invariant instead of exposing a writable balance.

## 4) Questions to Ask

- What responsibility does this class own?
- What state must remain valid?
- Which behavior belongs with that state?
- Can a caller put the object into an impossible state?
- Is this class doing persistence, presentation, and domain logic at once?
