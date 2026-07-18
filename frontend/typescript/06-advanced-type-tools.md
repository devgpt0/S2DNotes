# 06 - Advanced TypeScript Type Tools

Use advanced types to model real relationships, not to create puzzles.

## `keyof` and Indexed Access

```typescript
type User = { id: string; active: boolean };
type UserKey = keyof User;       // "id" | "active"
type Id = User["id"];           // string
const key: UserKey = "active";
console.log(key);
// Console output: active
```

## Utility Types

- `Partial<T>`: all properties optional
- `Required<T>`: all required
- `Readonly<T>`: readonly at one type level
- `Pick<T, K>` / `Omit<T, K>`: select/remove properties
- `Record<K, V>`: key/value object shape
- `Exclude`, `Extract`, `NonNullable`
- `Parameters`, `ReturnType`, `Awaited`

```typescript
type Course = { id: string; title: string; internalNotes: string };
type PublicCourse = Omit<Course, "internalNotes">;
const course: PublicCourse = { id: "html", title: "HTML" };
console.log(course.title);
// Console output: HTML
```

## Mapped Type

```typescript
type Flags<T> = { [Key in keyof T]: boolean };
type CourseFlags = Flags<{ published: string; featured: number }>;
const flags: CourseFlags = { published: true, featured: false };
console.log(flags);
// Console output: {published: true, featured: false}
```

## Conditional Type

```typescript
type ElementOf<T> = T extends readonly (infer Item)[] ? Item : T;
type Value = ElementOf<string[]>; // string
const value: Value = "HTML";
console.log(value);
// Console output: HTML
```

Conditional types distribute over naked union type parameters. Wrap each side in a tuple when non-distributive behavior is required.

## Template Literal Type

```typescript
type EventName = `course:${"created" | "deleted"}`;
const event: EventName = "course:created";
console.log(event);
// Console output: course:created
```

## `satisfies`

```typescript
const routes = {
  home: "/",
  courses: "/courses",
} satisfies Record<string, `/${string}`>;
console.log(routes.courses);
// Console output: /courses
```

`satisfies` checks compatibility while preserving the expression's useful inferred type.
