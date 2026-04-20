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

**Question:** Will this compile? Compare with C/C++ behavior.

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


# Java Control Flow — Level 2 (Java 21 Focus)

## Advanced Tricky Questions (10)

### Q1. Switch pattern matching with guards
```java
static String test(Object o) {
    return switch (o) {
        case Integer i when i > 0 -> "Positive Int";
        case Integer i -> "Non-positive Int";
        case null -> "Null";
        default -> "Other";
    };
}

What happens for input: 5, -1, null, "test"?

Explain guard evaluation order.



---

Q2. Dominance in pattern matching

static String test(Object o) {
    return switch (o) {
        case Object obj -> "Object";
        case String s -> "String";
    };
}

Will this compile?

Explain dominance rules in switch patterns.



---

Q3. Exhaustiveness in switch expressions

sealed interface Shape permits Circle, Square {}
final class Circle implements Shape {}
final class Square implements Shape {}

static int test(Shape s) {
    return switch (s) {
        case Circle c -> 1;
    };
}

Will this compile?

Why is exhaustiveness important?



---

Q4. Record pattern matching

record Point(int x, int y) {}

static String test(Object o) {
    return switch (o) {
        case Point(int x, int y) when x == y -> "Diagonal";
        case Point(int x, int y) -> "Point";
        default -> "Other";
    };
}

What happens for new Point(2,2) vs new Point(2,3)?



---

Q5. Null handling in switch

static String test(String s) {
    return switch (s) {
        case "A" -> "Alpha";
        case "B" -> "Beta";
        default -> "Other";
    };
}

What happens if s = null?

How to handle safely in Java 21?



---

Q6. Pattern variable scope

if (obj instanceof String s) {
    System.out.println(s.length());
}
System.out.println(s);

Will this compile?

Explain scope rules.



---

Q7. Guarded pattern fall-through

static String test(Object o) {
    return switch (o) {
        case Integer i when i > 10 -> "Big";
        case Integer i -> "Small";
        default -> "Other";
    };
}

What happens for i = 10?

Why?



---

Q8. for-each vs indexed loop mutation

List<Integer> list = List.of(1, 2, 3);
for (Integer x : list) {
    x++;
}
System.out.println(list);

What is the output?

Why does mutation not persist?



---

Q9. try-with-resources control flow

class A implements AutoCloseable {
    public void close() {
        System.out.println("close");
    }
}

try (A a = new A()) {
    System.out.println("try");
    return;
}

What is printed?

Order of execution?



---

Q10. Virtual threads + control flow

Thread.startVirtualThread(() -> {
    for (int i = 0; i < 3; i++) {
        System.out.println(i);
    }
});
System.out.println("Main");

Possible output order?

Does control flow guarantee ordering?



---

Code Quality & Control Flow Patterns (5)

Q11. Pattern matching vs instanceof chain

if (obj instanceof Integer) {
    Integer i = (Integer) obj;
} else if (obj instanceof String) {
    String s = (String) obj;
}

Rewrite using Java 21 pattern matching.

Why is it better?



---

Q12. Switch vs polymorphism

switch (shape) {
    case "CIRCLE": drawCircle(); break;
    case "SQUARE": drawSquare(); break;
}

Why is this design poor?

Suggest a better approach.



---

Q13. Overuse of default in switch

switch (day) {
    case MONDAY -> work();
    default -> rest();
}

Why can this hide bugs?

Improve using exhaustive handling.



---

Q14. Control flow with Optional

if (value != null) {
    process(value);
}

Rewrite using Optional.

Trade-offs?



---

Q15. Imperative vs declarative flow

List<Integer> result = new ArrayList<>();
for (int x : list) {
    if (x > 10) {
        result.add(x);
    }
}

Rewrite using modern Java constructs.

Performance considerations?