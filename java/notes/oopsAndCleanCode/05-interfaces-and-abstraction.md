# 05 - Interfaces and Abstraction

## 1) Abstraction Exposes What, Not How

```java
interface ExchangeRateProvider {
    BigDecimal rate(String from, String to);
}

final class FixedRateProvider implements ExchangeRateProvider {
    @Override
    public BigDecimal rate(String from, String to) {
        return new BigDecimal("83.00");
    }
}

ExchangeRateProvider provider = new FixedRateProvider();
System.out.println(provider.rate("USD", "INR"));
// Output: 83.00
```

The caller depends on a stable capability, not network or database details.

## 2) Small Interfaces

```java
interface Reader<T> {
    T read();
}

Reader<String> reader = () -> "ready";
System.out.println(reader.read());
// Output: ready
```

Prefer cohesive, role-based interfaces. An interface with unrelated methods forces implementations to depend on behavior they do not need.

## 3) Default and Static Methods

```java
interface Identifier {
    String value();

    default boolean isEmpty() {
        return value().isEmpty();
    }

    static Identifier of(String value) {
        return () -> value;
    }
}

System.out.println(Identifier.of("ID-1").isEmpty());
// Output: false
```

Default methods help evolve an interface, but should not accumulate unrelated business logic.

## 4) Abstract Class vs Interface

Use an interface for a capability that unrelated types may implement. Use an abstract class when closely related types share protected state or a carefully designed template. Prefer neither when one concrete class is sufficient.
