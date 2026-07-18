# 18 - WebFlux and Reactive Programming

WebFlux uses non-blocking request processing and Reactive Streams. Use it when the whole I/O path is non-blocking and high concurrency justifies the complexity. MVC with virtual threads is often simpler for blocking dependencies.

## Beginner Meaning

Normal blocking code waits for a result on the current thread. Reactive code describes a future flow of zero, one, or many values and lets the runtime notify the pipeline when data arrives. `Mono<T>` means zero or one value; `Flux<T>` means zero to many values.

Learn ordinary MVC first. Reactive code is not automatically faster.

## `Mono` and `Flux`

```java
Mono<String> greeting = Mono.just("Java").map(value -> "Hello " + value);
System.out.println(greeting.block());
// Output: Hello Java
// block is used only to demonstrate the result; do not block an event-loop request thread.
```

```java
List<Integer> values = Flux.just(1, 2, 3)
        .map(value -> value * value)
        .collectList()
        .block();
System.out.println(values);
// Output: [1, 4, 9]
```

Nothing executes until subscription. Errors are terminal signals, not ordinary values.

## Reactive Controller

```java
@RestController
final class ProductReactiveController {
    @GetMapping("/api/products/{id}")
    Mono<ProductResponse> find(@PathVariable long id) {
        return service.find(id);
        // HTTP 200 emits one product; empty/error mapping must be defined explicitly.
    }
}
```

## WebClient

```java
Mono<InventoryResponse> response = webClient.get()
        .uri("/api/inventory/{id}", 10)
        .retrieve()
        .bodyToMono(InventoryResponse.class)
        .timeout(Duration.ofSeconds(2));
System.out.println(response != null);
// Output: true
// Actual response is asynchronous and depends on the remote service.
```

## Threading Rules

- event-loop threads must not perform blocking JDBC, filesystem, or legacy HTTP calls
- use R2DBC/non-blocking clients for an end-to-end reactive path
- isolate unavoidable blocking work on a bounded scheduler
- preserve Reactor context for tracing/security rather than relying on `ThreadLocal`
- apply backpressure and response-size limits

## Operator Interview Points

- `map`: synchronous one-to-one transform
- `flatMap`: asynchronous zero/one-to-many composition; may reorder
- `concatMap`: preserves order by serial composition
- `zip`: combines independent publishers
- `onErrorResume`: switches to a valid fallback publisher
- `timeout`: terminates when the deadline expires
- `retryWhen`: retries only with explicit safe policy

Do not call `subscribe()` inside service code to make work happen; return the publisher so the framework owns lifecycle, cancellation, and error propagation.
