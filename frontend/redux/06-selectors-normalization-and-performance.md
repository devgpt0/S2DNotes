# 06 - Selectors, Normalization, and Performance

## Selectors Are Read Functions

```typescript
const selectCoursesState = (state: RootState) => state.courses;
const selectCourses = (state: RootState) => selectCoursesState(state).items;
const selectPlannedCourses = (state: RootState) => {
  return selectCourses(state).filter((course) => course.planned);
};
```

A selector should be pure. Do not fetch, mutate, log operational events, or write storage inside it.

## Why Fresh References Matter

This selector returns a new array on every call. In `useSelector`, that can rerender a component even when relevant input did not change.

Use memoization when the calculation returns a new reference and is reused in a render-sensitive path.

## `createSelector`

```typescript
import { createSelector } from "@reduxjs/toolkit";

const selectPlannedCourses = createSelector(
  [selectCourses],
  (courses) => courses.filter((course) => course.planned),
);
```

It recalculates only when an input selector result changes by identity.

Memoization is not for correctness. Profile before adding many selector layers.

## Selectors with Props

```typescript
const selectCourseById = (state: RootState, id: string): Course | undefined => {
  return state.courses.items.find((course) => course.id === id);
};

const course = useAppSelector((state) => selectCourseById(state, id));
```

For an expensive prop-based selector used by many component instances, create a selector factory so each instance has an appropriate memoization cache.

## Normalized State

Normalized state stores entities by ID and a separate order list:

```typescript
type NormalizedCourses = {
  ids: string[];
  entities: Record<string, Course | undefined>;
};
```

Benefits:

- one canonical object per ID
- direct lookup
- simpler updates
- relationships store IDs rather than nested copies

Do not normalize tiny, never-updated lists merely as a ritual.

## `createEntityAdapter`

```typescript
import { createEntityAdapter, createSlice } from "@reduxjs/toolkit";

const coursesAdapter = createEntityAdapter<Course>({
  sortComparer: (left, right) => left.title.localeCompare(right.title),
});

const coursesSlice = createSlice({
  name: "courses",
  initialState: coursesAdapter.getInitialState({ selectedId: null as string | null }),
  reducers: {
    coursesReceived: coursesAdapter.setAll,
    courseAdded: coursesAdapter.addOne,
    courseUpdated: coursesAdapter.updateOne,
    courseRemoved: coursesAdapter.removeOne,
  },
});
```

Adapter reducers use standard payload shapes. Read their contracts rather than guessing.

## Adapter Selectors

```typescript
const adapterSelectors = coursesAdapter.getSelectors<RootState>(
  (state) => state.courses,
);

export const {
  selectAll: selectAllCourses,
  selectById: selectCourseById,
  selectIds: selectCourseIds,
  selectTotal: selectCourseCount,
} = adapterSelectors;
```

## Store IDs for Relationships

```typescript
type Enrollment = Readonly<{
  learnerId: string;
  courseId: string;
}>;
```

Do not nest full learner and course copies in every enrollment. Join through selectors when rendering.

## Derived Data

Do not store values that can be calculated from canonical state:

- filtered lists
- totals
- selected object when selected ID exists
- booleans such as `hasCourses`
- sorted views unless ordering is itself user-managed state

## Rendering Performance

Fix in this order:

1. keep state in the correct owner
2. select only needed values
3. normalize large frequently updated entity collections
4. avoid selectors that create fresh objects unnecessarily
5. memoize measured derived work
6. split large components and virtualize measured large lists

Do not use `React.memo` and `createSelector` everywhere without evidence.

## Selector Stability Check

```typescript
const first = selectPlannedCourses(store.getState());
const second = selectPlannedCourses(store.getState());
console.log(first === second);
// Output: true for a memoized selector with unchanged input identity.
```

## Cache Size

Memoized selectors have cache policies. A selector called with many different arguments may need per-instance selectors or a bounded memoization strategy. An unbounded cache is a memory policy, not a free optimization.

## Final Rules

- selectors are pure reads
- normalized entities have one canonical owner
- relationships store IDs
- derived data stays derived
- memoization follows measured reference/calculation cost
- selector caches need appropriate scope and bounds
