# 99 - Build an Accessible Task Board in 60 Minutes

## Project Overview

Build a small task board with standard browser APIs and JavaScript modules. A learner can add, complete, filter, and delete tasks. Valid tasks persist across reloads. Invalid stored data stops startup with a visible error instead of being silently trusted.

The project separates pure state changes, the storage boundary, and DOM behavior so each part has one clear responsibility.

## What You Will Learn

- semantic HTML, labelled controls, live status, and keyboard behavior
- ES modules and explicit imports
- immutable state updates and derived filtered views
- event delegation and `data-*` attributes
- safe DOM rendering with `textContent`
- strict runtime validation at a storage boundary
- explicit startup and persistence failures
- unit testing pure functions without a browser

## Time Plan

| Minutes | Work |
|---:|---|
| 0-8 | Create the files and install the development tools |
| 8-18 | Build semantic HTML and basic responsive CSS |
| 18-30 | Implement and test pure state transitions |
| 30-38 | Validate storage data |
| 38-53 | Render state and connect delegated events |
| 53-60 | Test keyboard use, reloads, and failure cases |

## Folder Structure

```text
javascript-task-board/
|-- index.html
|-- package.json
|-- styles.css
|-- src/
|   |-- app.js
|   |-- state.js
|   `-- storage.js
`-- tests/
    `-- state.test.js
```

`node_modules`, `package-lock.json`, and build output are generated, so they are not hand-written project files.

## File: `package.json`

```json
{
  "name": "javascript-task-board",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest run"
  },
  "devDependencies": {
    "vite": "^7.0.0",
    "vitest": "^3.2.0"
  }
}
```

Concepts learned from this file:

- `private` prevents accidental publication to npm.
- `type: module` makes `.js` files use ES module rules.
- separate scripts make development, production building, and tests explicit.

## File: `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="A small accessible JavaScript task board.">
    <title>Task Board</title>
    <link rel="stylesheet" href="/styles.css">
  </head>
  <body>
    <main class="shell">
      <header>
        <p class="eyebrow">JavaScript project</p>
        <h1>Task board</h1>
        <p>Add a task, keep it focused, and mark it complete.</p>
      </header>

      <section aria-labelledby="add-heading">
        <h2 id="add-heading">Add a task</h2>
        <form id="task-form">
          <label for="task-text">Task</label>
          <div class="form-row">
            <input id="task-text" name="task" required maxlength="100" autocomplete="off">
            <button type="submit">Add task</button>
          </div>
        </form>
      </section>

      <section aria-labelledby="tasks-heading">
        <div class="section-heading">
          <h2 id="tasks-heading">Tasks</h2>
          <fieldset id="task-filter">
            <legend>Show</legend>
            <label><input type="radio" name="filter" value="all" checked> All</label>
            <label><input type="radio" name="filter" value="active"> Active</label>
            <label><input type="radio" name="filter" value="completed"> Completed</label>
          </fieldset>
        </div>

        <p id="status" role="status" aria-live="polite"></p>
        <p id="fatal-error" role="alert" hidden></p>
        <ul id="task-list" class="task-list"></ul>
      </section>
    </main>
    <script type="module" src="/src/app.js"></script>
  </body>
</html>
```

Concepts learned from this file:

- headings and sections expose a meaningful document outline.
- `label`, `fieldset`, and `legend` give controls accessible names and grouping.
- `role="status"` announces ordinary updates; `role="alert"` announces a fatal startup failure.
- a module script is deferred automatically and keeps imports explicit.

## File: `styles.css`

```css
*, *::before, *::after { box-sizing: border-box; }

:root {
  color-scheme: light dark;
  font-family: ui-sans-serif, system-ui, sans-serif;
  line-height: 1.5;
  --brand: #3157d5;
  --border: color-mix(in srgb, currentColor 22%, transparent);
}

body { margin: 0; min-block-size: 100dvh; }
button, input { font: inherit; }
button { min-block-size: 2.75rem; cursor: pointer; }
input { min-inline-size: 0; min-block-size: 2.75rem; padding-inline: 0.75rem; }
:focus-visible { outline: 0.2rem solid var(--brand); outline-offset: 0.2rem; }

.shell { inline-size: min(100% - 2rem, 48rem); margin-inline: auto; padding-block: 3rem; }
.shell > * + * { margin-block-start: 2.5rem; }
.eyebrow { color: var(--brand); font-size: 0.8rem; font-weight: 800; text-transform: uppercase; }
.form-row { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 0.75rem; }
.section-heading { display: flex; flex-wrap: wrap; align-items: end; justify-content: space-between; gap: 1rem; }
fieldset { display: flex; flex-wrap: wrap; gap: 0.75rem; border: 1px solid var(--border); }
.task-list { display: grid; gap: 0.75rem; padding: 0; list-style: none; }
.task { display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem; padding: 1rem; border: 1px solid var(--border); border-radius: 0.75rem; }
.task__text { flex: 1 1 16rem; overflow-wrap: anywhere; }
.task[data-completed="true"] .task__text { text-decoration: line-through; opacity: 0.7; }

