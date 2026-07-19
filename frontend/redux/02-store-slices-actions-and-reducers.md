# 02 - Store, Slices, Actions, and Reducers

## Install

```powershell
npm install @reduxjs/toolkit react-redux
```

## Define a State Model

```typescript
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
  items: [],
  selectedId: null,
};
```

State is mutable-looking inside Toolkit reducers but should be treated as readonly everywhere else.

## Create a Slice

```typescript
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

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
      state.selectedId = action.payload;
    },
  },
});

export const { courseAdded, courseSelected, courseToggled } = coursesSlice.actions;
export const coursesReducer = coursesSlice.reducer;
```

Reducer method syntax is used because these are named object methods in the slice configuration. Standalone helpers remain arrow variables.

## Why “Mutation” Is Safe Here

Immer gives the reducer a draft. Toolkit records draft changes and produces a new immutable result.

Do not both mutate the draft and return a different state from the same case.

Outside reducers, never mutate selected state:

```typescript
// Wrong outside a reducer: selectedCourse.planned = true;
```

## Prepare Callbacks

Create IDs and timestamps before reducer logic while keeping action creation testable:

```typescript
const preparedCoursesSlice = createSlice({
  name: "preparedCourses",
  initialState,
  reducers: {
    courseCreated: {
      reducer(state, action: PayloadAction<Course>) {
        state.items.push(action.payload);
      },
      prepare(title: string) {
        if (title.trim().length === 0) throw new TypeError("title is required");
        return {
          payload: {
            id: crypto.randomUUID(),
            title: title.trim(),
            planned: false,
          },
        };
      },
    },
  },
});
```

For deterministic tests, create IDs in a service/event handler and dispatch a complete value, or inject the ID source. Do not generate random values inside the reducer.

## Configure the Store

```typescript
import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: {
    courses: coursesReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

Toolkit adds safe default middleware for thunk support, development checks, and serializability checks.

## Selectors

```typescript
export const selectCourses = (state: RootState): readonly Course[] => {
  return state.courses.items;
};

export const selectSelectedCourse = (state: RootState): Course | undefined => {
  return state.courses.items.find(
    (course) => course.id === state.courses.selectedId,
  );
};
```

Do not store the complete selected object if its ID can identify the canonical item.

## Action Output

```typescript
console.log(courseSelected("ts"));
// Console output:
// { type: "courses/courseSelected", payload: "ts" }
```

## Extra Reducers

A slice owns its state but may react to actions defined elsewhere:

```typescript
const sessionEnded = createAction("session/ended");

const slice = createSlice({
  name: "courses",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(sessionEnded, () => initialState);
  },
});
```

Use cross-feature reactions sparingly. Listener middleware may express a workflow more clearly than making many slices respond implicitly.

## Final Rules

- one slice owns one cohesive state area
- reducers calculate next state only
- actions describe events
- selectors read and derive state
- state/actions remain serializable
- invalid transitions fail explicitly
- derived data is not duplicated in state
