# 11 - Routing, Data Architecture, and Server Components

## Routing

A production router maps URLs to UI, nested layouts, parameters, loaders/actions, navigation, errors, and code-split boundaries.

Keep shareable/filter/navigation state in the URL when users should bookmark, refresh, or send it.

```tsx
const url = new URL(window.location.href);
const query = url.searchParams.get("query") ?? "";
console.log(query);
// Console output: current query parameter or empty string.
```

Prefer a maintained router/framework over handwritten History listeners for nontrivial apps.

## Client State vs Server State

- client state: selected tab, draft, local modal
- server state: remote data with cache/freshness/retry/invalidation rules
- URL state: shareable navigation/filter state
- form state: draft and validation lifecycle

Do not copy server query data into global client state without a reason.

## Data Fetching Architecture

A router/framework/query library can own request deduplication, cache, stale time, retries, cancellation, mutation invalidation, SSR, and Suspense integration. An effect with fetch is suitable for small synchronization cases but grows complex quickly.

## Server Components

Server Components render on the server and can access server-side data/code without shipping that component implementation to the client. Client Components provide browser interactivity/state/effects.

Server Components require a supporting framework/build architecture; React library alone does not provide a complete production server setup.

```tsx
// Conceptual server component in a supporting framework
export default async function CoursePage({ id }: { id: string }) {
  const course = await database.course.find(id);
  return <article><h1>{course.title}</h1><EnrollButton courseId={course.id} /></article>;
}
// Result: course content renders from server data; interactive EnrollButton is a client boundary.
```

## Architecture by Feature

```text
features/course/
├─ api/          # boundary clients and validators
├─ components/   # feature UI
├─ hooks/        # feature stateful logic
├─ model/        # domain types and pure logic
├─ routes/       # route composition/loaders/actions
└─ tests/
# Result: cohesive feature ownership and smaller public APIs.
```

## Dependency Direction

Pure domain/model should not import React DOM, router, or HTTP clients. UI depends on model and adapters, which makes logic reusable/testable.
