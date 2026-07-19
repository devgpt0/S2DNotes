# 05 - RTK Query for Server State

## Client State vs Server State

Client state is owned by the browser workflow: selected tab, unsaved wizard, local preferences.

Server state is a cached view of data owned elsewhere: courses, users, orders.

Server state needs fetching, deduplication, cache lifetime, refetching, invalidation, and request status. RTK Query provides those behaviors.

## Create an API Slice

```typescript
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export type Course = Readonly<{ id: string; title: string }>;
export type CreateCourse = Readonly<{ title: string }>;

export const coursesApi = createApi({
  reducerPath: "coursesApi",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  tagTypes: ["Course"],
  endpoints: (builder) => ({
    getCourses: builder.query<readonly Course[], void>({
      query: () => "/courses",
      providesTags: (result) => result === undefined
        ? [{ type: "Course", id: "LIST" }]
        : [
            { type: "Course", id: "LIST" },
            ...result.map((course) => ({ type: "Course" as const, id: course.id })),
          ],
    }),
    createCourse: builder.mutation<Course, CreateCourse>({
      query: (body) => ({
        url: "/courses",
        method: "POST",
        body,
      }),
      invalidatesTags: [{ type: "Course", id: "LIST" }],
    }),
  }),
});

export const { useCreateCourseMutation, useGetCoursesQuery } = coursesApi;
```

## Add API Reducer and Middleware

```typescript
export const store = configureStore({
  reducer: {
    [coursesApi.reducerPath]: coursesApi.reducer,
  },
  middleware: (getDefaultMiddleware) => {
    return getDefaultMiddleware().concat(coursesApi.middleware);
  },
});
```

Without the middleware, cache lifetimes, polling, invalidation, and subscriptions do not work correctly.

## Query in a Component

```tsx
const CourseList = () => {
  const { data, error, isLoading, isFetching, refetch } = useGetCoursesQuery();

  if (isLoading) return <p>Loading courses…</p>;
  if (error) return <button onClick={refetch}>Retry loading courses</button>;
  if (data === undefined || data.length === 0) return <p>No courses found.</p>;

  return <>
    {isFetching && <p role="status">Refreshing…</p>}
    <ul>{data.map((course) => <li key={course.id}>{course.title}</li>)}</ul>
  </>;
};
```

- `isLoading`: no data yet
- `isFetching`: request in flight, possibly with cached data already shown

Do not replace useful cached content with a full loading screen during background refresh.

## Mutation

```tsx
const CreateCourseButton = () => {
  const [createCourse, { isLoading, error }] = useCreateCourseMutation();

  const submit = async (): Promise<void> => {
    try {
      const created = await createCourse({ title: "TypeScript" }).unwrap();
      console.log(created.id);
    } catch {
      // Render the safe error state below; unexpected detail belongs in monitoring.
    }
  };

  return <>
    <button type="button" disabled={isLoading} onClick={() => void submit()}>
      {isLoading ? "Saving…" : "Create course"}
    </button>
    {error && <p role="alert">Course could not be created.</p>}
  </>;
};
```

Server validation remains required. Client types do not validate the response body.

## Runtime Response Validation

`fetchBaseQuery` supports response transformation:

```typescript
getCourses: builder.query<readonly Course[], void>({
  query: () => "/courses",
  transformResponse: (response: unknown) => parseCourses(response),
}),
```

Use strict parsers or schemas at the boundary.

## Cache Keys

Query endpoint plus serialized argument identifies a cache entry.

```typescript
useGetCourseQuery("course-1");
```

Ensure arguments contain stable serializable request identity. Do not pass DOM nodes, functions, or changing objects.

## Tags and Invalidation

Tags connect mutations to cached data that may now be stale.

Use list tags for collection membership changes and entity tags for one item. Avoid invalidating every endpoint after every mutation.

## Optimistic Updates

```typescript
onQueryStarted: async ({ id, title }, { dispatch, queryFulfilled }) => {
  const patch = dispatch(
    coursesApi.util.updateQueryData("getCourses", undefined, (draft) => {
      const course = draft.find((item) => item.id === id);
      if (course === undefined) throw new RangeError("course not found in cache");
      course.title = title;
    }),
  );

  try {
    await queryFulfilled;
  } catch {
    patch.undo();
  }
}
```

Optimistic UI needs rollback, conflict policy, accessible feedback, and server identity rules. Prefer invalidation/refetch when optimistic complexity is not justified.

## Polling and Refetch Options

RTK Query can refetch on focus/reconnect and poll at an interval. Enable only for product requirements; polling consumes network and server capacity.

## Streaming Updates

`onCacheEntryAdded` can connect WebSocket/SSE updates to a cache entry. The lifecycle must await cache creation, validate every message, update cached data, and close the connection after cache removal.

## Do Not Copy Query Data into a Slice

```typescript
// Avoid: dispatch(coursesReceived(query.data));
```

That creates two owners and synchronization bugs. Select from RTK Query cache unless a distinct client workflow needs a deliberate snapshot.

## Final Rules

- RTK Query owns ordinary API resource cache
- validate runtime responses
- distinguish initial loading from refresh
- use precise tags
- do not duplicate cache data in slices
- optimistic changes need rollback/conflict design
- long-lived streams need cleanup
- authentication and authorization remain server responsibilities
