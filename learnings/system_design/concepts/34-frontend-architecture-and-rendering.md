# Frontend Architecture and Rendering

## Idea

Frontend architecture decides where UI work and data loading happen, how code
is split, and how browser/server output becomes interactive. Rendering strategy
should follow SEO, personalization, latency, cacheability, and interaction needs.

## Visual model

```text
request -> CDN/server renders HTML -> browser paints
        -> selective JS download -> hydrate/attach interactions
        -> client navigation + server/API data
```

## Design steps

1. Map routes by SEO, freshness, personalization, and interaction requirements.
2. Choose CSR, SSR, static generation, incremental regeneration, or a hybrid per route.
3. Define server/client component boundaries and serialization rules.
4. Split bundles by route/feature and stream independent page regions.
5. Add loading, empty, error, retry, and partial-data states.
6. Measure real-user performance before changing rendering mode.

## Rendering choices

- CSR: highly interactive authenticated apps; slower first meaningful render.
- SSR: personalized/fresh HTML; server cost and cache complexity.
- Static: fastest/cacheable content; rebuild or revalidation for freshness.
- Streaming/server components: less client JavaScript; tighter framework/server contract.

## Trade-offs

Server rendering improves initial content but can move bottlenecks to server
latency and hydration. More client JavaScript improves local interaction but
increases parse, memory, and main-thread work.

## Common mistakes

- Choosing one rendering mode for every route.
- Hydrating the whole page when only small islands are interactive.
- Fetching the same data independently at several component levels.
- Ignoring behavior when JavaScript, one API, or hydration fails.
