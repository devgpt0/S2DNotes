# Redux Toolkit and React Redux - Beginner to Expert Roadmap

Redux is useful when shared client state has complex transitions, many readers/writers, debugging requirements, or cross-feature workflows. It is not required for every React application.

These notes teach modern Redux Toolkit. Avoid legacy tutorials built around hand-written action constants, large switch reducers, or manual immutable spread chains unless you are maintaining old code.

## Learning Order

1. [Why state management exists and when Redux fits](01-state-management-mental-model.md)
2. [Store, slice, action, and reducer with Redux Toolkit](02-store-slices-actions-and-reducers.md)
3. [React Redux Provider and typed hooks](03-react-redux-and-typed-hooks.md)
4. [Async thunks and listener middleware](04-async-thunks-and-listeners.md)
5. [RTK Query for server state](05-rtk-query-server-state.md)
6. [Selectors, normalization, and performance](06-selectors-normalization-and-performance.md)
7. [Testing, DevTools, persistence, and production design](07-testing-devtools-and-persistence.md)
8. [Redux expert tips](98-redux-expert-tips.md)
9. [Complete Redux Toolkit course project](99-redux-course-project.md)

## Code Convention

Standalone functions use typed arrow variables. Reducer callbacks inside `createSlice` use method syntax because they are named fields in the slice configuration object.

## Beginner to Expert Path

- beginner: one-way data flow, store, dispatch, reducer, selector
- developer: slices, typed hooks, async lifecycle, normalized state
- senior: ownership boundaries, server vs client state, middleware, testing
- expert: selector invalidation, listener workflows, cache lifecycle, persistence migration, observability

## First Decision

Before adding Redux, ask:

1. Can local component state own this value?
2. Is it server data better owned by a query/cache tool?
3. Does the URL already own this shareable state?
4. Is Context with a small reducer sufficient?
5. Does Redux solve demonstrated coordination or debugging complexity?

Use the smallest state tool that keeps ownership clear.
