# 15 - GoF Behavioral Patterns

Behavioral patterns organize algorithms, responsibilities, and communication.

Simple question: “Who decides what happens next?” The answer may be a strategy, state object, command, event observer, chain, mediator, template, iterator, visitor, interpreter, or saved memento.

## 1) Chain of Responsibility

```java
UnaryOperator<String> authenticate = value -> value + "|authenticated";
UnaryOperator<String> authorize = value -> value + "|authorized";
System.out.println(authenticate.andThen(authorize).apply("request"));
// Output: request|authenticated|authorized
```

Each handler must define whether it stops or forwards the request.

## 2) Command

```java
interface Command { String execute(); }
Command createOrder = () -> "order-created";
System.out.println(createOrder.execute());
// Output: order-created
```

Commands can be queued, retried, audited, or undone when their contract supports it.

## 3) Interpreter

```java
interface Expression { int evaluate(); }
record NumberExpression(int value) implements Expression { public int evaluate() { return value; } }
record Add(Expression left, Expression right) implements Expression {
    public int evaluate() { return left.evaluate() + right.evaluate(); }
}
System.out.println(new Add(new NumberExpression(2), new NumberExpression(3)).evaluate());
// Output: 5
```

Use a parser library for non-trivial languages.

## 4) Iterator

```java
Iterator<String> iterator = List.of("A", "B").iterator();
while (iterator.hasNext()) System.out.println(iterator.next());
// Output:
// A
// B
```

Iterator traverses without exposing internal representation.

## 5) Mediator

```java
final class ChatRoom {
    String send(String from, String message) { return from + ":" + message; }
}
System.out.println(new ChatRoom().send("Asha", "hello"));
// Output: Asha:hello
```

Mediator centralizes interaction policy but can become a god object.

## 6) Memento

```java
record EditorState(String text) {}
EditorState saved = new EditorState("before");
EditorState current = new EditorState("after");
current = saved;
System.out.println(current.text());
// Output: before
```

Memento captures state without exposing mutable internals.

## 7) Observer

```java
List<Consumer<String>> observers = List.of(
        event -> System.out.println("audit:" + event),
        event -> System.out.println("metrics:" + event));
observers.forEach(observer -> observer.accept("ORDER_CREATED"));
// Output:
// audit:ORDER_CREATED
// metrics:ORDER_CREATED
```

Define ordering, failure isolation, unsubscribe, and delivery guarantees.

## 8) State

```java
sealed interface OrderState permits Created, Paid {}
record Created() implements OrderState {}
record Paid() implements OrderState {}
static OrderState pay(OrderState state) {
    if (!(state instanceof Created)) throw new IllegalStateException("cannot pay");
    return new Paid();
}
System.out.println(pay(new Created()).getClass().getSimpleName());
// Output: Paid
```

State moves behavior that varies by lifecycle state out of large conditionals.

## 9) Strategy

```java
IntUnaryOperator discount = price -> price * 90 / 100;
System.out.println(discount.applyAsInt(100));
// Output: 90
```

Strategy makes an algorithm replaceable.

## 10) Template Method

```java
abstract class ImportJob {
    final String run() { return read() + "|validated|saved"; }
    abstract String read();
}
ImportJob job = new ImportJob() { String read() { return "read"; } };
System.out.println(job.run());
// Output: read|validated|saved
```

Prefer composition when subclasses would need to override many hooks.

## 11) Visitor

```java
sealed interface Shape permits Circle, Rectangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double width, double height) implements Shape {}
static double area(Shape shape) {
    return switch (shape) {
        case Circle(var radius) -> Math.PI * radius * radius;
        case Rectangle(var width, var height) -> width * height;
    };
}
System.out.printf("%.2f%n", area(new Circle(2)));
// Output: 12.57
```

Classic Visitor is useful when adding operations is more frequent than adding element types. Sealed types and exhaustive switches provide a simpler modern alternative for closed hierarchies.
