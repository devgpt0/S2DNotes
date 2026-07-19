# 09 - Async UI, Suspense, Transitions, Actions, and Optimistic State

## Suspense Mental Model

Suspense shows a fallback while a compatible descendant's required resource/code is not ready.

```tsx
const CoursePage = lazy(() => import("./CoursePage"));
function App() {
  return <Suspense fallback={<p>Loading course…</p>}><CoursePage /></Suspense>;
}
// Browser result: fallback during code download, then CoursePage.
```

Suspense does not automatically make arbitrary effect-based fetching Suspense-aware. Use a framework/router/data source designed for it.

## Transition

Mark a non-urgent update so urgent input remains responsive.

```tsx
function Search({ courses }: { courses: readonly Course[] }) {
  const [input, setInput] = useState("");
  const [query, setQuery] = useState("");
  const [pending, startTransition] = useTransition();
  return <><input value={input} onChange={event => { const value = event.currentTarget.value; setInput(value); startTransition(() => setQuery(value)); }} />
    {pending && <span>Updating…</span>}<CourseResults courses={courses} query={query} /></>;
}
// Browser result: input updates urgently while expensive result update can be deferred.
```

Transitions do not make slow JavaScript fast; optimize expensive computation too.

## Deferred Value

`useDeferredValue` lets a part of UI lag behind an urgent value. It is not a fixed debounce timer and does not reduce network calls by itself.

## Action State

```tsx
async function saveCourse(_previous: string, formData: FormData): Promise<string> {
  const title = formData.get("title");
  if (typeof title !== "string" || title.length === 0) return "Title is required";
  await api.save({ title });
  return "Saved";
}
function CourseForm() {
  const [message, action, pending] = useActionState(saveCourse, "");
  return <form action={action}><input name="title" required /><button disabled={pending}>Save</button><p aria-live="polite">{message}</p></form>;
}
// Browser result: form action manages pending state and displays validation/success message.
```

## Optimistic UI

```tsx
const [optimisticTasks, addOptimisticTask] = useOptimistic(tasks, (current, task: Task) => [...current, task]);
// Behavior: UI can show submitted task immediately while the real operation completes; failure must reconcile/announce.
```

Use optimistic updates only when rollback/reconciliation is understandable and duplicate commands are controlled.

## `use`

React's `use` can read supported Promise/context resources during render and integrate with Suspense/error boundaries. Prefer framework-level patterns because creating uncached Promises during render causes repeated work.

## Async Design Checklist

Loading, empty, error, success, stale, retry, cancel, offline, authorization, mutation conflict, optimistic rollback, and accessibility announcement all need defined behavior.
