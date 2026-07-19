# 11 - Fundamental Interview Traps and Practice

## Numeric Promotion and Overflow

```java
byte left = 10;
byte right = 20;
int total = left + right;
System.out.println(total);
System.out.println(Integer.MAX_VALUE + 1);
// Output:
// 30
// -2147483648
```

Integer arithmetic wraps on overflow. Use `Math.addExact` when overflow must fail.

## Wrapper Cache and Unboxing

```java
Integer a = 127;
Integer b = 127;
Integer c = 128;
Integer d = 128;
System.out.println(a == b);
System.out.println(c == d);
// Output:
// true
// false
```

Never rely on wrapper identity. Unboxing null throws `NullPointerException`.

## `switch` Expression

```java
int days = switch ("WEEK") {
    case "DAY" -> 1;
    case "WEEK" -> 7;
    default -> throw new IllegalArgumentException("unknown unit");
};
System.out.println(days);
// Output: 7
```

## `finally` Trap

Never return from `finally`; it can suppress a result or exception.

```java
static int safe() {
    try {
        return 1;
    } finally {
        System.out.println("cleanup");
    }
}
System.out.println(safe());
// Output:
// cleanup
// 1
```

## Quick Questions

- Java is pass-by-value.
- Local variables have no default value; fields do.
- `this` refers to the current object; `super` accesses parent members/constructor.
- Constructors are not inherited and cannot be abstract, static, final, or synchronized.
- Static methods are hidden, not overridden.
- Private methods are not overridden.
- `main` is public static so the launcher can invoke it without an instance.
- An interface can have abstract, default, static, and private methods.
- An abstract class may have state, constructors, and concrete methods.

## Practice

1. Predict initialization order across a three-class hierarchy.
2. Explain five differences between `String`, `StringBuilder`, and `StringBuffer`.
3. Demonstrate pass-by-value with a primitive, mutable list, and reassignment.
4. Explain `==` versus `equals` for strings, wrappers, enums, and records.
5. Package, compile, and run a class without an IDE.
