# 07 - Context, Reducers, and State Ownership

## Context

Context supplies a value to descendants without passing it through every intermediate component.

```tsx
const ThemeContext = createContext<"light" | "dark" | null>(null);
function useTheme() {
  const theme = useContext(ThemeContext);
  if (theme === null) throw new Error("useTheme must be inside ThemeContext");
  return theme;
}
// Result: custom consumer fails clearly when provider is missing.
```

Use context for stable cross-cutting values such as theme, authenticated session interface, or feature service. Do not put every frequently changing field in one global context.

## Reducer

Reducer centralizes state transitions.

```tsx
type Task = { id: string; text: string; complete: boolean };
type Action = { type: "added"; task: Task } | { type: "toggled"; id: string } | { type: "removed"; id: string };
function tasksReducer(state: readonly Task[], action: Action): readonly Task[] {
  switch (action.type) {
    case "added": return [...state, action.task];
    case "toggled": return state.map(task => task.id === action.id ? { ...task, complete: !task.complete } : task);
    case "removed": return state.filter(task => task.id !== action.id);
    default: return action satisfies never;
  }
}
console.log(tasksReducer([], { type: "added", task: { id: "1", text: "Learn", complete: false } }).length);
// Console output: 1
```

Reducers must be pure and immutable.

## Context + Reducer

Separate state and dispatch contexts so components using only dispatch do not rerender from the state context value.

## State Ownership Decision

1. Can it be derived from props/state? Do not store it.
2. Used by one component? Keep local.
3. Shared by nearby siblings? Lift to closest common parent.
4. Deep stable cross-cutting value? Context may fit.
5. Remote server data? Use router/query cache rather than treating it as ordinary global client state.
6. URL-shareable state? Put it in URL/search params.

## External Stores

Use `useSyncExternalStore` for integration with stores outside React so concurrent rendering receives consistent snapshots.
