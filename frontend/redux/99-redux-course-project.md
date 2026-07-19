# 99 - Build a Redux Toolkit Course Planner

## Project Overview

Build a React and TypeScript course planner using Redux Toolkit and React Redux. Users add, plan, select, and remove courses. Reducers protect state transitions, selectors derive views, components use typed hooks, and tests exercise the real reducer.

This project intentionally has no API. Its state is a client workflow, making a slice appropriate. Use RTK Query when the course list comes from a server.

## What You Will Learn

- configure one Redux store
- model a feature slice and domain actions
- use Immer-backed reducer syntax safely
- create typed React Redux hooks
- select minimal and derived state
- keep form drafts local
- test reducer behavior and failure cases

## Folder Structure

```text
redux-course-planner/
|-- index.html
|-- package.json
|-- tsconfig.json
|-- vite.config.ts
`-- src/
    |-- App.tsx
    |-- main.tsx
    |-- styles.css
    `-- app/
        |-- hooks.ts
        |-- store.ts
        |-- courses.test.ts
        `-- courses.ts
```

The lockfile, dependencies, and `dist` output are generated.

## File: `package.json`

```json
{
  "name": "redux-course-planner",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "test": "vitest run"
  },
  "dependencies": {
    "@reduxjs/toolkit": "^2.8.0",
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "react-redux": "^9.2.0"
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

- Redux Toolkit and React Redux are runtime dependencies.
- the build requires strict type checking before bundling.
- reducer tests run independently from the browser UI.

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

- strict settings apply to slice, selectors, store, tests, and UI.
- bundler resolution matches Vite.
- unchecked indexes remain possibly undefined.

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

- Vite transforms React JSX.
- Vitest discovers only the project's test files.

## File: `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Plan courses with Redux Toolkit.">
    <title>Redux Course Planner</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

Concepts learned from this file:

- the document owns metadata.
- React mounts below one validated root element.

## File: `src/app/courses.ts`

```typescript
import { createSelector, createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "./store";

export type Course = Readonly<{
  id: string;
  title: string;
  planned: boolean;
}>;

type CoursesState = {
  items: Course[];
  selectedId: string | null;
};

const initialState: CoursesState = {
  items: [
    { id: "javascript", title: "JavaScript", planned: true },
    { id: "typescript", title: "TypeScript", planned: false },
  ],
  selectedId: null,
};

const coursesSlice = createSlice({
  name: "courses",
  initialState,
  reducers: {
    courseAdded(state, action: PayloadAction<Course>) {
      if (state.items.some((course) => course.id === action.payload.id)) {
        throw new RangeError(`duplicate course id: ${action.payload.id}`);
      }
      state.items.push(action.payload);
    },
    courseToggled(state, action: PayloadAction<string>) {
      const course = state.items.find((item) => item.id === action.payload);
      if (course === undefined) throw new RangeError("course not found");
      course.planned = !course.planned;
    },
    courseSelected(state, action: PayloadAction<string | null>) {
      const id = action.payload;
      if (id !== null && !state.items.some((course) => course.id === id)) {
        throw new RangeError("selected course not found");
      }
      state.selectedId = id;
    },
    courseRemoved(state, action: PayloadAction<string>) {
      const index = state.items.findIndex((course) => course.id === action.payload);
      if (index === -1) throw new RangeError("course not found");
      state.items.splice(index, 1);
      if (state.selectedId === action.payload) state.selectedId = null;
    },
  },
});

export const {
  courseAdded,
  courseRemoved,
  courseSelected,
  courseToggled,
} = coursesSlice.actions;
export const coursesReducer = coursesSlice.reducer;

export const selectCourses = (state: RootState): readonly Course[] => {
  return state.courses.items;
};

export const selectSelectedCourse = (state: RootState): Course | undefined => {
  return state.courses.items.find(
    (course) => course.id === state.courses.selectedId,
  );
};

export const selectPlannedCount = createSelector(
  [selectCourses],
  (courses) => courses.filter((course) => course.planned).length,
);
```

Concepts learned from this file:

- the slice owns cohesive course workflow state.
- actions describe domain events rather than generic setters.
- mutation-like reducer code produces immutable results through Immer.
- reducers reject unknown or duplicate IDs.
- selectors hide the slice's storage shape and derive values.

## File: `src/app/store.ts`

```typescript
import { configureStore } from "@reduxjs/toolkit";
import { coursesReducer } from "./courses";

export const createAppStore = () => configureStore({
  reducer: {
    courses: coursesReducer,
  },
});

export const store = createAppStore();
export type AppStore = ReturnType<typeof createAppStore>;
export type RootState = ReturnType<AppStore["getState"]>;
export type AppDispatch = AppStore["dispatch"];
```

Concepts learned from this file:

- one store factory supports isolated tests and browser setup.
- state and dispatch types come from the actual store configuration.
- Toolkit default middleware keeps useful development checks.

## File: `src/app/hooks.ts`

```typescript
import { useDispatch, useSelector, useStore } from "react-redux";
import type { AppDispatch, AppStore, RootState } from "./store";

export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
export const useAppStore = useStore.withTypes<AppStore>();
```

Concepts learned from this file:

- typed hooks keep store types out of every component call.
- hooks are application-specific, while React Redux remains generic.

## File: `src/App.tsx`

```tsx
import { useState, type FormEvent } from "react";
import { useAppDispatch, useAppSelector } from "./app/hooks";
import {
  courseAdded,
  courseRemoved,
  courseSelected,
  courseToggled,
  selectCourses,
  selectPlannedCount,
  selectSelectedCourse,
} from "./app/courses";

const App = () => {
  const dispatch = useAppDispatch();
  const courses = useAppSelector(selectCourses);
  const plannedCount = useAppSelector(selectPlannedCount);
  const selectedCourse = useAppSelector(selectSelectedCourse);
  const [title, setTitle] = useState("");

  const submit = (event: FormEvent<HTMLFormElement>): void => {
    event.preventDefault();
    const cleanTitle = title.trim();
    if (cleanTitle.length === 0) throw new TypeError("title is required");
    dispatch(courseAdded({
      id: crypto.randomUUID(),
      title: cleanTitle,
      planned: false,
    }));
    setTitle("");
  };

  return (
    <main className="shell">
      <header>
        <p className="eyebrow">Redux Toolkit project</p>
        <h1>Course planner</h1>
        <p>{plannedCount} of {courses.length} courses planned</p>
      </header>

      <section aria-labelledby="add-heading">
        <h2 id="add-heading">Add course</h2>
        <form className="add-form" onSubmit={submit}>
          <label htmlFor="title">Course title</label>
          <input id="title" value={title} onChange={(event) => setTitle(event.currentTarget.value)} required maxLength={80} />
          <button type="submit">Add</button>
        </form>
      </section>

      <section aria-labelledby="courses-heading">
        <h2 id="courses-heading">Courses</h2>
        {courses.length === 0 ? <p>No courses yet.</p> : (
          <ul className="courses">
            {courses.map((course) => (
              <li key={course.id}>
                <button type="button" className="course-title" onClick={() => dispatch(courseSelected(course.id))}>
                  {course.title}
                </button>
                <button type="button" aria-pressed={course.planned} onClick={() => dispatch(courseToggled(course.id))}>
                  {course.planned ? "Planned" : "Plan"}
                </button>
                <button type="button" onClick={() => dispatch(courseRemoved(course.id))}>
                  Delete <span className="visually-hidden">{course.title}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
        <p role="status">
          {selectedCourse === undefined ? "No course selected" : `Selected: ${selectedCourse.title}`}
        </p>
      </section>
    </main>
  );
};

export default App;
```

Concepts learned from this file:

- store state is read with narrow typed selectors.
- user events dispatch domain actions.
- the form draft remains local because no other feature needs it.
- IDs are created before dispatch, not inside a reducer.
- accessible names distinguish repeated delete actions.

`App` follows the repository convention: a named `const` arrow component with a separate default export. React DevTools still receives the variable name.

## File: `src/main.tsx`

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import App from "./App";
import { store } from "./app/store";
import "./styles.css";

const root = document.querySelector("#root");
if (!(root instanceof HTMLDivElement)) throw new Error("root element is missing");

createRoot(root).render(
  <StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </StrictMode>,
);
```

Concepts learned from this file:

- Provider receives one stable store.
- the entry point owns mounting and global styles.

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
.add-form { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 0.75rem; }
.add-form label { grid-column: 1 / -1; }
.courses { display: grid; gap: 0.75rem; padding: 0; list-style: none; }
.courses li { display: flex; flex-wrap: wrap; gap: 0.75rem; padding: 1rem; border: 1px solid var(--border); border-radius: 0.75rem; }
.course-title { flex: 1 1 14rem; text-align: start; }
.visually-hidden { position: absolute; inline-size: 1px; block-size: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
@media (max-width: 30rem) { .add-form { grid-template-columns: 1fr; } }
```

Concepts learned from this file:

- CSS owns responsive layout rather than Redux or React state.
- flexible rows survive long titles and zoom.
- keyboard focus remains visible.

## File: `src/app/courses.test.ts`

```typescript
import { describe, expect, test } from "vitest";
import {
  courseAdded,
  courseRemoved,
  courseToggled,
  coursesReducer,
} from "./courses";

describe("courses reducer", () => {
  test("adds and toggles without mutating prior state", () => {
    const before = coursesReducer(undefined, { type: "test/init" });
    const added = coursesReducer(before, courseAdded({ id: "redux", title: "Redux", planned: false }));
    const toggled = coursesReducer(added, courseToggled("redux"));

    expect(before.items).toHaveLength(2);
    expect(added.items.find((course) => course.id === "redux")?.planned).toBe(false);
    expect(toggled.items.find((course) => course.id === "redux")?.planned).toBe(true);
  });

  test("rejects an unknown removal", () => {
    const state = coursesReducer(undefined, { type: "test/init" });
    expect(() => coursesReducer(state, courseRemoved("missing"))).toThrow(RangeError);
  });
});
```

Concepts learned from this file:

- tests use the real reducer and action creators.
- prior state remains unchanged.
- invalid transitions are part of the tested contract.

## Run and Verify

```powershell
npm install
npm run test
npm run build
npm run dev
# Test result: 2 tests pass.
```

Use Redux DevTools to inspect each action and state diff. Test keyboard use, add/toggle/select/delete, empty state, 320px width, 200% zoom, and long titles.

## Completion Definition

Every file above exists, strict build and tests pass, form draft stays local, reducers protect transitions, selectors derive state, actions are understandable in DevTools, and the UI remains responsive and accessible.
