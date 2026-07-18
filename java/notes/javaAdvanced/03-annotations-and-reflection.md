# 03 - Annotations and Reflection

## Beginner Meaning

An annotation is a structured label attached to code. Reflection is Java code looking at classes, methods, and fields while the program is running. Frameworks such as Spring use both to discover components and configuration.

Ordinary business code should still call methods normally. Reflection is mainly framework/tool infrastructure.

## 1) Annotation Metadata

Annotations attach structured metadata to program elements.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@interface Feature {
    String value();
}

@Feature("payments")
final class PaymentService {}

Feature feature = PaymentService.class.getAnnotation(Feature.class);
System.out.println(feature.value());
// Output: payments
```

Retention choices:

- `SOURCE`: discarded by the compiler.
- `CLASS`: stored in bytecode, not available through normal runtime reflection.
- `RUNTIME`: available through reflection.

## 2) Inspecting Types

```java
record Customer(long id, String name) {}

Class<Customer> type = Customer.class;
System.out.println(type.isRecord());
System.out.println(type.getRecordComponents()[0].getName());
// Output:
// true
// id
```

## 3) Safe Reflective Construction

```java
final class Report {
    public Report() {}
}

Report report = Report.class.getDeclaredConstructor().newInstance();
System.out.println(report.getClass().getSimpleName());
// Output: Report
```

Prefer `getDeclaredConstructor().newInstance()` over deprecated `Class.newInstance()`.

## 4) Calling a Method

```java
Method method = String.class.getMethod("substring", int.class);
System.out.println(method.invoke("advanced", 3));
// Output: anced
```

Reflection failures are explicit: missing members, illegal access, and exceptions thrown by invoked code are different failures.

## 5) When to Use Reflection

Good uses include framework infrastructure, serializers, test tools, and plugin discovery. Ordinary business logic should use normal method calls because they are safer, faster, and easier to refactor.

Security rules:

- Never let untrusted input choose an arbitrary class or method.
- Avoid opening private members unless the framework truly requires it.
- Validate annotation values before using them in paths, queries, or commands.
