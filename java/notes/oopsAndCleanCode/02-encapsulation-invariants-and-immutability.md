# 02 - Encapsulation, Invariants, and Immutability

## 1) Encapsulation Protects Rules

Encapsulation is not merely making fields private. It exposes operations that keep the object valid.

```java
final class Percentage {
    private final int value;

    Percentage(int value) {
        if (value < 0 || value > 100) {
            throw new IllegalArgumentException("percentage must be between 0 and 100");
        }
        this.value = value;
    }

    int value() {
        return value;
    }
}

System.out.println(new Percentage(80).value());
// Output: 80
```

## 2) Defensive Copies

```java
final class Schedule {
    private final List<String> tasks;

    Schedule(List<String> tasks) {
        this.tasks = List.copyOf(tasks);
    }

    List<String> tasks() {
        return tasks;
    }
}

List<String> source = new ArrayList<>(List.of("review"));
Schedule schedule = new Schedule(source);
source.add("deploy");
System.out.println(schedule.tasks());
// Output: [review]
```

Copy mutable inputs and do not leak mutable internals.

## 3) Immutable State Transitions

```java
record Cart(int itemCount) {
    Cart {
        if (itemCount < 0) {
            throw new IllegalArgumentException("itemCount must be non-negative");
        }
    }

    Cart addItem() {
        return new Cart(itemCount + 1);
    }
}

Cart empty = new Cart(0);
Cart updated = empty.addItem();
System.out.println(empty.itemCount() + " -> " + updated.itemCount());
// Output: 0 -> 1
```

## 4) Benefits

- invalid states are rejected at construction
- immutable objects are naturally easier to share across threads
- reasoning and testing become simpler
- hash-based collection behavior stays stable

Immutability is not mandatory for every entity. Use controlled mutation when identity and lifecycle are fundamental.
