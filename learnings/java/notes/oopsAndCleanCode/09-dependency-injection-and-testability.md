# 09 - Dependency Injection and Testability

## 1) Constructor Injection

```java
interface PaymentGateway {
    String charge(int amount);
}

final class CheckoutService {
    private final PaymentGateway gateway;

    CheckoutService(PaymentGateway gateway) {
        this.gateway = Objects.requireNonNull(gateway);
    }

    String checkout(int amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("amount must be positive");
        }
        return gateway.charge(amount);
    }
}

PaymentGateway fake = amount -> "charged:" + amount;
System.out.println(new CheckoutService(fake).checkout(500));
// Output: charged:500
```

Constructor injection makes required dependencies explicit and prevents partially initialized objects.

## 2) Inject Sources of Nondeterminism

```java
final class TokenExpiry {
    private final Clock clock;

    TokenExpiry(Clock clock) {
        this.clock = clock;
    }

    Instant expiresAt() {
        return Instant.now(clock).plusSeconds(300);
    }
}

Clock fixed = Clock.fixed(Instant.EPOCH, ZoneOffset.UTC);
System.out.println(new TokenExpiry(fixed).expiresAt());
// Output: 1970-01-01T00:05:00Z
```

Useful injected boundaries include clocks, random generators, repositories, gateways, and message publishers.

## 3) Test Behavior, Not Implementation

```java
List<Integer> chargedAmounts = new ArrayList<>();
PaymentGateway recordingGateway = amount -> {
    chargedAmounts.add(amount);
    return "ok";
};
new CheckoutService(recordingGateway).checkout(250);
System.out.println(chargedAmounts);
// Output: [250]
```

Do not expose private methods solely for testing. Verify observable outcomes through the public contract.

## 4) Avoid Service Locator

Fetching dependencies from global static state hides requirements, complicates tests, and introduces ordering problems. Pass required collaborators explicitly.
