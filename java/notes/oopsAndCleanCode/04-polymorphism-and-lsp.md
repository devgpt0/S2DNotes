# 04 - Polymorphism and Liskov Substitution

## 1) Polymorphism Replaces Conditionals

```java
interface Notification {
    String send(String recipient);
}

record EmailNotification() implements Notification {
    @Override
    public String send(String recipient) {
        return "email:" + recipient;
    }
}

record SmsNotification() implements Notification {
    @Override
    public String send(String recipient) {
        return "sms:" + recipient;
    }
}

List<Notification> channels = List.of(new EmailNotification(), new SmsNotification());
channels.stream().map(channel -> channel.send("Asha")).forEach(System.out::println);
// Output:
// email:Asha
// sms:Asha
```

## 2) Liskov Substitution Principle

Any implementation must be usable wherever its abstraction is expected without surprising the caller.

A subtype must not:

- require stricter inputs than the abstraction
- return weaker guarantees
- throw new unexpected failures for valid operations
- break documented state or performance assumptions

```java
interface Stack<T> {
    void push(T value);
    T pop();
}

final class ArrayStack<T> implements Stack<T> {
    private final Deque<T> values = new ArrayDeque<>();

    public void push(T value) {
        values.push(Objects.requireNonNull(value));
    }

    public T pop() {
        if (values.isEmpty()) {
            throw new NoSuchElementException("stack is empty");
        }
        return values.pop();
    }
}

Stack<String> stack = new ArrayStack<>();
stack.push("Java");
System.out.println(stack.pop());
// Output: Java
```

## 3) Avoid Fake Polymorphism

If an implementation must throw `UnsupportedOperationException` for a core interface method, the abstraction may be too broad. Split capabilities into smaller interfaces.
