# JavaScript 60-Minute Project - Accessible Task Board

## Goal

Build a task board with add, complete, filter, delete, persistence, event delegation, validation, derived state, modules, cleanup, and tests—all without a framework.

## Time Box

- 0-8 min: semantic HTML and module files
- 8-20 min: state and pure functions
- 20-35 min: rendering and events
- 35-45 min: filters and storage
- 45-53 min: accessibility/errors
- 53-60 min: tests and performance audit

## Step 1: State Module

```javascript
// state.js
export function addTask(tasks, text, id = crypto.randomUUID()) {
  if (typeof text !== "string" || text.length === 0) throw new TypeError("text is required");
  return [...tasks, { id, text, completed: false }];
}
export const toggleTask = (tasks, id) => tasks.map(task => task.id === id ? { ...task, completed: !task.completed } : task);
export const removeTask = (tasks, id) => tasks.filter(task => task.id !== id);
// Result: pure functions return new arrays without mutating prior state.
```

## Step 2: Minimal HTML

```html
<form id="task-form"><label for="task">Task</label><input id="task" name="task" required maxlength="100"><button>Add</button></form>
<fieldset><legend>Filter</legend><label><input type="radio" name="filter" value="all" checked> All</label><label><input type="radio" name="filter" value="active"> Active</label><label><input type="radio" name="filter" value="complete"> Complete</label></fieldset>
<p id="status" aria-live="polite"></p><ul id="tasks"></ul>
<script type="module" src="app.js"></script>
<!-- Browser result: labelled form, filter group, live status, task list, deferred module. -->
```

## Step 3: Render Safely

```javascript
function render(tasks, filter) {
  const visible = tasks.filter(task => filter === "all" || (filter === "complete") === task.completed);
  list.replaceChildren(...visible.map(task => {
    const item = document.createElement("li");
    item.dataset.id = task.id;
    const label = document.createElement("span"); label.textContent = task.text;
    const toggle = document.createElement("button"); toggle.type = "button"; toggle.dataset.action = "toggle"; toggle.textContent = task.completed ? "Reopen" : "Complete";
    const remove = document.createElement("button"); remove.type = "button"; remove.dataset.action = "remove"; remove.textContent = "Delete";
    item.append(label, toggle, remove);
    return item;
  }));
  status.textContent = `${visible.length} visible tasks`;
}
// Browser result: safe text nodes and action buttons for current filtered state.
```

## Step 4: Events and Persistence

```javascript
form.addEventListener("submit", event => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  tasks = addTask(tasks, new FormData(form).get("task"));
  save(); render(tasks, filter); form.reset(); input.focus();
});
list.addEventListener("click", event => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const id = button.closest("li").dataset.id;
  tasks = button.dataset.action === "toggle" ? toggleTask(tasks, id) : removeTask(tasks, id);
  save(); render(tasks, filter);
});
// Browser result: submit adds; delegated buttons toggle/delete; state persists and rerenders.
```

Implement `save` with JSON and load through a runtime shape check. Handle storage errors rather than assuming success.

## Step 5: Tests

```javascript
import { test, expect } from "vitest";
import { addTask, toggleTask } from "./state.js";
test("adds without mutation", () => {
  const before = [];
  const after = addTask(before, "Learn closures", "1");
  expect(before).toHaveLength(0);
  expect(toggleTask(after, "1")[0].completed).toBe(true);
});
// Test output: passes when updates are immutable and toggle works.
```

## Expert/Interview Review

Explain module scope, pure functions, closure/resource lifetime, event delegation/bubbling, textContent vs innerHTML, FormData, immutable update, storage trust, runtime validation, focus/live regions, and why rendering is derived from state.

## Completion Definition

Keyboard usable, no unsafe HTML, no mutation, reload persistence, invalid storage handled, empty/filter states correct, listener count constant through delegation, and state tests pass.
