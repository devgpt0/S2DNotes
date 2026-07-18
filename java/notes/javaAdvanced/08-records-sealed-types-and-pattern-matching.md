# 08 - Records, Sealed Types, and Pattern Matching

## 1) Records Are Data Carriers

Records generate accessors, a canonical constructor, `equals`, `hashCode`, and `toString`.

```java
record Money(String currency, long minorUnits) {
    Money {
        Objects.requireNonNull(currency, "currency");
        if (minorUnits < 0) {
            throw new IllegalArgumentException("minorUnits must be non-negative");
        }
    }
}

System.out.println(new Money("INR", 500));
// Output: Money[currency=INR, minorUnits=500]
```

A record is shallowly immutable. Mutable components still need defensive copies.

## 2) Sealed Hierarchies

```java
sealed interface PaymentResult permits Approved, Declined {}
record Approved(String reference) implements PaymentResult {}
record Declined(String reason) implements PaymentResult {}

static String describe(PaymentResult result) {
    return switch (result) {
        case Approved(var reference) -> "approved: " + reference;
        case Declined(var reason) -> "declined: " + reason;
    };
}

System.out.println(describe(new Approved("PAY-10")));
// Output: approved: PAY-10
```

The compiler checks that the switch covers every permitted subtype.

## 3) Pattern Matching for `instanceof`

```java
Object value = "advanced";
if (value instanceof String text && text.length() > 5) {
    System.out.println(text.toUpperCase());
}
// Output: ADVANCED
```

The pattern variable exists only where the type test is known to succeed.

## 4) Design Guidance

- Use records for transparent immutable data, not entities with identity and mutable lifecycle.
- Use sealed types when the set of domain alternatives is intentionally closed.
- Prefer exhaustive switches over a default that hides a newly added case.
- Validate record invariants in the compact constructor.
