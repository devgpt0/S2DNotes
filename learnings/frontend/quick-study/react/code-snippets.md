# React: 3 commonly asked coding questions

The complete Vite application is in [`examples`](examples/) and displays all three exercises on one page.

```powershell
cd frontend/quick-study/react/examples
npm.cmd install
npm.cmd run dev
```

Open the URL printed by Vite, normally <http://localhost:5173>. Run `npm.cmd run build` to verify the production build.

For a complete React + TypeScript project containing all three examples, follow [the runnable example guide](./examples/README.md).

## 1. Build a counter with correct repeated updates

**Question:** Add increment, decrement, and “increment three times” buttons. Never read a stale state value.

```tsx
import { useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);

  function incrementThreeTimes() {
    for (let index = 0; index < 3; index += 1) {
      setCount((current) => current + 1);
    }
  }

  return (
    <main>
      <p aria-live="polite">Count: {count}</p>
      <button onClick={() => setCount((current) => current - 1)}>Decrease</button>
      <button onClick={() => setCount((current) => current + 1)}>Increase</button>
      <button onClick={incrementThreeTimes}>Increase by 3</button>
    </main>
  );
}
```

## 2. Build an immutable todo list

**Question:** Add, toggle, and remove todos using stable keys and immutable state updates.

```tsx
import { type FormEvent, useState } from "react";

type Todo = { id: string; title: string; done: boolean };

export default function App() {
  const [title, setTitle] = useState("");
  const [todos, setTodos] = useState<Todo[]>([]);

  function addTodo(event: FormEvent) {
    event.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) return;
    setTodos((current) => [...current, { id: crypto.randomUUID(), title: trimmedTitle, done: false }]);
    setTitle("");
  }

  return <main>
    <form onSubmit={addTodo}>
      <label htmlFor="todo">New todo</label>
      <input id="todo" value={title} onChange={(event) => setTitle(event.target.value)} />
      <button type="submit">Add</button>
    </form>
    <ul>{todos.map((todo) => <li key={todo.id}>
      <label><input type="checkbox" checked={todo.done} onChange={() => setTodos((current) => current.map((item) => item.id === todo.id ? { ...item, done: !item.done } : item))} /> {todo.title}</label>
      <button onClick={() => setTodos((current) => current.filter((item) => item.id !== todo.id))}>Remove {todo.title}</button>
    </li>)}</ul>
  </main>;
}
```

## 3. Write a reusable `useDebouncedValue` hook

**Question:** Delay a changing value and correctly clean up obsolete timers.

```tsx
import { useEffect, useState } from "react";

function useDebouncedValue<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timeoutId = window.setTimeout(() => setDebouncedValue(value), delay);
    return () => window.clearTimeout(timeoutId);
  }, [value, delay]);

  return debouncedValue;
}

export default function App() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebouncedValue(query, 400);

  return <main>
    <label htmlFor="search">Search</label>
    <input id="search" value={query} onChange={(event) => setQuery(event.target.value)} />
    <p>Request value: {debouncedQuery || "None"}</p>
  </main>;
}
```
