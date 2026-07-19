# React Expert Tips and Production Code Snippets

## Expert Principles

- Derive UI; do not synchronize duplicate state.
- State ownership and identity/key design solve more bugs than memoization.
- Effects are escape hatches for external systems.
- Treat server data, URL state, form state, and local UI state as different lifecycles.
- Keep render pure so concurrent/restarted rendering remains safe.
- Use semantic HTML and headless primitives before custom interaction mechanics.
- Profile production builds on realistic devices.

## Expert Code Snippet: Required Context Factory

```tsx
function createRequiredContext<T>(name: string) {
  const Context = createContext<T | null>(null);
  function useRequired(): T {
    const value = useContext(Context);
    if (value === null) throw new Error(`${name} provider is missing`);
    return value;
  }
  return [Context.Provider, useRequired] as const;
}
const [SessionProvider, useSession] = createRequiredContext<Session>("Session");
// Result: consumers receive Session directly and fail clearly outside provider.
```

## Expert Code Snippet: Stable Event Callback

```tsx
function useEvent<Arguments extends unknown[], Result>(
  handler: (...arguments_: Arguments) => Result,
): (...arguments_: Arguments) => Result {
  const ref = useRef(handler);
  useLayoutEffect(() => { ref.current = handler; });
  return useCallback((...arguments_: Arguments) => ref.current(...arguments_), []);
}
// Result: stable callback identity invokes latest handler; prefer official React APIs when available for the use case.
```

Use this carefully for subscription callbacks, not to bypass legitimate effect dependencies.

## Expert Code Snippet: Abortable Resource Hook

```tsx
function useCourse(id: string) {
  const [state, setState] = useState<State>({ status: "loading" });
  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading" });
    void fetchCourse(id, controller.signal).then(
      course => setState({ status: "success", course }),
      error => { if (error.name !== "AbortError") setState({ status: "error", message: "Could not load" }); },
    );
    return () => controller.abort();
  }, [id]);
  return state;
}
// Behavior: id changes cancel obsolete request and expose explicit loading/success/error states.
```

For production caching/deduplication/SSR, use a router/query framework rather than growing this hook indefinitely.

## Expert Code Snippet: Reducer with Exhaustiveness

```tsx
type Action = { type: "added"; item: Item } | { type: "removed"; id: string };
function reducer(state: readonly Item[], action: Action): readonly Item[] {
  switch (action.type) {
    case "added": return [...state, action.item];
    case "removed": return state.filter(item => item.id !== action.id);
    default: return action satisfies never;
  }
}
// Result: adding a new action fails type checking until reducer handles it.
```

## Expert Code Snippet: Accessible Pending Button

```tsx
function SubmitButton() {
  const { pending } = useFormStatus();
  return <button type="submit" disabled={pending} aria-disabled={pending}>{pending ? "Saving…" : "Save"}</button>;
}
// Browser result: form action pending state prevents duplicate activation and communicates progress.
```

## Production Review Checklist

- stable IDs/keys and intentional reset boundaries
- no derived-state effects
- every effect has complete cleanup/dependencies
- runtime API validation and safe error categories
- pending/error/empty/offline/cancel/conflict states
- route/feature error and Suspense boundaries
- keyboard/focus/labels/live announcements
- no unsafe HTML/client-only authorization
- tests use roles/user events
- profiler confirms optimization value
- bundle routes/chunks and Core Web Vitals measured

## State and Identity Tips

- Keep one source of truth; calculate filtered lists, totals, and flags during rendering.
- Use a reducer when transitions are related and need exhaustive review—not merely because state has several fields.
- Store IDs rather than duplicate selected objects when the canonical collection already exists.
- Treat key changes as explicit reset boundaries; never generate a random key during rendering.
- Keep input draft state local until another region genuinely needs it.
- Put shareable filters/page/search in the URL.
- Separate local UI, form, server-cache, and durable client-storage state because their lifecycles differ.

## Effect and Async Tips

- Effects synchronize external systems. Events/actions own user-triggered mutations.
- Never suppress exhaustive-deps to force timing; change ownership or extract stable logic.
- Cleanup must completely undo setup and tolerate development StrictMode setup-cleanup-setup.
- Abort obsolete work and prevent stale results from committing.
- Start independent requests together and avoid component-level waterfalls.
- Prefer router/framework/query data APIs for caching, SSR, deduplication, mutation invalidation, and retry policy.
- Place Suspense/Error boundaries around meaningful independently recoverable regions.
- Use transitions for non-urgent renders, not to hide slow algorithms or network latency.
- Optimistic UI needs server identity, rollback/reconciliation, conflict, and accessibility feedback.

## Component API Tips

- Prefer children/slots/composition over many boolean mode props.
- Provide controlled and uncontrolled modes only with a documented stable contract.
- Preserve semantic HTML, native props, accessible names, and refs in primitives.
- Avoid a wrapper that merely renames another component without adding policy.
- Model variants as finite unions and impossible states as discriminated unions.
- Keep domain components in features and reusable visual primitives in a small shared layer.
- Do not expose third-party query/form/router types through the entire domain unless intentional.

## Rendering and Performance Tips

- A render is calculation; a commit changes host UI. Do not optimize render count without measured cost.
- Profile production-like builds on representative mobile CPU.
- Fix state placement, context scope, list size, and request waterfalls before memoization.
- `useMemo`, `useCallback`, and `memo` are performance tools, not correctness guarantees.
- Keep context values narrow; split unrelated frequently changing values.
- Virtualize only large measured lists and test focus/screen-reader behavior.
- Lazy-load meaningful route/features and prefetch likely navigation from product evidence.
- When React Compiler is enabled, follow its rules/lints and remove redundant manual memoization only after verification.

## Accessibility and Security Tips

- Test keyboard, screen reader, zoom, reduced motion, forced colors, and touch—not just axe output.
- Use tested headless primitives for dialog/menu/combobox/listbox; these are interaction patterns, not styling tasks.
- Keep untrusted data in escaped JSX; sanitize deliberately allowed rich HTML.
- Validate navigation/resource URLs and never trust a client route guard as authorization.
- Frontend environment variables are public; keep secrets/server credentials outside the client graph.
- Preserve focus and announce pending/error/success for async operations.

## Testing and Debugging Tips

- Test roles, labels, user events, URL, network outcomes, and visible behavior.
- Mock request boundaries, not internal hooks.
- Include loading, error, empty, offline, conflict, cancellation, and retry states.
- Use React DevTools “why rendered,” browser Performance, Network initiators, and async stacks together.
- Common root causes: wrong key, mutated state, stale closure, missing cleanup, duplicate derived state, or invalid server data.

## High-Use Responsive Composition Pattern

```tsx
type PanelProps = Readonly<{
  id: string;
  title: string;
  action?: ReactNode;
  children: ReactNode;
}>;

function Panel({ id, title, action, children }: PanelProps) {
  return <section className="panel" aria-labelledby={id}>
    <header className="panel__header"><h2 id={id}>{title}</h2>{action}</header>
    <div className="panel__body">{children}</div>
  </section>;
}
```

```css
.panel__header { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1rem; }
.panel__body { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr)); gap: 1rem; }
```

Composition keeps the API extendable; CSS handles responsive placement without render-time viewport checks. Callers pass a stable, document-unique heading ID.
