# 07 - Arrays, Varargs, Enums, and Operators

## Arrays

Arrays have fixed length, are objects, and are covariant.

```java
int[] values = {10, 20, 30};
System.out.println(values.length);
System.out.println(Arrays.toString(values));
// Output:
// 3
// [10, 20, 30]
```

Array covariance can fail at runtime:

```java
Number[] numbers = new Integer[1];
try {
    numbers[0] = 1.5;
} catch (ArrayStoreException exception) {
    System.out.println(exception.getClass().getSimpleName());
}
// Output: ArrayStoreException
```

Generics are invariant and catch the comparable mistake at compile time.

## Varargs

```java
static int sum(int... values) {
    return Arrays.stream(values).sum();
}
System.out.println(sum(1, 2, 3));
// Output: 6
```

Varargs are arrays. They must be the last parameter. Generic varargs may cause heap pollution; use `@SafeVarargs` only when the method is genuinely safe.

## Enums

```java
enum Status {
    NEW(false), COMPLETE(true);
    private final boolean terminal;
    Status(boolean terminal) { this.terminal = terminal; }
    boolean isTerminal() { return terminal; }
}
System.out.println(Status.COMPLETE.isTerminal());
// Output: true
```

Enums can have fields, methods, interfaces, and constant-specific behavior. Compare enum constants with `==`.

## Operator Traps

```java
int value = 5;
System.out.println(value++);
System.out.println(value);
System.out.println(5 / 2);
System.out.println(5 / 2.0);
// Output:
// 5
// 6
// 2
// 2.5
```

`&&` and `||` short-circuit; `&` and `|` always evaluate both boolean operands.

```java
int x = 0;
boolean result = false && ++x > 0;
System.out.println(result + ", " + x);
// Output: false, 0
```
