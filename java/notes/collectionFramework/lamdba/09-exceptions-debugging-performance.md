# 09 - Lambda Errors, Debugging, and Performance

## Start with the Main Idea

A lambda follows the same error rules as ordinary Java code.

The confusing part is that common functional interfaces such as `Function` and `Consumer` do not allow checked exceptions in their method signatures.

Do not memorize that sentence yet. Start with the example.

## The Problem

Reading a file can fail with `IOException`:

```java
String content = Files.readString(path);
```

This ordinary method can declare `throws IOException`. But this lambda does not compile:

```java
// paths.forEach(path -> Files.readString(path));
```

`forEach` expects a `Consumer`. `Consumer.accept(...)` does not declare `IOException`, so the checked exception cannot leave the lambda directly.

## Learn These Four Words

- **checked exception:** Java forces the caller to catch it or declare it
- **unchecked exception:** runtime exception Java does not force into a method signature
- **cause:** the original exception stored inside a new exception
- **stack trace:** list of calls that shows how execution reached a failure

## Complete Runnable Failure Example

```java
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class LambdaErrorDemo {
    public static void main(String[] args) {
        List<Path> paths = List.of(Path.of("missing-course.txt"));

        try {
            paths.forEach(path -> printFile(path));
        } catch (UncheckedIOException exception) {
            System.out.println(exception.getMessage());
            System.out.println(exception.getCause().getClass().getSimpleName());
        }
    }

    private static void printFile(Path path) {
        try {
            System.out.println(Files.readString(path));
        } catch (IOException exception) {
            throw new UncheckedIOException(
                    "Could not read " + path.getFileName(),
                    exception);
        }
    }
}
// Output:
// Could not read missing-course.txt
// NoSuchFileException
```

## Understand the Flow

1. `forEach` gives one path to `printFile`.
2. `Files.readString` fails because the file is missing.
3. `catch (IOException exception)` receives the original failure.
4. `UncheckedIOException` adds a useful application message.
5. The original exception is passed as the cause; it is not lost.
6. The outer `catch` handles the failure because this small demo can show it to the learner.

In a real application, catch the exception only where you can make a real decision: return an error response, stop a job, retry a safe transient operation, or report the failure.

## What Not to Do

```java
// Bad: hides the failure and invents fake data.
try {
    return Files.readString(path);
} catch (IOException exception) {
    return "";
}
```

The caller cannot tell an empty file from a failed read.

Also avoid catching broad `Exception` when only `IOException` is expected.

## A Simple Debugging Method

When a lambda chain produces the wrong result, make the steps visible:

```java
List<String> rawNames = List.of(" Asha ", "", " Ravi ");

for (String rawName : rawNames) {
    String cleanName = rawName.trim();
    System.out.printf("before='%s', after='%s'%n", rawName, cleanName);
}
// Output:
// before=' Asha ', after='Asha'
// before='', after=''
// before=' Ravi ', after='Ravi'
```

Use this order:

1. write down the input
2. split a long chain into named steps
3. print temporary intermediate values in a local learning program
4. find the first value that differs from your prediction
5. add a test that reproduces the bug
6. remove temporary production prints after the test protects the fix

## `peek` Is Not Business Logic

`peek` can temporarily show stream values:

```java
List<String> names = rawNames.stream()
        .map(String::trim)
        .peek(System.out::println)
        .filter(name -> !name.isEmpty())
        .toList();
```

Do not use `peek` for required saving, auditing, or mutation. A stream pipeline should not depend on debug observation for correctness.

## Make Complex Lambdas Easy to Debug

Harder to read:

```java
orders.stream().filter(order -> order.paid() && !order.cancelled() && order.total() > 0).toList();
```

Easier to read and test:

```java
orders.stream().filter(this::isReadyForShipping).toList();
```

The named method explains *why* the condition exists.

## Performance: Do Not Guess

A shorter lambda is not automatically faster. A loop is not automatically faster either.

Follow this order:

1. make the result correct
2. measure with realistic data
3. find the actual slow part
4. change one thing
5. measure again

Useful tools:

- Java Flight Recorder for application behavior
- JDK Mission Control for reading recordings
- JMH for reliable small Java benchmarks

## Performance Terms in Easy Language

- **boxing:** turning `int` into an `Integer` object
- **allocation:** creating an object
- **hot path:** code that runs often enough to affect performance
- **benchmark warm-up:** allowing the JVM to optimize code before measuring it

Primitive streams can avoid boxing in numeric work:

```java
int total = IntStream.of(10, 20, 30).sum();
System.out.println(total);
// Output: 60
```

Use this because it expresses numeric work well. Claim a speed improvement only after measurement.

## Developer-Level Rules

- catch only the exception you can handle
- keep the original cause when translating an exception
- add useful context without secrets or personal data
- use named methods for multi-step rules
- keep side effects out of `map`, `filter`, and `peek`
- do not mutate shared data from a parallel stream

## Expert Understanding

- checked-exception compatibility comes from the functional interface method
- a custom “throwing function” can be useful at a real API boundary, but do not create wrappers for every lambda
- benchmark results need JVM version, warm-up, data size, and environment
- allocation or boxing matters only when measurement shows it is material
- parallel work needs safe ownership and enough work to repay coordination cost

## Quick Memory Card

- lambdas follow normal exception rules
- common functional interfaces do not declare checked exceptions
- never hide a failure or lose its cause
- debug by naming and observing small steps
- `peek` is for observation, not required behavior
- measure before optimizing

## Practice

Create `course.txt` containing `Java`, change the path, and run the example again.

Expected output:

```text
Java
```

Explain why the failure output disappears: the read succeeds, so neither catch block runs.
