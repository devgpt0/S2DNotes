# Java Control Flow - Beginner to Interview Level

Control flow means **the order in which Java runs statements**.

Normally Java runs from top to bottom. Conditions, loops, and jump statements can change that order.

## 1) `if`, `else if`, and `else`

Use an `if` statement when code should run only when a boolean condition is true.

```java
int age = 20;
if (age >= 18) {
    System.out.println("adult");
} else {
    System.out.println("minor");
}
// Output: adult
```

Java conditions must be boolean. `if (age = 18)` does not compile because the assignment produces an `int`, not a boolean.

## 2) Boolean Operators

- `&&`: both conditions must be true
- `||`: at least one condition must be true
- `!`: reverses true/false

`&&` and `||` short-circuit. Java skips the right side when the result is already known.

```java
int divisor = 0;
boolean safe = divisor != 0 && 10 / divisor > 1;
System.out.println(safe);
// Output: false
// The division is skipped, so no ArithmeticException occurs.
```

Boolean `&` and `|` evaluate both sides. Use them only when that behavior is intentional.

## 3) Classic `switch`

`switch` selects a branch from one value.

```java
int day = 2;
switch (day) {
    case 1:
        System.out.println("Monday");
        break;
    case 2:
        System.out.println("Tuesday");
        break;
    default:
        System.out.println("Unknown");
}
// Output: Tuesday
```

Without `break`, classic cases fall through into following cases.

## 4) Modern `switch` Expression

Arrow cases do not fall through and a switch expression can return a value.

```java
String type = "ADMIN";
int permissionLevel = switch (type) {
    case "ADMIN" -> 10;
    case "USER" -> 1;
    default -> 0;
};
System.out.println(permissionLevel);
// Output: 10
```

A switch expression must cover every possible input, usually with `default` or a complete sealed/enum type.

## 5) `for` Loop

Use `for` when initialization, condition, and update naturally belong together.

```java
for (int i = 1; i <= 3; i++) {
    System.out.println(i);
}
// Output:
// 1
// 2
// 3
```

Order: initialize once -> test condition -> run body -> update -> test again.

## 6) `while` and `do-while`

`while` checks before running. `do-while` runs once before checking.

```java
int value = 5;
while (value < 5) {
    System.out.println("while");
}
do {
    System.out.println("do-while");
} while (value < 5);
// Output: do-while
```

## 7) Enhanced `for` Loop

Use it to read every array or collection element when the index is unnecessary.

```java
for (String name : List.of("Asha", "Ravi")) {
    System.out.println(name);
}
// Output:
// Asha
// Ravi
```

Reassigning `name` would not replace the list element. The loop variable receives one copied value/reference per iteration.

## 8) `break`, `continue`, and `return`

- `break`: leave the nearest loop or classic switch
- `continue`: skip to the next loop iteration
- `return`: leave the current method

```java
for (int i = 1; i <= 5; i++) {
    if (i == 2) continue;
    if (i == 4) break;
    System.out.println(i);
}
// Output:
// 1
// 3
```

Labels can target an outer loop, but they are rarely needed and can make code harder to follow.

## 9) Ternary Operator

Use `condition ? valueWhenTrue : valueWhenFalse` for a small value choice.

```java
int score = 70;
String result = score >= 40 ? "pass" : "fail";
System.out.println(result);
// Output: pass
```

Prefer `if` when branches perform multiple actions.

## 10) `try` and `finally`

`finally` normally runs before control leaves the `try`, including after `return`, `break`, or an exception.

```java
static int answer() {
    try {
        return 42;
    } finally {
        System.out.println("cleanup");
    }
}
System.out.println(answer());
// Output:
// cleanup
// 42
```

Never return from `finally`; it can hide an earlier result or exception.

## 11) Clean Control Flow

- handle invalid input early with a guard clause
- avoid deep nesting
- give conditions meaningful method names
- use enums instead of unexplained numeric/string codes
- choose a loop when it reads more clearly than a stream
- never use exceptions as normal loop control

## Interview Checklist

Be able to predict short-circuiting, loop order, classic switch fall-through, modern switch exhaustiveness, `break`/`continue`, `do-while`, and `finally` behavior.