@media (max-width: 30rem) {
  .form-row { grid-template-columns: 1fr; }
}
```

Concepts learned from this file:

- intrinsic widths and `minmax(0, 1fr)` prevent narrow-screen overflow.
- a flex-wrapped task row remains usable with zoom and long content.
- `data-completed` connects state to presentation without fragile class-name branching.
- visible focus and minimum control height improve keyboard and touch use.

## File: `src/state.js`

```javascript
export const FILTERS = Object.freeze(["all", "active", "completed"]);

export function addTask(tasks, text, id = crypto.randomUUID()) {
  if (!Array.isArray(tasks)) throw new TypeError("tasks must be an array");
  if (typeof text !== "string" || text.trim().length === 0) {
    throw new TypeError("task text must be a non-empty string");
  }
  if (typeof id !== "string" || id.length === 0) {
    throw new TypeError("task id must be a non-empty string");
  }

  return [...tasks, { id, text: text.trim(), completed: false }];
}

export function toggleTask(tasks, id) {
  if (!tasks.some((task) => task.id === id)) {
    throw new RangeError(`unknown task id: ${id}`);
  }

  return tasks.map((task) =>
    task.id === id ? { ...task, completed: !task.completed } : task,
  );
}

export function removeTask(tasks, id) {
  if (!tasks.some((task) => task.id === id)) {
    throw new RangeError(`unknown task id: ${id}`);
  }
  return tasks.filter((task) => task.id !== id);
}

export function visibleTasks(tasks, filter) {
  if (!FILTERS.includes(filter)) throw new RangeError(`unknown filter: ${filter}`);
  if (filter === "all") return tasks;
  const completed = filter === "completed";
  return tasks.filter((task) => task.completed === completed);
}
```

Concepts learned from this file:

- state functions fail immediately for invalid operations.
- spread, `map`, and `filter` return new arrays instead of mutating prior state.
- filtered tasks are derived from canonical state rather than stored twice.
- dependency injection through the optional `id` makes `addTask` deterministic in tests.

## File: `src/storage.js`

```javascript
const STORAGE_KEY = "javascript-task-board.tasks";

function isTask(value) {
  return typeof value === "object"
    && value !== null
    && typeof value.id === "string"
    && value.id.length > 0
    && typeof value.text === "string"
    && value.text.length > 0
    && typeof value.completed === "boolean";
}

export function loadTasks(storage = localStorage) {
  const serialized = storage.getItem(STORAGE_KEY);
  if (serialized === null) return [];

  const value = JSON.parse(serialized);
  if (!Array.isArray(value) || !value.every(isTask)) {
    throw new TypeError("stored tasks do not match the task schema");
  }
  return value;
}

export function saveTasks(tasks, storage = localStorage) {
  if (!Array.isArray(tasks) || !tasks.every(isTask)) {
    throw new TypeError("refusing to store invalid tasks");
  }
  storage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}
```

Concepts learned from this file:

- parsed JSON is untrusted until every item and property is checked.
- validation verifies types; it does not coerce or repair corrupted data.
- injected storage makes the boundary testable without wrapping browser APIs.
- JSON syntax, quota, and security errors propagate to the caller for explicit handling.

## File: `src/app.js`

```javascript
import { addTask, removeTask, toggleTask, visibleTasks } from "./state.js";
import { loadTasks, saveTasks } from "./storage.js";

const form = document.querySelector("#task-form");
const input = document.querySelector("#task-text");
const filterGroup = document.querySelector("#task-filter");
const list = document.querySelector("#task-list");
const status = document.querySelector("#status");
const fatalError = document.querySelector("#fatal-error");

if (!(form instanceof HTMLFormElement)
  || !(input instanceof HTMLInputElement)
  || !(filterGroup instanceof HTMLFieldSetElement)
  || !(list instanceof HTMLUListElement)
  || !(status instanceof HTMLParagraphElement)
  || !(fatalError instanceof HTMLParagraphElement)) {
  throw new Error("required task board elements are missing");
}

let tasks;
let filter = "all";

function taskElement(task) {
  const item = document.createElement("li");
  item.className = "task";
  item.dataset.id = task.id;
  item.dataset.completed = String(task.completed);

  const text = document.createElement("span");
  text.className = "task__text";
  text.textContent = task.text;

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.dataset.action = "toggle";
  toggle.textContent = task.completed ? "Reopen" : "Complete";
  toggle.setAttribute("aria-label", `${toggle.textContent} ${task.text}`);

  const remove = document.createElement("button");
  remove.type = "button";
  remove.dataset.action = "remove";
  remove.textContent = "Delete";
  remove.setAttribute("aria-label", `Delete ${task.text}`);

  item.append(text, toggle, remove);
  return item;
}

