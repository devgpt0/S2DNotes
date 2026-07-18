# 18 - Common OOP and Design Pattern Code Questions with Solutions

## 1) Create an Immutable Class

```java
final class Student {
    private final String name;
    private final List<String> skills;

    Student(String name, List<String> skills) {
        this.name = Objects.requireNonNull(name);
        this.skills = List.copyOf(skills);
    }

    String name() { return name; }
    List<String> skills() { return skills; }
}

List<String> source = new ArrayList<>(List.of("Java"));
Student student = new Student("Asha", source);
source.add("SQL");
System.out.println(student.skills());
// Output: [Java]
```

Required points: final class/fields, constructor validation, defensive copy, no mutators, no mutable-state leak.

## 2) Thread-Safe Singleton

```java
enum ApplicationSettings {
    INSTANCE;
    String mode() { return "production"; }
}
System.out.println(ApplicationSettings.INSTANCE.mode());
System.out.println(ApplicationSettings.INSTANCE == ApplicationSettings.INSTANCE);
// Output:
// production
// true
```

In Spring applications, constructor-injected singleton-scoped beans usually provide clearer ownership and testing.

## 3) Strategy Pattern

```java
interface DiscountPolicy { int apply(int price); }
record Checkout(DiscountPolicy policy) {
    int total(int price) { return policy.apply(price); }
}
Checkout checkout = new Checkout(price -> price * 90 / 100);
System.out.println(checkout.total(500));
// Output: 450
```

Strategy replaces a growing algorithm-selection conditional.

## 4) Factory Method

```java
interface Notification { String send(String recipient); }
static Notification notificationFor(String channel) {
    return switch (channel) {
        case "email" -> recipient -> "email:" + recipient;
        case "sms" -> recipient -> "sms:" + recipient;
        default -> throw new IllegalArgumentException("unsupported channel");
    };
}
System.out.println(notificationFor("email").send("Asha"));
// Output: email:Asha
```

## 5) Builder with Validation

```java
record ConnectionSettings(String host, int port) {
    static final class Builder {
        private String host;
        private int port = 443;
        Builder host(String value) { host = value; return this; }
        Builder port(int value) { port = value; return this; }
        ConnectionSettings build() {
            if (host == null || host.isBlank() || port < 1 || port > 65_535) {
                throw new IllegalStateException("invalid settings");
            }
            return new ConnectionSettings(host, port);
        }
    }
}
System.out.println(new ConnectionSettings.Builder().host("example.com").build());
// Output: ConnectionSettings[host=example.com, port=443]
```

## 6) Correct equals/hashCode with a Value Object

```java
record Money(String currency, long minorUnits) {
    Money {
        Objects.requireNonNull(currency);
        if (minorUnits < 0) throw new IllegalArgumentException("negative money");
    }
}
Set<Money> values = new HashSet<>();
values.add(new Money("INR", 500));
System.out.println(values.contains(new Money("INR", 500)));
// Output: true
```

Records generate compatible value-based `equals` and `hashCode`.

## 7) Composition Instead of Inheritance

```java
interface Engine { String start(); }
record Car(Engine engine) {
    String start() { return "car:" + engine.start(); }
}
System.out.println(new Car(() -> "electric-start").start());
// Output: car:electric-start
```

Composition varies engine behavior without exposing a fragile base-class implementation.

## Most-Asked OOP Questions

1. Encapsulation? Protect invariants through safe operations, not merely private fields.
2. Abstraction? Expose necessary contract and hide irrelevant implementation.
3. Inheritance vs composition? Is-a substitutability vs has-a collaboration; prefer composition for behavior reuse.
4. Overloading vs overriding? Compile-time parameter selection vs runtime subtype dispatch.
5. Interface vs abstract class? Capability contract across types vs shared state/template for closely related types.
6. LSP? Every subtype must preserve the parent contract for valid callers.
7. Entity vs value object? Identity/lifecycle vs equality by immutable values.
8. SOLID purpose? Design signals for cohesion, substitutability, focused contracts, and dependency direction—not interface count.
9. Singleton downside? Hidden global dependency/state, test coupling, lifecycle/class-loader issues.
10. Factory vs Builder? Choose/create a product vs assemble one object with named options.
11. Adapter vs Decorator vs Proxy? Change interface vs add behavior vs control access.
12. Strategy vs State? Caller/config chooses algorithm vs object behavior changes with lifecycle state.
13. Observer risk? Ordering, failure isolation, unsubscribe leaks, delivery guarantees.
14. Why DI? Explicit required collaborators and replaceable boundaries.
15. Why avoid Cloneable? Awkward shallow-copy contract; explicit copy/immutable values are clearer.
