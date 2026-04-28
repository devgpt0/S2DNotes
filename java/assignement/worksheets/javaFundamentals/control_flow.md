```markdown
# Java Control Flow: Deep Dive Questions

## Level 1 — Tricky Control Flow Questions (10)

### Q1. Short-circuit vs Non-short-circuit

```java
int x = 0;
if (x != 0 && 10 / x > 1) {
    System.out.println("A");
} else {
    System.out.println("B");
}
```

**Question:** What is the output? Why? What changes if `&&` → `&`?

---

### Q2. Assignment inside condition

```java
int a = 5;
if (a = 10) {
    System.out.println("True");
}
```

**Question:** Will this compile?

---

### Q3. Switch fall-through trap

```java
int x = 2;
switch (x) {
    case 1:
        System.out.println("One");
    case 2:
        System.out.println("Two");
    case 3:
        System.out.println("Three");
        break;
    default:
        System.out.println("Default");
}
```

**Question:** Output? Explain bytecode-level fall-through behavior.

---

### Q4. Switch with String (hash-based dispatch)

```java
String s = "FB";
switch (s) {
    case "Ea":
        System.out.println("Case Ea");
        break;
    case "FB":
        System.out.println("Case FB");
        break;
}
```

**Question:** Why is this example interesting wrt hash collisions?

---

### Q5. Infinite loop subtlety

```java
for (int i = 0; i < 10; i--) {
    System.out.println(i);
}
```

**Question:** Will this terminate? What optimization might JIT apply here?

---

### Q6. Loop variable scope

```java
for (int i = 0; i < 3; i++) {}
System.out.println(i);
```

**Question:** Compile-time or runtime error? Why?

---

### Q7. Labelled break behavior

```java
outer:
for (int i = 0; i < 3; i++) {
    inner:
    for (int j = 0; j < 3; j++) {
        if (i == 1 && j == 1) break outer;
        System.out.println(i + " " + j);
    }
}
```

**Question:** Exact output sequence?

---

### Q8. do-while execution guarantee

```java
int x = 10;
do {
    System.out.println("Run");
} while (x < 5);
```

**Question:** Output and reasoning vs while loop.

---

### Q9. Ternary operator type inference

```java
Object o = true ? new Integer(1) : new Double(2.0);
System.out.println(o.getClass());
```

**Question:** What type is chosen? Why?

---

### Q10. Dead code detection

```java
while (false) {
    System.out.println("Hello");
}
```

**Question:** Compile-time or runtime issue? JVM reasoning?

---

## Level 2 — Advanced Tricky Control Flow Questions (10)

### Q1. Enhanced switch expression

```java
int x = 2;
String result = switch (x) {
    case 1 -> "One";
    case 2 -> "Two";
    default -> "Default";
};
System.out.println(result);
```

**Question:** What is the output? Can this switch be used without assigning to a variable?

---

### Q2. Switch with multiple case labels

```java
int day = 6;
switch (day) {
    case 1, 2, 3, 4, 5 -> System.out.println("Weekday");
    case 6, 7 -> System.out.println("Weekend");
}
```

**Question:** What is printed? How does the comma-separated syntax work?

---

### Q3. Switch expression exhaustiveness

```java
enum Color { RED, GREEN, BLUE }

Color c = Color.RED;
String desc = switch (c) {
    case RED -> "Stop";
    case GREEN -> "Go";
};
```

**Question:** Will this compile? Why or why not?

---

### Q4. Switch expression with yield

```java
int x = 1;
int result = switch (x) {
    case 1 -> {
        System.out.println("Processing");
        yield 10;
    }
    default -> 0;
};
System.out.println(result);
```

**Question:** What is the output? When is `yield` required?

---

### Q5. Labelled continue behavior

```java
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) continue outer;
        System.out.println(i + " " + j);
    }
}
```

**Question:** What is the exact output sequence?

---

### Q6. for loop with multiple variables and conditions

```java
for (int i = 0, j = 10; i < 5 && j > 5; i++, j--) {
    System.out.println(i + " " + j);
}
```

**Question:** What values are printed? Explain evaluation order.

---

### Q7. do-while with break and continue

```java
int i = 0;
do {
    i++;
    if (i == 3) continue;
    if (i == 5) break;
    System.out.println(i);
} while (i < 10);
```

**Question:** What is the output? Trace the control flow step by step.

---

### Q8. Ternary operator chaining

```java
int a = 5, b = 10, c = 15;
int result = a > b ? a : b > c ? b : c;
System.out.println(result);
```

**Question:** What is the output? Explain associativity rules.

---

### Q9. try-finally with return statements

```java
int test() {
    try {
        return 10;
    } finally {
        System.out.println("Finally executed");
        return 20;
    }
}

