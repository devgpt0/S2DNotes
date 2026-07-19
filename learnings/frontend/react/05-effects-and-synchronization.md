# 05 - React Effects and Synchronization

## What an Effect Is

An effect synchronizes a committed component with something outside React: subscription, timer, browser API, imperative widget, or network connection.

## What Does Not Need an Effect

Do not use effects to calculate filtered data, respond to a click, copy props into state, or chain state that can be derived during render.

```tsx
function Results({ courses, query }: { courses: readonly Course[]; query: string }) {
  const visible = courses.filter(course => course.title.includes(query));
  return <p>{visible.length} results</p>;
}
// Browser result: count is derived directly; no effect or duplicate state needed.
```

## Subscription with Cleanup

```tsx
function OnlineStatus() {
  const [online, setOnline] = useState(navigator.onLine);
  useEffect(() => {
    const update = () => setOnline(navigator.onLine);
    window.addEventListener("online", update);
    window.addEventListener("offline", update);
    return () => { window.removeEventListener("online", update); window.removeEventListener("offline", update); };
  }, []);
  return <p>{online ? "Online" : "Offline"}</p>;
}
// Browser result: status follows browser events; listeners are removed on unmount.
```

## Dependencies

Every reactive value read by an effect belongs in its dependency list unless the code is restructured so it is no longer reactive. Do not disable the hooks lint rule to force desired timing.

## Fetch with Cancellation

```tsx
useEffect(() => {
  const controller = new AbortController();
  void loadCourse(courseId, controller.signal).then(setCourse, error => {
    if (error.name !== "AbortError") setError("Could not load course");
  });
  return () => controller.abort();
}, [courseId]);
// Behavior: changing courseId/unmount aborts obsolete request and prevents stale lifecycle work.
```

Prefer router/framework data loading or a query library when caching, deduplication, retries, SSR, or mutation invalidation matters.

## Effect Timing

- `useEffect`: after paint for ordinary synchronization
- `useLayoutEffect`: before browser paint after DOM commit; only for measurement/synchronous visual correction
- insertion-style hooks: library-level CSS injection use cases

## StrictMode

Development StrictMode may setup/cleanup/setup effects to expose missing cleanup and impure logic. Fix the lifecycle instead of adding flags to suppress the signal.
