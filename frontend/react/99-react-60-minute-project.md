# React 60-Minute Project - Course Planner

## Goal

Build a searchable course planner practicing typed components, props, state snapshots, immutable updates, controlled form, derived lists, stable keys, reducer, custom hook, persistence effect, accessibility, and tests.

## Time Box

- 0-8 min: Vite React TS and types
- 8-18 min: reducer and sample data
- 18-32 min: list/search/selection
- 32-43 min: add-course form
- 43-50 min: persistence custom hook
- 50-56 min: accessibility/states
- 56-60 min: tests/profile

## Step 1: Model and Reducer

```tsx
type Course = Readonly<{ id: string; title: string; planned: boolean }>;
type Action = { type: "added"; course: Course } | { type: "toggled"; id: string } | { type: "removed"; id: string };
function reducer(state: readonly Course[], action: Action): readonly Course[] {
  switch (action.type) {
    case "added": return [...state, action.course];
    case "toggled": return state.map(course => course.id === action.id ? { ...course, planned: !course.planned } : course);
    case "removed": return state.filter(course => course.id !== action.id);
    default: return action satisfies never;
  }
}
// Result: pure immutable transitions with exhaustive action handling.
```

## Step 2: Planner

```tsx
function Planner() {
  const [courses, dispatch] = useReducer(reducer, initialCourses);
  const [query, setQuery] = useState("");
  const visible = courses.filter(course => course.title.toLowerCase().includes(query.toLowerCase()));
  return <main><h1>Course Planner</h1>
    <label>Search <input value={query} onChange={event => setQuery(event.currentTarget.value)} /></label>
    <p aria-live="polite">{visible.length} courses</p>
    <CourseList courses={visible} dispatch={dispatch} />
  </main>;
}
// Browser result: controlled search filters a derived list and announces count.
```

## Step 3: Stable List

```tsx
function CourseList({ courses, dispatch }: { courses: readonly Course[]; dispatch: Dispatch<Action> }) {
  if (courses.length === 0) return <p>No courses match.</p>;
  return <ul>{courses.map(course => <li key={course.id}><span>{course.title}</span>
    <button aria-pressed={course.planned} onClick={() => dispatch({ type: "toggled", id: course.id })}>{course.planned ? "Planned" : "Plan"}</button>
    <button onClick={() => dispatch({ type: "removed", id: course.id })}>Delete <span className="visually-hidden">{course.title}</span></button>
  </li>)}</ul>;
}
// Browser result: stable keyed rows with accessible toggle/delete names.
```

## Step 4: Add Form

Use a React 19 form action or controlled submission. Validate non-empty title, create ID outside rendering during action, dispatch `added`, reset, and return focus/status.

```tsx
function add(formData: FormData) {
  const title = formData.get("title");
  if (typeof title !== "string" || title.length === 0) throw new TypeError("title required");
  dispatch({ type: "added", course: { id: crypto.randomUUID(), title, planned: false } });
  console.log(title);
}
// Console output on valid submit: submitted title; list receives new course.
```

## Step 5: Persistence Hook

Create `usePersistentReducer`: initializer parses localStorage through a validator; effect writes state and handles quota/security errors. Do not accept arbitrary stored JSON as `Course[]` without checking.

## Step 6: Test

```tsx
test("filters and toggles a course", async () => {
  const user = userEvent.setup();
  render(<Planner />);
  await user.type(screen.getByRole("textbox", { name: /search/i }), "React");
  await user.click(screen.getByRole("button", { name: "Plan" }));
  expect(screen.getByRole("button", { name: "Planned" })).toHaveAttribute("aria-pressed", "true");
});
// Test output: passes when user-visible filter and toggle behavior work.
```

## Interview Review

1. Why is filtered data calculated during rendering instead of stored in state?
   **Answer:** It is derived from existing state; storing it separately creates synchronization bugs and unnecessary renders.
2. Why must list keys come from stable course IDs?
   **Answer:** Stable keys preserve component identity and prevent state from moving to the wrong row after insertions or reordering.
3. Why does persistence belong in an Effect but filtering does not?
   **Answer:** Persistence synchronizes React with browser storage, while filtering is a pure calculation from current state.
4. Why validate `localStorage` data at runtime when TypeScript already knows `Course[]`?
   **Answer:** TypeScript checks source code, not untrusted data read at runtime; stored JSON can be missing, stale, or malformed.
5. What does the behavior test prove better than an implementation-detail test?
   **Answer:** It verifies the user-visible contract and remains useful when internal component structure changes.

## Completion Definition

No duplicate state/effect, stable keys, immutable exhaustive reducer, runtime-validated storage, semantic controls, keyboard operation, explicit empty/error status, behavior test passes, and Profiler shows no obvious repeated heavy work.
