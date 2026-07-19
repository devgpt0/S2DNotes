# 99 - Build a Course Planner in 60 Minutes

## Project Overview

Build a React 19 course planner with strict TypeScript. Users can search, add, plan, and remove courses. State updates are immutable and exhaustive. Browser storage is checked at runtime before React trusts it.

## What You Will Learn

- component, prop, and state ownership
- controlled form inputs and user events
- reducer actions and exhaustive TypeScript unions
- derived filtered UI and stable list keys
- strict runtime validation at local-storage boundaries
- accessible status, empty, error, and action states
- focused reducer tests and production builds

## Folder Structure

```text
react-course-planner/
|-- index.html
|-- package.json
|-- tsconfig.json
|-- vite.config.ts
`-- src/
    |-- App.tsx
    |-- course.test.ts
    |-- course.ts
    |-- main.tsx
    `-- styles.css
```

The lockfile, installed packages, and `dist` folder are generated.

## File: `package.json`

```json
{
  "name": "react-course-planner",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "test": "vitest run"
  },
  "dependencies": {
    "react": "^19.1.0",
    "react-dom": "^19.1.0"
  },
  "devDependencies": {
    "@types/react": "^19.1.0",
    "@types/react-dom": "^19.1.0",
    "@vitejs/plugin-react": "^4.6.0",
    "typescript": "^5.8.0",
    "vite": "^7.0.0",
    "vitest": "^3.2.0"
  }
}
```

Concepts learned from this file:

- React is a runtime dependency; Vite and type/test tools are development dependencies.
- the build fails if strict type checking fails.
- `private` prevents accidental package publication.

## File: `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "noEmit": true
  },
  "include": ["src", "vite.config.ts"]
}
```

Concepts learned from this file:

- the modern JSX transform avoids manual `React` imports.
- strict null and index checks expose impossible assumptions early.
- Vite emits assets, while TypeScript checks types only.

## File: `vite.config.ts`

```typescript
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  test: {
    include: ["src/**/*.test.ts"],
  },
});
```

Concepts learned from this file:

- the React plugin handles JSX development behavior and production transformation.
- test discovery is intentionally limited to this project's test files.

## File: `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Plan frontend learning courses.">
    <title>Course Planner</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

Concepts learned from this file:

- React mounts into one known root element.
- the HTML keeps document metadata and delegates application UI to React.

## File: `src/course.ts`

```typescript
export type Course = Readonly<{
  id: string;
  title: string;
  planned: boolean;
}>;

export type CourseAction =
  | Readonly<{ type: "added"; course: Course }>
  | Readonly<{ type: "toggled"; id: string }>
  | Readonly<{ type: "removed"; id: string }>;

export function isCourse(value: unknown): value is Course {
  return typeof value === "object"
    && value !== null
    && "id" in value
    && typeof value.id === "string"
    && value.id.length > 0
    && "title" in value
    && typeof value.title === "string"
    && value.title.length > 0
    && "planned" in value
    && typeof value.planned === "boolean";
}

export function courseReducer(
  courses: readonly Course[],
  action: CourseAction,
): readonly Course[] {
  switch (action.type) {
    case "added":
      if (!isCourse(action.course)) throw new TypeError("course is invalid");
      return [...courses, action.course];
    case "toggled":
      if (!courses.some((course) => course.id === action.id)) {
        throw new RangeError(`unknown course id: ${action.id}`);
      }
      return courses.map((course) =>
        course.id === action.id
          ? { ...course, planned: !course.planned }
          : course,
      );
    case "removed":
      if (!courses.some((course) => course.id === action.id)) {
        throw new RangeError(`unknown course id: ${action.id}`);
      }
      return courses.filter((course) => course.id !== action.id);
    default:
      return action satisfies never;
  }
}

export function parseCourses(serialized: string): readonly Course[] {
  const value: unknown = JSON.parse(serialized);
  if (!Array.isArray(value) || !value.every(isCourse)) {
    throw new TypeError("stored courses do not match the course schema");
  }
  return value;
}
```

Concepts learned from this file:

- readonly types state ownership expectations.
- a discriminated union lists every legal state transition.
- the `never` check makes a new unhandled action fail type checking.
- JSON is `unknown` until all required properties pass runtime checks.

## File: `src/App.tsx`

