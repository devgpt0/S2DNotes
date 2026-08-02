# Design an Interactive Map Frontend

> **Difficulty:** Hard  
> **Main focus:** tiles, viewport queries, rendering

## Interview prompt

Design a browser map that displays millions of places, live vehicles, search, and route overlays.

## 1. Clarify the experience

**What I would say first:** The viewport is the query. I will fetch tiled or bounded data by zoom, cluster dense features, and separate map rendering from application selection state.

### Functional requirements

- Pan, zoom, search, select places, and show routes.
- Display many static features plus live moving objects.
- Work on mobile with poor networks and preserve map state in shareable URLs.
- Remain accessible beyond pointer-only interaction.

### Browser and product constraints

- Only a small geographic viewport is visible.
- The same data needs different detail at different zoom levels.
- Frequent live updates can overwhelm map rendering.

## 2. State and API contracts

- GET /tiles/{z}/{x}/{y}.mvt for immutable/versioned vector tiles
- GET /v1/places?bbox=...&zoom=...&filters=...
- WebSocket subscribe {cells, types} -> sequenced live position batches
- URL owns center, zoom, selected entity, and stable filters

## 3. Frontend architecture

```text
URL/router -> map controller -> viewport/camera state
                      |             |
                      |             +-> tile cache -> CDN vector/raster tiles
                      |
                 data layers -> worker decode/layout -> WebGL renderer
                      |
live subscription manager -> coalesced positions
selection panel/search are separate accessible DOM
```

## 4. Critical user flow

1. Read camera and filters from the URL and request visible tiles with a small margin.
2. Cancel obsolete viewport requests during rapid movement.
3. Decode vector tiles and layout labels in workers, then render GPU layers.
4. Subscribe live objects by coarse cells and coalesce updates to render frames.
5. Selecting a feature updates durable UI state and an accessible details panel.

## 5. Deep dive

- Cluster points at low zoom and reveal individuals only as visual space permits.
- Separate feature identity from tile instances because one feature can cross tile boundaries.
- Use hysteresis around viewport subscriptions to avoid churn at cell boundaries.
- Routes are simplified by zoom while retaining exact metadata for instructions.

## 6. Performance, resilience, and observability

- Bound tile cache by bytes and evict farthest or least-recently-used tiles.
- Limit labels, live objects, and update frequency at each zoom.
- Use workers for decoding and spatial calculations; keep interactions on the main thread.
- Track tile latency, cancelled bytes, dropped frames, live lag, cache hit ratio, and memory.

## 7. Security and accessibility

- Protect location permissions and avoid retaining precise user location unnecessarily.
- Sanitize labels and external links.
- Provide text search, result lists, keyboard zoom/pan, route instructions, and non-color map encodings.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| DOM markers | Simple and accessible for small counts, slow at scale. |
| WebGL layers | Scalable rendering with separate accessibility UI. |
| Fetch exact viewport | Less data but request churn. |
| Viewport margin/hysteresis | More cache data with smoother movement. |

## 9. 60-second interview summary

The URL and map controller own camera state, tiled viewport queries feed a byte-bounded cache, workers decode vector data, and WebGL renders dense layers. Live cell subscriptions are coalesced, while selection and navigation remain accessible DOM experiences.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

