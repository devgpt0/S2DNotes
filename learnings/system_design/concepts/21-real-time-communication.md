# Real-Time Communication

## Idea

Real-time systems push fresh events to connected clients while handling
disconnects, ordering, slow consumers, and reconnect catch-up.

## Classroom board

```text
client -> connection gateway -> session registry
event -> broker -> gateway owning that connection -> client
reconnect(last_seen_sequence) -> fetch missed events
```

## Design steps

1. Choose polling, SSE, or WebSocket from direction and latency needs.
2. Authenticate the connection and authorize every channel.
3. Assign per-stream sequence IDs and persist important events.
4. Use heartbeats, bounded buffers, backpressure, and reconnect cursors.

## When to use it

Use for chat, collaboration, presence, live dashboards, and notifications.
Presence may be approximate; messages normally need durable catch-up.

## Trade-offs and mistakes

Long connections add routing and deployment-drain complexity. Do not promise
global order, keep infinite per-client buffers, or trust subscription names
without authorization.
