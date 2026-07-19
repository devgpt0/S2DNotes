# 01 - State Management and the Redux Mental Model

## What Is State?

State is information that can change and affects application behavior or rendering.

Examples:

- selected course ID
- open/closed panel
- shopping-cart items
- authenticated user summary
- draft form values
- request status

## Start with Local State

```tsx
const Counter = () => {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount((value) => value + 1)}>{count}</button>;
};
```

This state belongs to one component. Redux would add no value.

## When Shared State Becomes Difficult

Problems appear when:

- distant features read and update the same state
- transitions follow important business rules
- many events must be debugged in order
- workflows react to actions from several features
- state must be inspected, replayed, or tested independently

Redux gives one explicit event flow.

## One-Way Data Flow

```text
UI/user/system event
  -> dispatch action
  -> reducer calculates next state
  -> store publishes next state
  -> selector reads needed data
  -> UI renders
```

## Action

An action is a plain event description:

```typescript
const action = {
  type: "courses/courseSelected",
  payload: "typescript",
};
console.log(action.type, action.payload);
// Console output: courses/courseSelected typescript
```

Actions should describe what happened, not hide arbitrary executable work.

## Reducer

A reducer receives current state and an action, then returns next state:

```typescript
type State = Readonly<{ selectedId: string | null }>;
type Action = Readonly<{ type: "selected"; id: string }>;

const reducer = (state: State, action: Action): State => {
  if (action.type === "selected") return { selectedId: action.id };
  return state;
};

console.log(reducer({ selectedId: null }, { type: "selected", id: "ts" }));
// Console output: { selectedId: "ts" }
```

Reducers must be deterministic and free from side effects. No network calls, random IDs, current time, DOM writes, or storage writes inside a reducer.

## Store

The store holds the current state, runs reducers after dispatch, and notifies subscribers.

```typescript
import { configureStore, createSlice } from "@reduxjs/toolkit";

const counterSlice = createSlice({
  name: "counter",
  initialState: { value: 0 },
  reducers: {
    increment(state) {
      state.value += 1;
    },
  },
});

const store = configureStore({ reducer: { counter: counterSlice.reducer } });
store.subscribe(() => console.log(store.getState().counter.value));
store.dispatch(counterSlice.actions.increment());
// Console output: 1
```

Redux Toolkit uses Immer so the reducer callback can use mutation-like syntax while producing an immutable next state.

## Selector

A selector reads a value from store state:

```typescript
type RootState = ReturnType<typeof store.getState>;
const selectCount = (state: RootState): number => state.counter.value;
console.log(selectCount(store.getState()));
// Console output: 1
```

Components should select the smallest value they need.

## State Ownership Categories

| State | Best starting owner |
|---|---|
| one component's input draft | local React state |
| shareable filters/page | URL |
| remote API resource/cache | RTK Query or another query cache |
| complex shared client workflow | Redux slice |
| durable offline database | IndexedDB/OPFS plus sync design |
| authentication authority | trusted server/session |

Redux memory state is not durable storage and not a security boundary.

## What Should Not Go in Redux by Default?

- every input keystroke
- derived totals that selectors can calculate
- non-serializable DOM nodes
- class instances, promises, controllers, sockets
- server data duplicated beside RTK Query cache
- values owned by the URL
- secrets

## Serializability

Serializable actions/state improve DevTools, persistence, replay, and debugging.

Store plain objects, arrays, strings, numbers, booleans, and null where practical. Convert Date to a deliberate string/number representation at the boundary.

## Quick Decision Example

Course filters that must survive refresh and be shareable belong in URL search parameters. A multi-step unsaved course editor used across routes may justify a Redux slice. The saved course list from an API usually belongs in RTK Query cache.

## Final Rule

Redux coordinates shared state transitions. It should not become a dumping ground for every value in the application.