function render() {
  const visible = visibleTasks(tasks, filter);
  list.replaceChildren(...visible.map(taskElement));
  status.textContent = `${visible.length} of ${tasks.length} tasks shown`;
}

function commit(nextTasks) {
  saveTasks(nextTasks);
  tasks = nextTasks;
  render();
}

function start() {
  tasks = loadTasks();
  render();

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    commit(addTask(tasks, input.value));
    form.reset();
    input.focus();
  });

  filterGroup.addEventListener("change", (event) => {
    if (!(event.target instanceof HTMLInputElement)) return;
    filter = event.target.value;
    render();
  });

  list.addEventListener("click", (event) => {
    if (!(event.target instanceof Element)) return;
    const button = event.target.closest("button[data-action]");
    const item = button?.closest("li[data-id]");
    if (!(button instanceof HTMLButtonElement) || !(item instanceof HTMLLIElement)) return;

    const nextTasks = button.dataset.action === "toggle"
      ? toggleTask(tasks, item.dataset.id)
      : removeTask(tasks, item.dataset.id);
    commit(nextTasks);
  });
}

try {
  start();
} catch (error) {
  fatalError.hidden = false;
  fatalError.textContent = error instanceof Error
    ? `Task board could not start: ${error.message}`
    : "Task board could not start.";
  form.inert = true;
  filterGroup.disabled = true;
}
```

Concepts learned from this file:

- startup checks required DOM dependencies before behavior is attached.
- rendering uses `textContent`, so a task cannot inject HTML.
- one delegated list listener handles buttons added during later renders.
- `commit` persists first; failed persistence leaves in-memory and stored state consistent.
- the boundary catch handles a known UI responsibility: stop interaction and show an actionable failure.

## File: `tests/state.test.js`

```javascript
import { describe, expect, test } from "vitest";
import { addTask, toggleTask, visibleTasks } from "../src/state.js";

describe("task state", () => {
  test("adds a trimmed task without mutating prior state", () => {
    const before = [];
    const after = addTask(before, "  Learn closures  ", "task-1");

    expect(before).toEqual([]);
    expect(after).toEqual([
      { id: "task-1", text: "Learn closures", completed: false },
    ]);
  });

  test("toggles and derives completed tasks", () => {
    const tasks = addTask([], "Learn modules", "task-1");
    const toggled = toggleTask(tasks, "task-1");

    expect(visibleTasks(toggled, "completed")).toEqual(toggled);
    expect(tasks[0].completed).toBe(false);
  });

  test("rejects an unknown task id", () => {
    expect(() => toggleTask([], "missing")).toThrow(RangeError);
  });
});
```

Concepts learned from this file:

- tests verify public behavior and immutability, not implementation details.
- injected IDs remove randomness from expectations.
- a failure-path test preserves the fail-fast contract.

## Run the Project

```powershell
npm install
npm run test
npm run dev
# Test result: 3 tests pass.
# Dev result: Vite prints a local URL, normally http://localhost:5173.
```

Run `npm run build` before delivery. Open the printed local URL instead of opening the file directly because ES modules and development tooling expect an HTTP origin.

## Expected Behavior

1. An empty task is blocked by native validation.
2. Adding a task trims its outer whitespace and returns focus to the input.
3. Complete, reopen, and delete work from one delegated event listener.
4. Filters change only the visible view, not canonical task state.
5. Reloading restores valid tasks.
6. Corrupting the storage value in DevTools stops the board and displays a clear error.

## Browser Verification

- complete the full flow with only the keyboard
- test at 320px width and 200% zoom
- enter `<img src=x onerror=alert(1)>` and verify it is displayed as text
- inspect the Elements panel and confirm accessible control names
- inspect Application > Local Storage and verify the stored schema
- record a Performance trace with 100 tasks and check that one user action causes one render

## Practice Extensions

1. Add an edit operation while keeping one canonical task array.
2. Add a clear-completed action with a confirmation dialog.
3. Add storage tests with a small in-memory `Storage` implementation.
4. Move focus predictably after deleting the currently focused task.

## Interview Review

### Why derive filtered tasks instead of storing them?

The filtered list is a calculation from tasks and the current filter. Storing it creates a second source of truth that can become stale.

### Why use event delegation?

Task buttons are recreated during rendering. One stable listener on the list observes bubbled clicks without attaching and cleaning up a listener for every row.

### Why is `textContent` safer than `innerHTML` here?

Task text is user input. `textContent` creates text, while `innerHTML` interprets markup and can create an XSS vulnerability.

### Why validate local storage?

Browser storage can be edited, corrupted, or left behind by an older application version. Parsed JSON has no automatic schema guarantee.

## Completion Definition

The project is complete when tests and the production build pass, keyboard and narrow-screen flows work, invalid data stops startup visibly, untrusted text is never interpreted as HTML, and you can explain the concept section for every file.
