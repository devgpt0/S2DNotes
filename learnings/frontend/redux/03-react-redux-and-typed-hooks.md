# 03 - React Redux and Typed Hooks

## Provider

The Provider makes one store available to React components:

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { store } from "./store";
import App from "./App";

const root = document.querySelector("#root");
if (!(root instanceof HTMLDivElement)) throw new Error("root is missing");

createRoot(root).render(
  <StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </StrictMode>,
);
```

Do not create the store inside a component render. That would replace state and subscriptions.

## Typed Hooks

```typescript
import { useDispatch, useSelector, useStore } from "react-redux";
import type { AppDispatch, AppStore, RootState } from "./store";

export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
export const useAppStore = useStore.withTypes<AppStore>();
```

Add this store type:

```typescript
export type AppStore = typeof store;
```

Typed hooks remove repeated annotations and keep application components connected to the correct store types.

## Reading State

```tsx
const CourseCount = () => {
  const count = useAppSelector((state) => state.courses.items.length);
  return <p>{count} courses</p>;
};
```

Select the smallest value needed. Returning a fresh object on every selection can cause unnecessary renders.

## Dispatching Actions

```tsx
const PlanButton = ({ id }: { id: string }) => {
  const dispatch = useAppDispatch();
  const planned = useAppSelector((state) =>
    state.courses.items.find((course) => course.id === id)?.planned,
  );
  if (planned === undefined) return null;

  return (
    <button
      type="button"
      aria-pressed={planned}
      onClick={() => dispatch(courseToggled(id))}
    >
      {planned ? "Planned" : "Plan"}
    </button>
  );
};
```

The event decides what happened and dispatches it. The reducer owns the transition.

## Pass IDs, Not Store Objects

```tsx
const CourseRow = ({ id }: { id: string }) => {
  const course = useAppSelector((state) =>
    state.courses.items.find((item) => item.id === id),
  );
  if (course === undefined) return null;
  return <li>{course.title}</li>;
};
```

Passing only an ID can keep children subscribed to the state they need. For small lists, passing a complete selected value may be simpler; measure before optimizing.

## Local State Still Belongs Locally

```tsx
const CourseSearch = () => {
  const [draft, setDraft] = useState("");
  const courses = useAppSelector(selectCourses);
  const visible = courses.filter((course) =>
    course.title.toLocaleLowerCase().includes(draft.toLocaleLowerCase()),
  );
  return <section aria-labelledby="search-heading">
    <h2 id="search-heading">Find courses</h2>
    <label htmlFor="course-search">Search</label>
    <input id="course-search" value={draft} onChange={(event) => setDraft(event.currentTarget.value)} />
    <ul>{visible.map((course) => <li key={course.id}>{course.title}</li>)}</ul>
  </section>;
};
```

An input draft used by one component does not need Redux. If the search must be shareable/bookmarkable, the URL may be the correct owner.

## Component Boundary

Use connected feature components near the store and plain presentational components for reusable UI:

```tsx
type CourseListProps = Readonly<{
  courses: readonly Course[];
  onToggle: (id: string) => void;
}>;

const CourseList = ({ courses, onToggle }: CourseListProps) => {
  return <ul>{courses.map((course) => (
    <li key={course.id}>
      {course.title}
      <button type="button" onClick={() => onToggle(course.id)}>Toggle</button>
    </li>
  ))}</ul>;
};
```

Do not wrap every component in a store-aware layer. Keep domain coordination cohesive and visual primitives reusable.

## Store Setup for SSR or Tests

A factory creates one store per request/test:

```typescript
export const createAppStore = (preloadedState?: RootState) => {
  return configureStore({
    reducer: { courses: coursesReducer },
    preloadedState,
  });
};
```

For server rendering, never share one mutable global store across users.

## Final Rules

- Provider receives a stable store
- use typed hooks
- selectors read minimal state
- local drafts stay local
- URL owns shareable navigation state
- plain UI components do not need store knowledge
- server/test environments use a store factory when isolation matters
