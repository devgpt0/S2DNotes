# Design a Real-Time Analytics Dashboard Frontend

> **Difficulty:** Medium  
> **Main focus:** streaming data, chart performance, freshness

## Interview prompt

Design a dashboard with many charts that update continuously from live data.

## 1. Clarify the experience

**What I would say first:** The browser should receive aggregated bounded updates, not every raw event. I will separate the server-state stream from chart rendering and apply backpressure.

### Functional requirements

- Load historical data, then apply live updates.
- Render charts, tables, filters, and drill-down.
- Show freshness, connection state, and partial failures.
- Remain usable with many widgets and high update rates.

### Browser and product constraints

- The main thread must remain responsive.
- Widgets may use different time ranges and permissions.
- A slow browser cannot buffer an unlimited stream.

## 2. State and API contracts

- GET /v1/dashboards/{id}/snapshot?range=1h
- WebSocket/SSE subscribe {seriesIds, resolution} -> point batches and sequence
- GET /v1/series/{id}?start=...&end=...&resolution=...

## 3. Frontend architecture

```text
dashboard route -> layout/config store
       |
query cache -> snapshot APIs
       |
stream manager -> sequence/gap detector -> bounded series buffers
       |                                      |
       +-> shared subscriptions               +-> chart adapters
                                                     |
                                               canvas/worker rendering
```

## 4. Critical user flow

1. Fetch dashboard configuration and historical snapshots in parallel with authorization.
2. Open one shared stream and subscribe only visible widgets.
3. Apply ordered batches to bounded ring buffers and record last sequence.
4. Coalesce visual updates to animation frames or a lower chart refresh rate.
5. On a sequence gap, pause that series and fetch a new snapshot.

## 5. Deep dive

- Choose aggregation resolution from pixel width; drawing ten points per pixel adds no value.
- Use Canvas or WebGL for dense series and DOM/SVG for accessible summaries.
- Move expensive transforms to workers when copying cost is justified.
- Virtualize offscreen widgets and suspend their live subscriptions.

## 6. Performance, resilience, and observability

- Apply explicit limits for points, widgets, subscriptions, and update frequency.
- Drop intermediate visual frames but never silently corrupt aggregate state.
- Show widget-level errors rather than failing the whole dashboard.
- Track input latency, dropped frames, stream lag, sequence gaps, memory, and stale widgets.

## 7. Security and accessibility

- Authorize every series server-side and avoid embedding secrets in dashboard config.
- Sanitize labels and exported values.
- Provide tabular alternatives, keyboard filters, non-color encodings, and pause controls for motion.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Raw event stream | Maximum detail but overwhelms network and browser. |
| Aggregated series | Efficient and readable with less drill-down detail. |
| SVG charts | Accessible structure but costly for many points. |
| Canvas/WebGL | Fast dense rendering with extra accessibility work. |

## 9. 60-second interview summary

The client loads a snapshot, then one shared sequenced stream updates bounded series buffers. It subscribes only visible widgets, coalesces chart rendering, detects gaps, and exposes freshness and partial failure without sacrificing main-thread responsiveness.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

