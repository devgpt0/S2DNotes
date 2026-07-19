# Advanced Java in Simple Words

“Advanced Java” is not one feature. It is the set of tools needed to build safe real programs after learning the language basics.

## What This Module Adds

- generics: reusable code with compile-time type safety
- exceptions and resources: fail clearly and release files or connections
- files and data exchange: communicate outside the process
- annotations and reflection: inspect metadata at runtime
- date and time: model time correctly
- records and sealed types: model data shapes
- JVM, GC, and JIT: understand runtime behavior
- testing: prove behavior and protect changes
- networking and JDBC: work with external systems safely

## Generics

```java
static <T> T first(List<T> values) {
    if (values.isEmpty()) {
        throw new IllegalArgumentException("values cannot be empty");
    }
    return values.getFirst();
}

System.out.println(first(List.of("Java", "SQL")));
// Output: Java
```

`T` means the method works with one consistent element type chosen by the caller.

## Exceptions and Resources

```java
try (BufferedReader reader = Files.newBufferedReader(path)) {
    System.out.println(reader.readLine());
}
```

Try-with-resources closes the reader whether reading succeeds or fails. Catch only failures you can handle.

## Files

```java
Path path = Path.of("course.txt");
Files.writeString(path, "Java");
System.out.println(Files.readString(path));
// Output: Java
```

Validate file paths when they include external input. Never allow an input path to escape an approved storage root.

## Date and Time

```java
LocalDate start = LocalDate.of(2026, 7, 19);
System.out.println(start.plusDays(7));
// Output: 2026-07-26
```

Use `LocalDate` for a date without time or zone. Use `Instant` for a machine timestamp. Use `ZonedDateTime` when human time-zone rules matter.

## Records

```java
record Course(String id, String title) {
    Course {
        if (id.isBlank() || title.isBlank()) {
            throw new IllegalArgumentException("id and title are required");
        }
    }
}

System.out.println(new Course("java-1", "Java"));
// Output: Course[id=java-1, title=Java]
```

A record is a concise data-focused class. It can still validate its rules.

## JVM in Plain Language

1. `javac` compiles source into bytecode.
2. The JVM loads and verifies classes.
3. The JVM interprets or compiles frequently used code.
4. Objects normally live in managed heap memory.
5. Garbage collection reclaims unreachable objects.

Do not tune garbage collection from guesses. Measure the application with realistic load and Java Flight Recorder.

## Testing

A good test describes behavior:

```java
@Test
void rejectsEmptyCourseId() {
    assertThrows(IllegalArgumentException.class, () -> new Course("", "Java"));
}
```

Tests should be deterministic, focused, and independent of execution order.

## Networking and Databases

External calls need validated input, timeouts, safe credentials, parameterized SQL, clear transactions, limited safe retries, and useful metrics.

## Beginner to Expert Path

1. **Beginner:** use one API correctly in a small runnable example.
2. **Developer:** validate inputs, handle resources, and write tests.
3. **Senior:** design boundaries, transactions, and failure behavior.
4. **Expert:** understand runtime tradeoffs, diagnose with evidence, and evolve APIs safely.

Read the numbered chapters in order. Skip JVM tuning and migration details until the basic APIs and tests feel natural.
