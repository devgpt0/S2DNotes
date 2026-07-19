# 04 - Async Thunks and Listener Middleware

## Reducers Cannot Perform Async Work

A reducer must remain synchronous and side-effect free. Network calls belong in thunks, RTK Query, listener middleware, or an external service layer.

## `createAsyncThunk`

Use a thunk for a request tied to a client workflow when RTK Query is not the better server-cache owner.

```typescript
import { createAsyncThunk } from "@reduxjs/toolkit";

export const saveCourse = createAsyncThunk<
  Course,
  CourseInput,
  { rejectValue: string }
>(
  "courses/saveCourse",
  async (input, { rejectWithValue, signal }) => {
    const response = await fetch("/api/courses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
      signal,
    });

    if (!response.ok) {
      return rejectWithValue(`save failed: HTTP ${response.status}`);
    }
    return parseCourse(await response.json());
  },
);
```

- first type: fulfilled value
- second: dispatch argument
- `rejectValue`: expected rejection payload
- `signal`: cancellation signal connected to the thunk promise

## Async State

```typescript
type SaveState =
  | { status: "idle" }
  | { status: "pending"; requestId: string }
  | { status: "error"; message: string };
```

Model states explicitly instead of combining unrelated booleans.

## Handle Lifecycle Actions

```typescript
extraReducers: (builder) => {
  builder
    .addCase(saveCourse.pending, (state, action) => {
      state.save = { status: "pending", requestId: action.meta.requestId };
    })
    .addCase(saveCourse.fulfilled, (state, action) => {
      state.items.push(action.payload);
      state.save = { status: "idle" };
    })
    .addCase(saveCourse.rejected, (state, action) => {
      if (action.meta.aborted) {
        state.save = { status: "idle" };
        return;
      }
      state.save = {
        status: "error",
        message: action.payload ?? "Course could not be saved",
      };
    });
}
```

## Component Dispatch and Unwrap

```tsx
const dispatch = useAppDispatch();

const submit = async (input: CourseInput): Promise<void> => {
  try {
    const course = await dispatch(saveCourse(input)).unwrap();
    console.log(course.id);
  } catch (error: unknown) {
    console.log(typeof error === "string" ? error : "Save failed");
  }
};
```

`.unwrap()` returns the fulfilled payload or throws the rejected payload/error. Catch only where the component can provide meaningful UX.

## Cancellation

```typescript
const promise = dispatch(saveCourse(input));
promise.abort();
```

Aborting the client wait does not guarantee server rollback. Design idempotency and server transaction behavior separately.

## Prevent Duplicate Work

`condition` can skip dispatch before the payload creator runs:

```typescript
export const loadCourse = createAsyncThunk<Course, string, { state: RootState }>(
  "courses/loadCourse",
  async (id, { signal }) => fetchCourse(id, signal),
  {
    condition: (id, { getState }) => {
      return getState().courses.loadingById[id] !== true;
    },
  },
);
```

RTK Query already handles request deduplication and caching for ordinary server resources.

## Listener Middleware

Listener middleware reacts to actions and coordinates workflows without putting effects in reducers.

```typescript
import { createListenerMiddleware } from "@reduxjs/toolkit";
import type { AppDispatch, RootState } from "./store";

export const listenerMiddleware = createListenerMiddleware();
export const startAppListening = listenerMiddleware.startListening
  .withTypes<RootState, AppDispatch>();

startAppListening({
  actionCreator: sessionEnded,
  effect: (_action, listenerApi) => {
    listenerApi.cancelActiveListeners();
    listenerApi.dispatch(coursesCleared());
    sessionStorage.removeItem("course-draft");
  },
});
```

`removeItem` is synchronous. The listener does not pretend it returns a promise.

## Good Listener Use Cases

- cancel work after logout/navigation
- react to one action with another feature workflow
- debounce autosave
- coordinate WebSocket messages
- start/stop long-lived subscriptions
- record safe analytics after a domain event

## Listener Cancellation

Listener APIs support delay, pause, condition, fork, cancellation, and taking future actions. Treat every long-running listener as an owned process with a clear stop condition.

## Thunk vs Listener vs RTK Query

| Need | Tool |
|---|---|
| imperative workflow requested by UI | thunk |
| react to actions/state changes | listener middleware |
| fetch/cache server resources | RTK Query |
| pure state transition | reducer |

## Final Rules

- reducers stay pure
- validate response data
- track pending/error/cancelled states explicitly
- bound retries and require safe semantics
- use RTK Query for ordinary server caching
- listeners own cleanup and cancellation
- do not duplicate one request lifecycle across several state systems
