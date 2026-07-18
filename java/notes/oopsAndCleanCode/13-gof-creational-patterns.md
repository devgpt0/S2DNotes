# 13 - GoF Creational Patterns

Creational patterns control object construction. Use ordinary constructors until construction has a real variation or lifecycle problem.

Do not memorize UML first. For each pattern, learn the construction problem, the smallest example, and one reason not to use it.

## 1) Singleton

A Singleton guarantees one instance per class loader and provides global access. The safest serialization-resistant implementation is an enum.

```java
enum ApplicationClock {
    INSTANCE;

    Instant now() {
        return Instant.EPOCH;
    }
}

System.out.println(ApplicationClock.INSTANCE == ApplicationClock.INSTANCE);
System.out.println(ApplicationClock.INSTANCE.now());
// Output:
// true
// 1970-01-01T00:00:00Z
```

For lazy initialization without enum semantics:

```java
final class ConfigurationRegistry {
    private ConfigurationRegistry() {}

    private static final class Holder {
        private static final ConfigurationRegistry INSTANCE = new ConfigurationRegistry();
    }

    static ConfigurationRegistry instance() {
        return Holder.INSTANCE;
    }
}

System.out.println(ConfigurationRegistry.instance() == ConfigurationRegistry.instance());
// Output: true
```

Singleton drawbacks: hidden global dependency, shared mutable state, test coupling, and one instance per class loader rather than necessarily one per process. In Spring, prefer a container-managed singleton bean injected through constructors.

## 2) Factory Method

Factory Method lets a method choose the concrete product while callers depend on its abstraction.

```java
interface Parser {
    String parse(String value);
}

static Parser parserFor(String format) {
    return switch (format) {
        case "plain" -> String::strip;
        case "upper" -> value -> value.strip().toUpperCase();
        default -> throw new IllegalArgumentException("unsupported format: " + format);
    };
}

System.out.println(parserFor("upper").parse(" java "));
// Output: JAVA
```

## 3) Abstract Factory

Abstract Factory creates a compatible family of related products.

```java
interface UiFactory {
    String button();
    String menu();
}

record DarkUiFactory() implements UiFactory {
    public String button() { return "dark-button"; }
    public String menu() { return "dark-menu"; }
}

UiFactory factory = new DarkUiFactory();
System.out.println(factory.button() + ", " + factory.menu());
// Output: dark-button, dark-menu
```

## 4) Builder

Builder names optional construction choices and validates the final object.

```java
record HttpRequestSpec(URI uri, Duration timeout) {
    static final class Builder {
        private URI uri;
        private Duration timeout = Duration.ofSeconds(3);

        Builder uri(URI value) { uri = value; return this; }
        Builder timeout(Duration value) { timeout = value; return this; }

        HttpRequestSpec build() {
            return new HttpRequestSpec(
                    Objects.requireNonNull(uri, "uri"),
                    Objects.requireNonNull(timeout, "timeout"));
        }
    }
}

HttpRequestSpec request = new HttpRequestSpec.Builder()
        .uri(URI.create("https://example.com"))
        .build();
System.out.println(request.timeout());
// Output: PT3S
```

Use a constructor or record when there are only a few required values.

## 5) Prototype

Prototype creates an object from an existing object. Prefer explicit copy methods over `Cloneable`.

```java
record ReportSettings(String title, List<String> columns) {
    ReportSettings {
        columns = List.copyOf(columns);
    }

    ReportSettings withTitle(String newTitle) {
        return new ReportSettings(newTitle, columns);
    }
}

ReportSettings original = new ReportSettings("Daily", List.of("id", "total"));
System.out.println(original.withTitle("Weekly"));
// Output: ReportSettings[title=Weekly, columns=[id, total]]
```

## Interview Comparison

- Factory Method chooses one product.
- Abstract Factory creates a compatible product family.
- Builder assembles one complex object step by step.
- Prototype copies an existing configured object.
- Singleton controls instance count but introduces global-lifecycle tradeoffs.
