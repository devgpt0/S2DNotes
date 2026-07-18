# 15 - HTTP Client, Networking, and I/O Boundaries

## Java HTTP Client

```java
HttpClient client = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(2))
        .build();
HttpRequest request = HttpRequest.newBuilder(URI.create("https://example.com"))
        .timeout(Duration.ofSeconds(3))
        .GET()
        .build();
System.out.println(request.method());
System.out.println(request.timeout().orElseThrow());
// Output:
// GET
// PT3S
```

## Asynchronous Request

```java
CompletableFuture<HttpResponse<String>> response = client.sendAsync(
        request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.getClass().getSimpleName().contains("Future"));
// Output: true
// Actual network response depends on the remote service.
```

## Network Interview Fundamentals

- DNS maps names to addresses and can return multiple results.
- TCP provides an ordered byte stream, not message boundaries.
- TLS authenticates peers and protects transport confidentiality/integrity.
- HTTP keep-alive reuses connections.
- HTTP/2 multiplexes streams over a connection.
- idempotency determines whether retries can be safe.

## Boundary Security

- allow-list outbound schemes and hosts to prevent SSRF
- validate redirects and resolved destinations
- configure connect, request, and total operation deadlines
- limit response size and decompression
- validate content type and schema
- never log credentials or authorization headers
- retry only safe transient failures with backoff and jitter
