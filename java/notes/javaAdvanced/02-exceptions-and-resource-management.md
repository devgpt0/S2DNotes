# 02 - Exceptions and Resource Management

## 1) Checked and Unchecked Exceptions

- Checked exceptions represent recoverable conditions a caller must acknowledge.
- Runtime exceptions usually represent invalid input, invalid state, or programming errors.
- Catch an exception only when the current layer can recover or add useful context.

```java
static int positive(int value) {
    if (value <= 0) {
        throw new IllegalArgumentException("value must be positive");
    }
    return value;
}

System.out.println(positive(5));
// Output: 5
```

## 2) Preserve the Cause

```java
static int parsePort(String text) {
    try {
        return Integer.parseInt(text);
    } catch (NumberFormatException exception) {
        throw new IllegalArgumentException("port must be an integer", exception);
    }
}

System.out.println(parsePort("8080"));
// Output: 8080
```

Never discard the original exception when translating it.

## 3) Try-With-Resources

Resources implementing `AutoCloseable` are closed in reverse declaration order.

```java
try (StringReader reader = new StringReader("Java")) {
    System.out.println((char) reader.read());
}
// Output: J
```

If both the body and `close()` fail, the body exception is primary and close failures are suppressed.

```java
try (var resource = new AutoCloseable() {
    @Override
    public void close() {
        System.out.println("closed");
    }
}) {
    System.out.println("used");
}
// Output:
// used
// closed
```

## 4) Domain Exceptions

Use a domain-specific exception only when callers benefit from distinguishing the failure.

```java
final class InsufficientBalanceException extends RuntimeException {
    InsufficientBalanceException(long balance, long requested) {
        super("balance=" + balance + ", requested=" + requested);
    }
}

System.out.println(new InsufficientBalanceException(100, 150).getMessage());
// Output: balance=100, requested=150
```

## 5) Rules

- Validate at boundaries and fail fast.
- Never use exceptions for normal loop control.
- Never catch `Exception` or `Throwable` unless a framework boundary requires it.
- Do not log and rethrow the same failure at every layer.
- Include actionable context, but never secrets or personal data.
