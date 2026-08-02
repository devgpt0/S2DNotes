# Frontend Architecture and Rendering

## Idea

Frontend architecture assigns ownership of routes, UI state, data fetching,
and rendering between browser, edge, and server.

## Classroom board

```text
request -> CDN/server HTML -> browser parse/render -> hydrate interactive parts
future navigation -> route data -> render only changed UI
```

## Design steps

1. Split by user journeys/routes and stable feature ownership.
2. Choose CSR, SSR, SSG, streaming, or hybrid per route.
3. Keep server/client boundaries explicit and minimize shipped JavaScript.
4. Define error/loading states, accessibility, analytics, and deployment safety.

## When to use it

SSR/streaming helps first view and SEO; CSR fits highly interactive private
apps; static generation fits content that changes less often.

## Trade-offs and mistakes

SSR shifts work to servers and hydration. Avoid one global store, client-only
auth checks, browser API use during server render, and architecture by component
type instead of product feature.
