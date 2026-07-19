# 14 - GoF Structural Patterns

Structural patterns organize relationships between objects and interfaces.

Simple question: “How should these objects be connected?” Adapter changes a shape, Decorator adds a layer, Proxy controls access, Facade simplifies, Composite builds a tree, Bridge separates dimensions, and Flyweight shares reusable state.

## 1) Adapter

```java
interface TemperatureCelsius { double value(); }

double fahrenheit = 86;
TemperatureCelsius adapter = () -> (fahrenheit - 32) * 5 / 9;
System.out.println(adapter.value());
// Output: 30.0
```

Adapter changes an interface; it does not add business behavior.

## 2) Bridge

Bridge separates an abstraction from an implementation dimension.

```java
interface Renderer { String render(String text); }
record HtmlRenderer() implements Renderer {
    public String render(String text) { return "<p>" + text + "</p>"; }
}
record Report(Renderer renderer) {
    String output() { return renderer.render("ready"); }
}

System.out.println(new Report(new HtmlRenderer()).output());
// Output: <p>ready</p>
```

## 3) Composite

Composite treats one object and a group uniformly.

```java
interface Cost { int amount(); }
record Item(int amount) implements Cost {}
record Bundle(List<Cost> children) implements Cost {
    public int amount() { return children.stream().mapToInt(Cost::amount).sum(); }
}

System.out.println(new Bundle(List.of(new Item(10), new Item(20))).amount());
// Output: 30
```

## 4) Decorator

Decorator wraps an object to add behavior while preserving its interface.

```java
interface Message { String text(); }
Message base = () -> "java";
Message uppercase = () -> base.text().toUpperCase();
Message bracketed = () -> "[" + uppercase.text() + "]";
System.out.println(bracketed.text());
// Output: [JAVA]
```

## 5) Facade

Facade provides a small entry point to a larger subsystem.

```java
final class CheckoutFacade {
    String checkout(int amount) {
        if (amount <= 0) throw new IllegalArgumentException("amount must be positive");
        return "paid-and-notified:" + amount;
    }
}

System.out.println(new CheckoutFacade().checkout(500));
// Output: paid-and-notified:500
```

## 6) Flyweight

Flyweight shares immutable intrinsic state between many logical objects.

```java
Map<String, String> symbols = new ConcurrentHashMap<>();
String first = symbols.computeIfAbsent("warning", String::toUpperCase);
String second = symbols.computeIfAbsent("warning", String::toUpperCase);
System.out.println(first == second);
// Output: true
```

Cache ownership, bounds, and eviction remain design responsibilities.

## 7) Proxy

Proxy controls access to another object, for example authorization, lazy loading, caching, or remote access.

```java
interface Document { String read(); }
Document target = () -> "content";
Document authorizedProxy = () -> {
    boolean allowed = true;
    if (!allowed) throw new SecurityException("denied");
    return target.read();
};
System.out.println(authorizedProxy.read());
// Output: content
```

## Interview Comparison

- Adapter changes an incompatible interface.
- Decorator adds behavior through wrapping.
- Proxy controls access while presenting the same contract.
- Facade simplifies a subsystem.
- Bridge separates two independently varying dimensions.
- Composite models part-whole trees.
- Flyweight shares immutable reusable state.
