# 14 - Testing with JUnit and Mockito

## JUnit 5 Unit Test

```java
@Test
void rejectsNegativeAmount() {
    IllegalArgumentException error = assertThrows(
            IllegalArgumentException.class,
            () -> new Money("INR", -1));
    assertEquals("minorUnits must be non-negative", error.getMessage());
    // Test output: passes when invalid state fails with the expected message.
}
```

## Parameterized Test

```java
@ParameterizedTest
@ValueSource(ints = {1, 2, 10})
void acceptsPositiveValues(int value) {
    assertTrue(value > 0);
    // Test output: three successful test invocations.
}
```

## Mockito at a Boundary

```java
PaymentGateway gateway = mock(PaymentGateway.class);
when(gateway.charge(500)).thenReturn("PAY-1");

CheckoutService service = new CheckoutService(gateway);
assertEquals("PAY-1", service.checkout(500));
verify(gateway).charge(500);
// Test output: result and one gateway interaction are verified.
```

Mock unstable or slow boundaries, not simple values and every internal class. Prefer fakes when stateful behavior matters.

## Test Types

- unit: one small behavior without infrastructure
- integration: real collaboration with database, broker, filesystem, or network substitute
- contract: provider/consumer interface compatibility
- component: deployable component with controlled dependencies
- end-to-end: critical flow through the whole system

## Quality Rules

- Arrange, Act, Assert
- deterministic clocks, IDs, and random sources
- no order dependency or shared mutable fixture
- assert observable behavior and important state
- test failure, timeout, authorization, and concurrency paths
- use Testcontainers when real database/broker semantics matter
- mutation testing can reveal assertions that do not protect behavior
