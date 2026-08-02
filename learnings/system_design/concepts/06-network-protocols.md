# Network Protocols

## Idea

Protocol choice controls connection cost, delivery direction, compatibility,
and failure behavior.

## Visual model

```text
HTTP request/response: client asks -> server answers
SSE:                   client connects <- server streams
WebSocket:             client <-------> server
queue/event:           producer -> broker -> consumer later
```

## Design steps

1. Decide direction: request/response, server push, or bidirectional.
2. Decide duration: short request or long-lived connection.
3. Define ordering, retries, heartbeats, timeouts, and message limits.
4. Secure with TLS, authentication, authorization, and validation.

## When to use it

- HTTP: ordinary APIs and cacheable content.
- SSE: one-way browser updates with simple reconnection.
- WebSocket: low-latency bidirectional sessions.
- gRPC: typed internal RPC and streaming.
- asynchronous broker: durable decoupling.

## Trade-offs

Long-lived connections reduce update latency but require connection routing,
heartbeats, backpressure, and deployment draining.

## Common mistakes

- Claiming TCP removes application duplicates.
- No timeout or maximum payload.
- Using WebSockets for rarely changing data.
- Ignoring mobile reconnects and proxy idle timeouts.