```tsx
import { useReducer, useState, type FormEvent } from "react";
import {
  courseReducer,
  parseCourses,
  type Course,
  type CourseAction,
} from "./course";

const STORAGE_KEY = "react-course-planner.courses";
const initialCourses: readonly Course[] = [
  { id: "java", title: "Java Foundations", planned: true },
  { id: "react", title: "React Essentials", planned: false },
];

type InitialState =
  | Readonly<{ status: "ready"; courses: readonly Course[] }>
  | Readonly<{ status: "error"; message: string }>;

function loadInitialState(): InitialState {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return {
      status: "ready",
      courses: stored === null ? initialCourses : parseCourses(stored),
    };
  } catch (error: unknown) {
    return {
      status: "error",
      message: error instanceof Error ? error.message : "courses could not be loaded",
    };
  }
}

export default function App() {
  const [initialState] = useState(loadInitialState);
  if (initialState.status === "error") {
    return <main className="shell"><h1>Course planner</h1><p role="alert">Could not start: {initialState.message}</p></main>;
  }

  return <CoursePlanner initialCourses={initialState.courses} />;
}

function CoursePlanner({ initialCourses: coursesAtStart }: { initialCourses: readonly Course[] }) {
  const [courses, dispatch] = useReducer(courseReducer, coursesAtStart);
  const [query, setQuery] = useState("");
  const [title, setTitle] = useState("");
  const [message, setMessage] = useState("");

  const visibleCourses = courses.filter((course) =>
    course.title.toLocaleLowerCase().includes(query.toLocaleLowerCase()),
  );

  function commit(action: CourseAction, successMessage: string): void {
    const nextCourses = courseReducer(courses, action);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextCourses));
    dispatch(action);
    setMessage(successMessage);
  }

  function addCourse(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const cleanTitle = title.trim();
    if (cleanTitle.length === 0) throw new TypeError("course title is required");
    commit(
      { type: "added", course: { id: crypto.randomUUID(), title: cleanTitle, planned: false } },
      `${cleanTitle} added`,
    );
    setTitle("");
  }

  return (
    <main className="shell">
      <header><p className="eyebrow">React project</p><h1>Course planner</h1><p>Choose the next skill you want to practice.</p></header>

      <section aria-labelledby="add-heading">
        <h2 id="add-heading">Add a course</h2>
        <form className="form-row" onSubmit={addCourse}>
          <label htmlFor="course-title">Course title</label>
          <input id="course-title" value={title} onChange={(event) => setTitle(event.currentTarget.value)} required maxLength={80} />
          <button type="submit">Add course</button>
        </form>
      </section>

      <section aria-labelledby="courses-heading">
        <div className="toolbar">
          <h2 id="courses-heading">Courses</h2>
          <label htmlFor="search">Search</label>
          <input id="search" type="search" value={query} onChange={(event) => setQuery(event.currentTarget.value)} />
        </div>
        <p role="status">{message || `${visibleCourses.length} courses shown`}</p>
        {visibleCourses.length === 0 ? <p>No courses match your search.</p> : (
          <ul className="course-list">
            {visibleCourses.map((course) => (
              <li key={course.id}>
                <span>{course.title}</span>
                <button type="button" aria-pressed={course.planned} onClick={() => commit({ type: "toggled", id: course.id }, `${course.title} updated`)}>
                  {course.planned ? "Planned" : "Plan"}
                </button>
                <button type="button" onClick={() => commit({ type: "removed", id: course.id }, `${course.title} removed`)}>
                  Delete <span className="visually-hidden">{course.title}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
```

Concepts learned from this file:

- startup data is loaded once and invalid data produces an explicit fatal state.
- filtered courses are derived during rendering instead of synchronized through an Effect.
- persistence occurs before reducer dispatch, so failed storage does not commit UI state.
- stable IDs preserve list identity; random keys are never created during rendering.
- controlled inputs keep each draft close to the form that owns it.

## File: `src/main.tsx`

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

const root = document.querySelector("#root");
if (!(root instanceof HTMLDivElement)) throw new Error("root element is missing");

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

Concepts learned from this file:

- the root dependency is checked before mounting.
- `StrictMode` helps expose unsafe render and cleanup behavior during development.
- the entry file owns global CSS loading and application mounting.

## File: `src/styles.css`

```css
*, *::before, *::after { box-sizing: border-box; }
:root { color-scheme: light dark; font-family: ui-sans-serif, system-ui, sans-serif; line-height: 1.5; --brand: #3157d5; --border: color-mix(in srgb, currentColor 22%, transparent); }
body { margin: 0; min-block-size: 100dvh; }
button, input { min-block-size: 2.75rem; font: inherit; }
:focus-visible { outline: 0.2rem solid var(--brand); outline-offset: 0.2rem; }
.shell { inline-size: min(100% - 2rem, 52rem); margin-inline: auto; padding-block: 3rem; }
.shell > * + * { margin-block-start: 2.5rem; }
.eyebrow { color: var(--brand); font-weight: 800; text-transform: uppercase; }
.form-row { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 0.75rem; }
.form-row label { grid-column: 1 / -1; }
.toolbar { display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem; }
.toolbar h2 { margin-inline-end: auto; }
.course-list { display: grid; gap: 0.75rem; padding: 0; list-style: none; }
.course-list li { display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem; padding: 1rem; border: 1px solid var(--border); border-radius: 0.75rem; }
.course-list li > span { flex: 1 1 14rem; overflow-wrap: anywhere; }
.visually-hidden { position: absolute; inline-size: 1px; block-size: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
@media (max-width: 30rem) { .form-row { grid-template-columns: 1fr; } }
```

Concepts learned from this file:

- the UI responds to available space and zoom without React viewport logic.
- flexible rows allow long translated titles without page overflow.
- visually hidden text gives repeated delete buttons unique accessible names.

## File: `src/course.test.ts`

```typescript
import { expect, test } from "vitest";
import { courseReducer, parseCourses, type Course } from "./course";

const course: Course = { id: "java", title: "Java", planned: false };

test("toggles without mutating prior state", () => {
  const before = [course] as const;
  const after = courseReducer(before, { type: "toggled", id: "java" });
  expect(before[0].planned).toBe(false);
  expect(after[0]?.planned).toBe(true);
});

test("rejects invalid stored course data", () => {
  expect(() => parseCourses('[{"id":"java","title":"Java","planned":"yes"}]'))
    .toThrow(TypeError);
});
```

Concepts learned from this file:

- pure reducer behavior is tested without rendering components.
- tests preserve immutability and runtime-validation contracts.

## Run and Verify

```powershell
npm install
npm run test
npm run build
npm run dev
# Test result: 2 tests pass.
```

Test add, search, plan, delete, reload, corrupted storage, keyboard use, 320px width, 200% zoom, and long titles. Use React DevTools Profiler only after finding a visible performance issue; this small list does not need memoization.

## Completion Definition

Every file exists, strict build and tests pass, invalid stored data stops safely, no derived-state Effect exists, list keys are stable, the UI remains accessible and responsive, and every per-file concept can be explained.
