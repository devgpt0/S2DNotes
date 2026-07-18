# 10 - Essential Design Patterns

Patterns name recurring designs. Use one only when it makes the current solution simpler.

## 1) Strategy

```java
interface ShippingCost {
    int calculate(int weightKg);
}

ShippingCost standard = weight -> weight * 10;
ShippingCost express = weight -> weight * 25;
System.out.println(standard.calculate(2) + ", " + express.calculate(2));
// Output: 20, 50
```

## 2) Factory Method

```java
enum Format { CSV, JSON }

static String fileExtension(Format format) {
    return switch (format) {
        case CSV -> ".csv";
        case JSON -> ".json";
    };
}

System.out.println(fileExtension(Format.JSON));
// Output: .json
```

A simple switch is often enough; do not build a factory hierarchy unnecessarily.

## 3) Decorator

```java
interface TextSource {
    String read();
}

TextSource source = () -> "java";
TextSource uppercase = () -> source.read().toUpperCase();
System.out.println(uppercase.read());
// Output: JAVA
```

## 4) Observer

```java
List<Consumer<String>> listeners = new ArrayList<>();
listeners.add(event -> System.out.println("received:" + event));
listeners.forEach(listener -> listener.accept("ORDER_CREATED"));
// Output: received:ORDER_CREATED
```

Define failure, ordering, and unsubscribe behavior in production event systems.

## 5) Adapter

```java
interface TemperatureCelsius {
    double value();
}

double fahrenheit = 86;
TemperatureCelsius adapter = () -> (fahrenheit - 32) * 5 / 9;
System.out.println(adapter.value());
// Output: 30.0
```

Also know Builder for many optional construction parameters, Template Method for a stable algorithm skeleton, and Command for representing actions. Prefer records, lambdas, and ordinary constructors when they already solve the problem.
