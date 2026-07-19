# 11 - Code Smells and Refactoring

A smell is a signal to investigate, not automatic proof of bad code.

## 1) Long Conditional

Replace a type-code conditional with an enum or polymorphism when variants have substantial independent behavior.

```java
enum Priority {
    LOW(5), HIGH(1);

    private final int responseDays;

    Priority(int responseDays) {
        this.responseDays = responseDays;
    }

    int responseDays() {
        return responseDays;
    }
}

System.out.println(Priority.HIGH.responseDays());
// Output: 1
```

## 2) Primitive Obsession

```java
record EmailAddress(String value) {
    EmailAddress {
        if (value == null || !value.contains("@")) {
            throw new IllegalArgumentException("invalid email address");
        }
    }
}

System.out.println(new EmailAddress("team@example.com").value());
// Output: team@example.com
```

A value object centralizes rules that would otherwise be duplicated.

## 3) Feature Envy

If a method mostly reads another object’s internals, move the behavior closer to that data.

```java
record Rectangle(int width, int height) {
    int area() {
        return width * height;
    }
}

System.out.println(new Rectangle(4, 5).area());
// Output: 20
```

## 4) Common Smells

- god class: split by cohesive responsibility
- long parameter list: introduce a meaningful parameter object
- shotgun surgery: move related policy together
- duplicated logic: extract the shared concept after confirming it is truly the same
- dead code: delete it; version control preserves history
- inappropriate inheritance: replace with composition

## 5) Safe Refactoring Loop

1. Protect behavior with focused tests.
2. Make one small structural change.
3. Run tests and static analysis.
4. Repeat until the design communicates clearly.

Refactoring changes structure without changing observable behavior.
