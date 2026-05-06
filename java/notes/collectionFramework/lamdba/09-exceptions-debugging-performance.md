# 09 - Exceptions, Debugging, Performance

## 1) Checked Exceptions Problem

Most functional interfaces do not declare checked exceptions.

Pattern 1: handle inside lambda

```java
list.forEach(s -> {
    try {
        riskyIO(s);
    } catch (IOException e) {
        throw new UncheckedIOException(e);
    }
});
```

Pattern 2: create wrapper utility for cleaner code.

## 2) Debugging Tips

- break long stream chains into steps
- use `peek` only for temporary debugging
- extract lambda into named method when logic grows

## 3) Performance Guidelines

- avoid unnecessary object creation in hot lambdas
- prefer primitive functional interfaces for numeric heavy work
- avoid boxing/unboxing loops where possible

## 4) Readability Rule

If lambda is more than a few lines or has branching, extract method:

```java
list.stream().filter(this::isEligible).map(this::toDto).toList();
```

## 5) Common Mistakes

- modifying shared state from parallel stream
- side effects in `map`/`filter`
- assuming stream order in parallel mode without need

