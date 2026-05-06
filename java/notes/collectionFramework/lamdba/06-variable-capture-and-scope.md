# 06 - Variable Capture and Scope

## 1) Effective Final Rule

Lambda can capture local variables only if they are final or effectively final.

```java
int base = 10;
Function<Integer, Integer> addBase = x -> x + base; // OK
// base = 20; // not allowed after capture
```

## 2) Why This Rule Exists

Local variables live on stack, lambda may outlive method call.
Java captures value snapshot, so mutation is restricted.

## 3) Instance and Static Fields

Fields can be read/write inside lambda (normal object rules apply).

```java
class Counter {
    int count = 0;
    Runnable r = () -> count++;
}
```

## 4) Shadowing

Lambda cannot redeclare a local variable with same name from enclosing scope.

## 5) Thread Safety Note

Captured mutable objects can still create concurrency bugs.
Prefer immutable data or synchronization in concurrent contexts.

