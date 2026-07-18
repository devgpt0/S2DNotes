# 18 - Common Advanced Java Code Snippets and Solved Questions

## 1) Generic Maximum

```java
static <T extends Comparable<? super T>> T maximum(List<T> values) {
    if (values.isEmpty()) throw new IllegalArgumentException("values must not be empty");
    T maximum = values.getFirst();
    for (T value : values) {
        if (value.compareTo(maximum) > 0) maximum = value;
    }
    return maximum;
}

System.out.println(maximum(List.of(3, 9, 4)));
// Output: 9
```

The `? super T` bound accepts comparison contracts implemented by a supertype.

## 2) Read a File and Count Words

```java
Path file = Files.createTempFile("words-", ".txt");
Files.writeString(file, "Java stream Java", StandardCharsets.UTF_8);
try (Stream<String> lines = Files.lines(file, StandardCharsets.UTF_8)) {
    long count = lines.flatMap(line -> Arrays.stream(line.split("\\s+")))
            .filter(word -> !word.isEmpty())
            .count();
    System.out.println(count);
}
Files.delete(file);
// Output: 3
```

Try-with-resources closes the file-backed stream.

## 3) Strict Date Parsing

```java
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("uuuu-MM-dd")
        .withResolverStyle(ResolverStyle.STRICT);
System.out.println(LocalDate.parse("2024-02-29", formatter));
try {
    LocalDate.parse("2023-02-29", formatter);
} catch (DateTimeParseException error) {
    System.out.println("invalid date");
}
// Output:
// 2024-02-29
// invalid date
```

## 4) Custom Runtime Annotation and Reflection

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@interface Role { String value(); }

@Role("admin")
final class AdminService {}

Role role = AdminService.class.getAnnotation(Role.class);
System.out.println(role.value());
// Output: admin
```

Interview point: runtime retention is required for ordinary reflection.

## 5) Safe Upload Path Resolution

```java
static Path resolveInside(Path root, String requested) {
    Path normalizedRoot = root.toAbsolutePath().normalize();
    Path result = normalizedRoot.resolve(requested).normalize();
    if (!result.startsWith(normalizedRoot)) {
        throw new IllegalArgumentException("path escapes root");
    }
    return result;
}

System.out.println(resolveInside(Path.of("uploads"), "images/a.png").getFileName());
// Output: a.png
```

Security-sensitive writes must also account for symbolic links and permissions.

## 6) Build an HTTP Request with Deadlines

```java
HttpClient client = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(2))
        .build();
HttpRequest request = HttpRequest.newBuilder(URI.create("https://example.com/api"))
        .timeout(Duration.ofSeconds(3))
        .header("Accept", "application/json")
        .GET()
        .build();
System.out.println(request.method() + ", " + request.timeout().orElseThrow());
// Output: GET, PT3S
```

## 7) Sealed Result and Exhaustive Switch

```java
sealed interface Result permits Success, Failure {}
record Success(String value) implements Result {}
record Failure(String message) implements Result {}

static String describe(Result result) {
    return switch (result) {
        case Success(var value) -> "success:" + value;
        case Failure(var message) -> "failure:" + message;
    };
}
System.out.println(describe(new Success("ready")));
// Output: success:ready
```

## 8) Exact Money Total

```java
BigDecimal total = Stream.of("10.25", "20.75")
        .map(BigDecimal::new)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
System.out.println(total);
// Output: 31.00
```

Never construct money from a binary floating-point value.

## Most-Asked Advanced Java Questions

1. Type erasure? Generic type arguments are mostly removed/bridged at runtime; compile-time safety remains.
2. PECS? Producer extends, consumer super.
3. Checked vs unchecked exception? Compiler-enforced recoverable contract vs runtime invalid state/programming/domain failure.
4. Why try-with-resources? Deterministic reverse-order closing with suppressed-close failure support.
5. Reflection drawback? Runtime failure, weaker refactoring safety, access/module/performance complexity.
6. Record limitations? Shallow immutability; unsuitable for every identity/mutable lifecycle entity.
7. Sealed type benefit? Closed alternatives and exhaustive switches.
8. `Instant` vs `LocalDateTime`? UTC timeline point vs date-time without zone/offset.
9. Serialization risk? Native deserialization can construct dangerous object graphs; never accept untrusted bytes.
10. ClassNotFoundException vs NoClassDefFoundError? Explicit loading failure vs class expected by executing compiled code could not be defined.
11. Soft vs weak reference? Memory-pressure-sensitive vs cleared when only weakly reachable; neither is a predictable cache policy.
12. JIT? Runtime compilation/optimization of hot paths using profiling.
13. Java module `exports` vs `opens`? Normal compile/runtime access vs deep reflection access.
14. `BigDecimal.equals` vs compareTo? Equals includes scale; compareTo compares numeric value.
15. Why inject Clock? Deterministic time-dependent behavior and tests.
