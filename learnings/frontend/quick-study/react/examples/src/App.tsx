import { type FormEvent, useEffect, useState } from "react";

type Todo = { id: string; title: string; done: boolean };

function Counter() {
  const [count, setCount] = useState(0);

  function incrementThreeTimes() {
    for (let index = 0; index < 3; index += 1) {
      setCount((current) => current + 1);
    }
  }

  return (
    <section>
      <h2>1. Counter with safe updates</h2>
      <p aria-live="polite">Count: {count}</p>
      <div className="actions">
        <button onClick={() => setCount((current) => current - 1)}>Decrease</button>
        <button onClick={() => setCount((current) => current + 1)}>Increase</button>
        <button onClick={incrementThreeTimes}>Increase by 3</button>
      </div>
    </section>
  );
}

function TodoList() {
  const [title, setTitle] = useState("");
  const [todos, setTodos] = useState<Todo[]>([]);

  function addTodo(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) return;
    setTodos((current) => [
      ...current,
      { id: crypto.randomUUID(), title: trimmedTitle, done: false },
    ]);
    setTitle("");
  }

  return (
    <section>
      <h2>2. Immutable todo list</h2>
      <form onSubmit={addTodo}>
        <label htmlFor="todo">New todo</label>
        <div className="actions">
          <input
            id="todo"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />
          <button type="submit">Add</button>
        </div>
      </form>
      {todos.length === 0 ? (
        <p>No todos yet.</p>
      ) : (
        <ul>
          {todos.map((todo) => (
            <li key={todo.id}>
              <label>
                <input
                  type="checkbox"
                  checked={todo.done}
                  onChange={() =>
                    setTodos((current) =>
                      current.map((item) =>
                        item.id === todo.id ? { ...item, done: !item.done } : item,
                      ),
                    )
                  }
                />{" "}
                {todo.title}
              </label>
              <button
                onClick={() => {
                  setTodos((current) =>
                    current.filter((item) => item.id !== todo.id),
                  );
                }}
              >
                Remove {todo.title}
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function useDebouncedValue<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timeoutId = window.setTimeout(() => setDebouncedValue(value), delay);
    return () => window.clearTimeout(timeoutId);
  }, [value, delay]);

  return debouncedValue;
}

function DebouncedSearch() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebouncedValue(query, 500);

  return (
    <section>
      <h2>3. Debounced value hook</h2>
      <p>Type quickly. The request value waits for 500 ms of inactivity.</p>
      <label htmlFor="search">Search</label>
      <input
        id="search"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
      />
      <p aria-live="polite">Request value: {debouncedQuery || "None"}</p>
    </section>
  );
}

export default function App() {
  return (
    <main>
      <h1>React interview examples</h1>
      <Counter />
      <TodoList />
      <DebouncedSearch />
    </main>
  );
}
