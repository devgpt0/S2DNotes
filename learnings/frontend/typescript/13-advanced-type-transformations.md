# 13 - Mapped, Conditional, Template, and Recursive Types

Advanced types calculate new types from existing types. Use them when they remove repeated contracts and remain easier to understand than handwritten alternatives.

## `keyof`

```typescript
type Course = {
  id: string;
  title: string;
  lessons: number;
};

type CourseKey = keyof Course; // "id" | "title" | "lessons"
const key: CourseKey = "title";
console.log(key);
// Console output: title
```

For types with string index signatures, `keyof` can include `string` or `number`, not only visibly declared keys.

## Indexed Access Types

```typescript
type CourseTitle = Course["title"]; // string
type CourseValue = Course[keyof Course]; // string | number
```

`T[K]` means “the value type found at key `K` in `T`.”

## `typeof` in a Type Position

```typescript
const defaultCourse = {
  id: "ts",
  title: "TypeScript",
  lessons: 14,
};

type DefaultCourse = typeof defaultCourse;
```

This reuses the inferred type of a runtime declaration. It does not inspect a runtime value dynamically.

## Mapped Types

A mapped type loops over keys at compile time:

```typescript
type OptionalFields<T> = {
  [Key in keyof T]?: T[Key];
};

type CoursePatch = OptionalFields<Course>;
const patch: CoursePatch = { title: "Advanced TypeScript" };
console.log(patch.title);
// Console output: Advanced TypeScript
```

This resembles built-in `Partial<T>`.

## Add and Remove Modifiers

```typescript
type MutableRequired<T> = {
  -readonly [Key in keyof T]-?: T[Key];
};
```

- `-readonly`: remove readonly
- `-?`: remove optional
- `+readonly` or `+?`: add modifiers; `+` is usually omitted

Use modifier removal carefully. It can violate ownership assumptions if applied merely for convenience.

## Key Remapping

```typescript
type EventHandlers<T> = {
  [Key in keyof T as `on${Capitalize<string & Key>}`]: (value: T[Key]) => void;
};

type CourseEvents = EventHandlers<{
  titleChanged: string;
  lessonsChanged: number;
}>;
```

The resulting keys are `onTitleChanged` and `onLessonsChanged`.

## Filter Keys by Mapping to `never`

```typescript
type StringKeys<T> = {
  [Key in keyof T]: T[Key] extends string ? Key : never;
}[keyof T];

type CourseStringKey = StringKeys<Course>; // "id" | "title"
```

The mapped type creates a union of keys or `never`; indexed access collects the remaining keys.

## Conditional Types

```typescript
type ElementType<T> = T extends readonly (infer Item)[] ? Item : T;

type A = ElementType<string[]>; // string
type B = ElementType<number>; // number
```

Read it as: if `T` is an array, extract its item type; otherwise keep `T`.

## `infer`

`infer` names a type discovered while matching:

```typescript
type FunctionResult<T> = T extends (...arguments_: never[]) => infer Result
  ? Result
  : never;

const createCourse = () => ({ id: "ts", title: "TypeScript" });
type CreatedCourse = FunctionResult<typeof createCourse>;
```

Use built-in `ReturnType<T>` instead of recreating it in application code. The example explains how such utilities work.

## Distributive Conditional Types

A conditional type distributes across a union when the checked type is a naked type parameter:

```typescript
type ToArray<T> = T extends unknown ? T[] : never;
type Result = ToArray<string | number>; // string[] | number[]
```

Prevent distribution by wrapping both sides:

```typescript
type OneArray<T> = [T] extends [unknown] ? T[] : never;
type Combined = OneArray<string | number>; // (string | number)[]
```

This difference is important when building library-level utilities.

## Template Literal Types

```typescript
type Entity = "course" | "learner";
type Action = "created" | "deleted";
type EventName = `${Entity}:${Action}`;

const event: EventName = "course:created";
console.log(event);
// Console output: course:created
```

Template literal types are useful for finite naming contracts. Do not use them to pretend arbitrary external strings are validated.

## Built-In Utility Types

| Utility | Meaning |
|---|---|
| `Partial<T>` | every property optional |
| `Required<T>` | every property required |
| `Readonly<T>` | every property readonly |
| `Pick<T, K>` | keep selected keys |
| `Omit<T, K>` | remove selected keys |
| `Record<K, V>` | keys `K` map to values `V` |
| `Exclude<U, M>` | remove union members assignable to `M` |
| `Extract<U, M>` | keep union members assignable to `M` |
| `NonNullable<T>` | remove `null` and `undefined` |
| `Parameters<F>` | function parameter tuple |
| `ReturnType<F>` | function result type |
| `Awaited<T>` | recursively unwrap promise-like results |

Example:

```typescript
type CoursePreview = Pick<Course, "id" | "title">;
const preview: CoursePreview = { id: "ts", title: "TypeScript" };
console.log(preview);
// Console output: { id: "ts", title: "TypeScript" }
```

## `satisfies`

`satisfies` checks a value against a type while preserving useful inference:

```typescript
type RouteName = "home" | "courses";
const ROUTES = {
  home: "/",
  courses: "/courses",
} satisfies Record<RouteName, string>;

console.log(ROUTES.courses);
// Console output: /courses
```

Unlike a type assertion, `satisfies` checks compatibility. It still performs no runtime validation.

## `NoInfer<T>`

`NoInfer<T>` can stop one location from contributing to inference:

```typescript
const choose = <T>(options: readonly T[], fallback: NoInfer<T>): T => {
  return options[0] ?? fallback;
};

const choice = choose(["light", "dark"] as const, "light");
console.log(choice);
// Console output: light
// "system" would fail because options determine T.
```

Use it only when inference direction is part of a carefully designed API.

## Recursive Types

```typescript
type JsonValue =
  | null
  | boolean
  | number
  | string
  | JsonValue[]
  | { [key: string]: JsonValue };

const value: JsonValue = { course: "TypeScript", lessons: [1, 2] };
console.log(JSON.stringify(value));
// Console output: {"course":"TypeScript","lessons":[1,2]}
```

Recursive types model trees and nested formats. Deep generic recursion can slow the compiler or hit instantiation limits.

## Recursive Readonly Example

```typescript
type DeepReadonly<T> =
  T extends (...arguments_: never[]) => unknown ? T
  : T extends readonly (infer Item)[] ? readonly DeepReadonly<Item>[]
  : T extends object ? { readonly [Key in keyof T]: DeepReadonly<T[Key]> }
  : T;
```

This learning utility does not handle every built-in class exactly as a production library might. Prefer a proven utility when Date, Map, Set, branded types, tuples, and special objects matter.

## Avoid Type-Level Overengineering

Stop and simplify when:

- an explicit domain type is shorter
- error messages become unreadable
- callers need assertions
- compile time becomes material
- only one use exists
- runtime validation is still missing

Types should make application rules easier to see.

## Beginner to Expert Path

- beginner: `keyof`, indexed access, `Partial`, `Pick`, `Record`
- developer: mapped types, `satisfies`, template literals
- senior: conditional types, `infer`, key filtering
- expert: distributivity control, recursive limits, inference direction, public compatibility

## Final Rule

Create advanced type utilities only when they encode a repeated, stable relationship. Prefer a plain named type for one domain shape.
