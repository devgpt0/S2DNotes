# 14 - Active Object, Event Loop, and Reactive Streams Patterns

## 1) Active Object

An Active Object owns its thread, accepts method requests, and returns futures.

```java
final class ActiveCalculator implements AutoCloseable {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    CompletableFuture<Integer> add(int left, int right) {
        return CompletableFuture.supplyAsync(() -> left + right, executor);
    }

    public void close() {
        executor.close();
    }
}

try (ActiveCalculator calculator = new ActiveCalculator()) {
    System.out.println(calculator.add(20, 22).join());
}
// Output: 42
```

State is confined to the active object's executor. Bound its request queue in high-load systems.

## 2) Event Loop

An event loop serializes callbacks on one thread, avoiding locks for loop-owned state.

```java
try (ExecutorService eventLoop = Executors.newSingleThreadExecutor()) {
    List<String> state = new ArrayList<>();
    Future<?> first = eventLoop.submit(() -> state.add("connected"));
    Future<?> second = eventLoop.submit(() -> state.add("message"));
    first.get();
    second.get();
    System.out.println(state);
}
// Output: [connected, message]
```

Never block the event-loop thread with slow I/O or CPU work; offload it and post the result back.

## 3) Reactor and Proactor

- Reactor: an event demultiplexer announces readiness; handlers perform non-blocking operations.
- Proactor: asynchronous operations complete and invoke completion handlers.

Java NIO selectors support reactor-style designs. `AsynchronousChannel` APIs support completion-driven designs. Prefer frameworks that already implement their subtle lifecycle and error handling.

## 4) Reactive Streams and Backpressure

Java's `Flow` interfaces define publisher, subscriber, subscription, and processor roles.

```java
try (SubmissionPublisher<String> publisher = new SubmissionPublisher<>()) {
    CompletableFuture<String> received = new CompletableFuture<>();
    publisher.subscribe(new Flow.Subscriber<>() {
        private Flow.Subscription subscription;

        public void onSubscribe(Flow.Subscription value) {
            subscription = value;
            subscription.request(1);
        }

        public void onNext(String item) {
            received.complete(item);
            subscription.cancel();
        }

        public void onError(Throwable error) {
            received.completeExceptionally(error);
        }

        public void onComplete() {
            // Result: no action is required after the first requested item.
        }
    });
    publisher.submit("event");
    System.out.println(received.join());
}
// Output: event
```

Demand must be positive and bounded. Reactive programming helps when the entire pipeline honors backpressure; mixing blocking calls into it requires deliberate isolation.
