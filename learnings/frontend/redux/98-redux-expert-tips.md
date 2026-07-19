# 98 - Redux Toolkit Expert Tips

## State Ownership

- local UI draft stays local
- shareable navigation state stays in URL
- server resources stay in RTK Query cache
- Redux slices own coordinated client workflows
- durable offline data uses a browser database and sync design

## Slice Design

- organize by feature/domain, not action type
- keep one canonical entity per ID
- store IDs for relationships and selection
- model lifecycle states explicitly
- reject invalid transitions
- never put effects in reducers

## Action Design

Prefer domain events:

```typescript
dispatch(courseEnrollmentRequested({ courseId, learnerId }));
```

Avoid generic setters that expose internal state shape everywhere:

```typescript
// Avoid: dispatch(setCourses(nextCourses));
```

Events make DevTools and workflows understandable.

## Typed Matchers

```typescript
const isRejectedAction = isRejectedWithValue(saveCourse, deleteCourse);

listenerMiddleware.startListening({
  matcher: isRejectedAction,
  effect: (action) => {
    console.log("Expected request failure", action.type);
  },
});
```

Log only safe categories and IDs allowed by policy, not full payloads or tokens.

## Listener Concurrency

Use listener cancellation primitives for take-latest, debounce, pause, and child tasks instead of building uncontrolled timers.

```typescript
listenerMiddleware.startListening({
  actionCreator: searchChanged,
  effect: async (action, api) => {
    api.cancelActiveListeners();
    await api.delay(300);
    api.dispatch(searchRequested(action.payload));
  },
});
```

The latest search cancels previous listener instances before the delayed dispatch.

## Selector API

Expose domain selectors from the slice module:

```typescript
export const selectVisibleCourses = createSelector(
  [selectAllCourses, selectCourseFilter],
  (courses, filter) => courses.filter((course) => matchesFilter(course, filter)),
);
```

Do not make components understand normalized internal structure.

## RTK Query Cache Updates

- prefer tags for ordinary invalidation
- use manual cache updates only for a real UX requirement
- always handle rollback or refetch on failure
- keep cache key arguments stable and serializable
- use `selectFromResult` for narrowly subscribed derived query results

## Dynamic Reducers

Code-split reducer injection is justified in very large route/plugin systems. It adds store lifecycle and type complexity. Prefer a static reducer map until bundle evidence requires dynamic injection.

## Middleware Order

Middleware wraps dispatch in order. Preserve Toolkit defaults unless a measured or integration requirement changes them. Serializability/immutability checks are valuable development diagnostics.

## Performance

- profile components before memoizing selectors
- select primitives or stable references
- normalize large frequently updated entity sets
- avoid dispatching on every animation frame or pointer move
- batch at the event/workflow boundary when product semantics allow it
- do not persist or log the entire store after every action

## Security

- Redux is visible to browser code and developer tools
- never store secrets as a security measure
- client state cannot authorize server operations
- sanitize shared bug reports and DevTools exports
- validate external action payloads from sockets, storage, or cross-window messages before dispatch

## Store Factory

```typescript
export const setupStore = (preloadedState?: RootState) => configureStore({
  reducer: rootReducer,
  preloadedState,
  middleware: (getDefaultMiddleware) => getDefaultMiddleware()
    .prepend(listenerMiddleware.middleware)
    .concat(coursesApi.middleware),
});

export type AppStore = ReturnType<typeof setupStore>;
export type AppDispatch = AppStore["dispatch"];
```

One factory supports isolated tests, SSR requests, stories, and the browser entry point.

## Expert Review Checklist

- why does this value need Redux?
- who owns the canonical state?
- is it client workflow or server cache?
- are actions domain events?
- can impossible lifecycle states be represented?
- are selectors hiding storage shape?
- what cancels each async process?
- what is persisted, for how long, and with which version?
- what data appears in DevTools?
- what measurement justifies optimization?

## Final Rule

Expert Redux code is often less Redux: fewer global values, fewer duplicate caches, narrower actions, clearer ownership, and explicit async lifecycles.