System.out.println(test());
```

**Question:** What is printed and what value is returned? Why?

---

### Q10. for-each loop modification

```java
List<Integer> list = List.of(1, 2, 3);
for (Integer x : list) {
    x = x + 10;
}
System.out.println(list);
```

**Question:** What is the output? Why can't elements be modified this way?

---

## Level 3 — Java 21 Control Flow Questions (Pattern Matching for switch) (10)

### Q1. Basic type pattern matching in switch

```java
static String describe(Object obj) {
    return switch (obj) {
        case Integer i -> "Integer: " + i;
        case String s -> "String: " + s;
        case null -> "Null value";
        default -> "Other type";
    };
}
```

**Question:** What is returned for inputs: 42, "Hello", null, 3.14? Explain how type patterns work.

---

### Q2. Guarded patterns in switch

```java
static String classify(Number n) {
    return switch (n) {
        case Integer i when i > 0 -> "Positive Integer";
        case Integer i -> "Non-positive Integer";
        case Double d when d.isNaN() -> "Not a Number";
        default -> "Other Number";
    };
}
```

**Question:** What happens for inputs: 5, -3, Double.NaN, 4.2? When are guards evaluated?

---

### Q3. Dominance rules in pattern matching

```java
static String test(Object o) {
    return switch (o) {
        case Object obj -> "Any object";
        case String s -> "String";
    };
}
```

**Question:** Will this compile? Explain dominance rules and why order matters.

---

### Q4. Exhaustiveness with sealed types

```java
sealed interface Shape permits Circle, Rectangle {}
final class Circle implements Shape {}
final class Rectangle implements Shape {}

static int area(Shape s) {
    return switch (s) {
        case Circle c -> 1;
        // case Rectangle r -> 2;
    };
}
```

**Question:** Will this compile? Why is exhaustiveness enforced here?

---

### Q5. Null handling with pattern matching

```java
static String handle(String s) {
    return switch (s) {
        case "A" -> "Alpha";
        case "B" -> "Beta";
        case null -> "Null input";
        default -> "Other";
    };
}
```

**Question:** What happens if `s = null`? How does explicit `case null` differ from default?

---

### Q6. Record patterns in switch

```java
record Point(int x, int y) {}

static String analyze(Object o) {
    return switch (o) {
        case Point(int x, int y) when x == y -> "Diagonal point";
        case Point(int x, int y) -> "Point (" + x + "," + y + ")";
        default -> "Not a point";
    };
}
```

**Question:** What is returned for `new Point(5,5)` and `new Point(3,7)`?

---

### Q7. Pattern variable scope in switch

```java
Object obj = "test";
switch (obj) {
    case String s -> System.out.println(s.length());
    default -> {}
}
System.out.println(s);  // Is this accessible?
```

**Question:** Will this compile? Explain scope of pattern variables.

---

### Q8. Combined type and constant patterns

```java
static String describe(Object o) {
    return switch (o) {
        case String s when s.equals("special") -> "Special string";
        case Integer i when i == 42 -> "The answer";
        case String s -> "Any string";
        default -> "Other";
    };
}
```

**Question:** What is returned for "special", 42, "hello", true? Explain matching order.

---

### Q9. When clause vs if-else in patterns

```java
static String check(Object o) {
    return switch (o) {
        case Integer i when i > 100 -> "Large";
        case Integer i -> "Small or negative";
        default -> "Not integer";
    };
}
```

**Question:** For input 150 and 50, what is returned? Why use `when` instead of traditional if?

---

### Q10. Switch with pattern matching as expression vs statement

```java
Object value = 42;
switch (value) {
    case Integer i when i > 0 -> System.out.println("Positive");
    case Integer i -> System.out.println("Non-positive");
    default -> System.out.println("Other");
}
```

**Question:** Is this valid as a statement? What changes if it is converted to an expression?

---

## Extra — Code Quality (Good vs Bad Control Flow) (5)

### Q11. Deep nesting vs guard clauses

**Bad:**

```java
if (user != null) {
    if (user.isActive()) {
        if (user.hasPermission()) {
            process(user);
        }
    }
}
```

**Question:** Rewrite using better control flow. Why is it superior?

---

### Q12. Magic numbers in conditions

```java
if (status == 3) {
    // process
}
```

**Question:** Why is this bad? Suggest a scalable alternative.

---

### Q13. Multiple returns debate

```java
if (x < 0) return -1;
if (x == 0) return 0;
return 1;
```

**Question:** Is multiple return good or bad in modern Java?

---

### Q14. Loop misuse vs streams

```java
List<Integer> result = new ArrayList<>();
for (int i = 0; i < list.size(); i++) {
    if (list.get(i) % 2 == 0) {
        result.add(list.get(i));
    }
}
```

**Question:** Rewrite and compare performance (stream vs loop).

---

### Q15. Exception as control flow

```java
try {
    int x = Integer.parseInt(s);
} catch (Exception e) {
    x = 0;
}
```

**Question:** Why is this considered bad in performance-critical systems?
```