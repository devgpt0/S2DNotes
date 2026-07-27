# React: beginner-to-expert essential notes

React builds user interfaces from **components**. A component is a function that receives inputs (props) and returns UI. When state changes, React renders again and updates the necessary DOM.

## 1. Components, JSX, and props

```tsx
type GreetingProps = { name: string };

function Greeting({ name }: GreetingProps) {
  return <h1>Hello, {name}</h1>;
}
```

Components start with a capital letter. JSX looks like HTML but is JavaScript syntax: use `className`, braces for expressions, and close tags. Props flow **down** from parent to child and should be treated as read-only.

Use composition: pass children or render smaller components instead of making one huge configurable component.

## 2. State, snapshots, batching, and events

State is data that changes over time and affects what React displays.

```tsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount((current) => current + 1)}>{count}</button>;
}
```

Never mutate state directly. Make a new object/array and call its setter. When the next value depends on the previous value, use the updater form: `setCount(current => current + 1)`.

Each render sees a snapshot of state. Calling a setter requests another render; it does not change the variable inside the current event handler. React batches updates during an event.

Events use camelCase: `onClick`, `onChange`, `onSubmit`. For a form, call `event.preventDefault()` in `onSubmit` to handle it in JavaScript.

## 3. Rendering lists, conditions, and keys

```tsx
type Todo = { id: string; title: string; done: boolean };

function TodoList({ todos }: { todos: Todo[] }) {
  if (todos.length === 0) return <p>No todos yet.</p>;
  return <ul>{todos.map((todo) => <li key={todo.id}>{todo.title}</li>)}</ul>;
}
```

Use `&&`, ternaries, or early returns for conditional UI. A `key` identifies a list item between renders. Use a stable ID from data; do not use an array index when items can be inserted, deleted, or reordered. Keys belong on the element directly returned by `map`.

## 4. Effects and data fetching

Rendering must be pure: given the same props/state, it returns the same UI and does not change the outside world. An effect synchronizes React with an external system: network request, subscription, timer, or browser API.

```tsx
import { useEffect, useState } from "react";

function UserName({ id }: { id: string }) {
  const [name, setName] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch(`/api/users/${encodeURIComponent(id)}`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error("Could not load user");
        return response.json();
      })
      .then((value: unknown) => {
        if (typeof value !== "object" || value === null || !("name" in value) || typeof value.name !== "string") {
          throw new TypeError("Invalid user response");
        }
        setName(value.name);
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === "AbortError") return;
        throw error;
      });
    return () => controller.abort();
  }, [id]);

  return <p>{name ?? "Loading…"}</p>;
}
```

The dependency array lists values read by the effect that can change. `[]` means only after mount; no array means after every render. Do not use an effect to calculate a value from props/state—calculate it during render instead. Effects should clean up subscriptions, timers, and in-flight work.

## 5. Reducers, custom hooks, refs, and context

Use `useReducer` when state transitions are related and benefit from explicit actions:

```tsx
type State = { count: number };
type Action = { type: "increment" } | { type: "reset" };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "increment": return { count: state.count + 1 };
    case "reset": return { count: 0 };
  }
}
```

A custom hook is a function beginning with `use` that combines reusable hook logic. It shares logic, not state—each call owns its state. `useRef` stores mutable information without rendering and references DOM nodes. Do not read or write refs during render except predictable initialization.

Context avoids passing the same value through many levels. Split frequently changing contexts, keep providers close to consumers, and do not use context for every local value.

## 6. State design and performance

- Keep state as small as possible. Derive `filteredTodos` from `todos` and the filter; do not store a duplicate.
- Lift state up to the closest shared parent when siblings need it.
- Use controlled inputs when React state is the source of truth: `value={name}` and `onChange={...}`.
- `useRef` stores a value between renders without causing a render; it is also used for DOM nodes.
- Context shares broadly needed values (theme, authenticated user). It is not a replacement for all state management.
- `useMemo` caches an expensive calculated value; `useCallback` caches a function reference; `memo` can skip a child render when props are unchanged. Use them only after measuring a real rerender problem.

## 7. Rendering lifecycle and component identity

```text
state/props change → render functions run → React compares trees → DOM commit → effects run
```

React preserves state while the same component remains at the same tree position. Changing its `key` or component type resets its state. Never define a component inside another component; it creates a new component type on each render.

Strict Mode may intentionally render and run effect setup/cleanup extra times in development to expose impure code. Production is not double-rendered for this check.

## 8. Errors, Suspense, and application structure

Error boundaries catch rendering errors in their descendant tree and show fallback UI; they do not catch ordinary event-handler or arbitrary async errors. Use framework/router error handling where appropriate.

`lazy` loads a component only when needed; `Suspense` shows a fallback while a supported child is waiting. Prefer framework data APIs or a well-designed server-state library for serious data fetching, caching, cancellation, retries, and race handling.

Keep server state, URL state, form state, and local UI state in the tool that owns them. Do not copy server data into multiple states without a reason.

## 9. Testing

Test behavior visible to the user. Query by accessible role and name, interact as a user would, and assert the result. Avoid testing component internals or hook call counts. Keep pure business logic outside components when it can be tested directly.

## 10. Rules of Hooks, security, and accessibility

Call hooks only at the top level of a React component or custom hook—never inside loops, conditions, or nested functions. React relies on hook call order.

Use semantic HTML in JSX: real `<button>`, `<label>`, heading order, visible focus, and meaningful alternative text. React escapes text values by default; avoid `dangerouslySetInnerHTML` unless the HTML is trusted and sanitized.

## 11. Common mistakes

- Mutating state or props.
- Using an effect for derived data or an event-specific action.
- Missing effect dependencies or disabling the dependency rule.
- Using unstable/random list keys.
- Copying props into state and letting them drift apart.
- Memoizing everything without measurement.
- Creating a new component type inside a render.
- Putting secrets in frontend code or rendering untrusted HTML.

## Interview checklist

Explain props vs state, controlled components, immutable updates, rendering and reconciliation, list keys, lifting state up, effect purpose/dependencies/cleanup, refs, context, memoization tradeoffs, and Rules of Hooks.
