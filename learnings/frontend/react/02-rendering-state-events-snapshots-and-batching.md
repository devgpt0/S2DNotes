# 02 - Rendering, State, Events, Snapshots, and Batching

## State

State is component memory that requests a new render when updated.

```tsx
function LikeButton() {
  const [liked, setLiked] = useState(false);
  return <button aria-pressed={liked} onClick={() => setLiked(value => !value)}>{liked ? "Liked" : "Like"}</button>;
}
// Browser result: activation toggles label and aria-pressed state.
```

## State Is a Snapshot

Each render sees fixed state values. Calling a setter schedules a later render; it does not change the variable in the current handler.

```tsx
function Counter() {
  const [count, setCount] = useState(0);
  function incrementThree() {
    setCount(value => value + 1);
    setCount(value => value + 1);
    setCount(value => value + 1);
  }
  return <button onClick={incrementThree}>{count}</button>;
}
// Browser result: each activation increases count by 3 because functional updates consume queued values.
```

Using `setCount(count + 1)` three times usually queues the same snapshot value.

## Batching

React batches state updates during an event to avoid unnecessary intermediate renders. Do not depend on immediate DOM updates after a setter.

## Events

```tsx
function Search() {
  const [query, setQuery] = useState("");
  return <label>Search <input value={query} onChange={event => setQuery(event.currentTarget.value)} /></label>;
}
// Browser result: input value stays synchronized with query state.
```

Pass a function: `onClick={handleClick}`. `onClick={handleClick()}` calls it during rendering.

## Immutable State Update

```tsx
type Task = { id: string; text: string; complete: boolean };
const [tasks, setTasks] = useState<readonly Task[]>([]);
const toggle = (id: string) => setTasks(items => items.map(item => item.id === id ? { ...item, complete: !item.complete } : item));
// Result: a new array and changed task object allow React and memoized children to observe identity changes.
```

## State Placement

Keep state in the closest common owner that needs to coordinate it. Do not duplicate the same source of truth in child and parent. Derive totals/filtered arrays during render when cheap instead of storing them as synchronized state.

## Render and Commit

Render must remain pure and can be restarted. Commit changes the DOM and runs layout/passive synchronization at the appropriate phase.
