# 11 - Narrowing, Type Guards, and Runtime Trust

## Why Narrowing Exists

A union or `unknown` value can have several possible runtime shapes. Narrowing proves which shape is present before code uses type-specific operations.

```typescript
const format = (value: string | number): string => {
  if (typeof value === "number") {
    return value.toFixed(2);
  }
  return value.toUpperCase();
};

console.log(format(5), format("typescript"));
// Console output: 5.00 TYPESCRIPT
```

Inside the first branch, TypeScript knows `value` is a number. In the remaining branch, it is a string.

## Control-Flow Analysis

TypeScript follows assignments, conditions, returns, and throws:

```typescript
const requireName = (name: string | undefined): string => {
  if (name === undefined) {
    throw new TypeError("name is required");
  }
  return name.toUpperCase();
};
```

After the throw, only `string` remains.

## `typeof`

Use for JavaScript primitive categories:

```typescript
const describe = (value: unknown): string => {
  switch (typeof value) {
    case "string": return `text:${value}`;
    case "number": return Number.isFinite(value) ? `number:${value}` : "non-finite number";
    case "boolean": return `boolean:${value}`;
    case "undefined": return "missing";
    default: return "object, function, bigint, or symbol";
  }
};
console.log(describe(true));
// Console output: boolean:true
```

Remember: `typeof null` is historically `"object"`, so check `value !== null`.

## Equality Narrowing

```typescript
const label = (value: string | null | undefined): string => {
  if (value === null) return "explicitly empty";
  if (value === undefined) return "missing";
  return value;
};
```

Prefer strict equality so the exact runtime case is visible.

## Truthiness Narrowing

```typescript
const unsafeLabel = (value: string | undefined): string => {
  if (!value) return "missing";
  return value;
};
```

This treats an empty string as missing. Use an explicit `value === undefined` check when empty text is valid.

## `in` Operator

```typescript
type EmailMessage = { email: string };
type SmsMessage = { phone: string };

const destination = (message: EmailMessage | SmsMessage): string => {
  return "email" in message ? message.email : message.phone;
};
console.log(destination({ email: "learn@example.com" }));
// Console output: learn@example.com
```

The `in` operator checks property existence, including inherited properties. Runtime boundary parsers should usually require plain expected objects and validate every relevant field.

## `instanceof`

```typescript
const errorMessage = (error: unknown): string => {
  return error instanceof Error ? error.message : "Unknown failure";
};
console.log(errorMessage(new Error("Network unavailable")));
// Console output: Network unavailable
```

`instanceof` uses runtime constructor/prototype identity. It may fail across realms such as different windows and does not validate plain JSON.

## Discriminated Unions

Give every member one common literal property:

```typescript
type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: string };

const resultMessage = (result: Result<number>): string => {
  return result.ok ? `Value: ${result.value}` : `Error: ${result.error}`;
};
console.log(resultMessage({ ok: true, value: 42 }));
// Console output: Value: 42
```

This is safer than optional `value?` and `error?` fields that permit impossible combinations.

## User-Defined Type Predicates

A predicate returns a boolean and tells TypeScript what success proves:

```typescript
type Course = Readonly<{ id: string; title: string }>;

const isCourse = (value: unknown): value is Course => {
  return typeof value === "object"
    && value !== null
    && "id" in value
    && typeof value.id === "string"
    && value.id.length > 0
    && "title" in value
    && typeof value.title === "string"
    && value.title.length > 0;
};

const value: unknown = { id: "ts", title: "TypeScript" };
if (isCourse(value)) {
  console.log(value.title);
}
// Console output: TypeScript
```

A wrong predicate can lie to the compiler. Test its accepted and rejected cases.

## Assertion Functions

An assertion function throws on failure and narrows after it returns:

```typescript
const assertCourse = (value: unknown): asserts value is Course => {
  if (!isCourse(value)) throw new TypeError("invalid course");
};

const parsed: unknown = JSON.parse('{"id":"ts","title":"TypeScript"}');
assertCourse(parsed);
console.log(parsed.id);
// Console output: ts
```

Use assertions when failure must stop the current operation. Use a result-returning parser when callers need to display or combine expected validation errors.

## Parse, Do Not Merely Check

A parser returns a trusted value and can reject extra or unsafe structure:

```typescript
const parseCourse = (value: unknown): Course => {
  if (!isCourse(value)) throw new TypeError("invalid course");
  return { id: value.id, title: value.title };
};
```

Returning a new object establishes the exact trusted shape instead of passing an external object with unknown extra properties deeper into the application.

## Array Validation

```typescript
const parseCourses = (value: unknown): readonly Course[] => {
  if (!Array.isArray(value) || !value.every(isCourse)) {
    throw new TypeError("courses must be an array of valid courses");
  }
  return value.map((course) => ({ id: course.id, title: course.title }));
};
```

Checking only `Array.isArray` proves nothing about the elements.

## Exhaustive Checking

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

const area = (shape: Shape): number => {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rectangle": return shape.width * shape.height;
    default: return shape satisfies never;
  }
};
```

Adding a new shape creates a type error until the switch handles it.

## Narrowing Can Be Invalidated

Mutable values and callbacks can make assumptions stale. Prefer local immutable values:

```typescript
const title = course.title;
if (title !== undefined) {
  queueMicrotask(() => console.log(title.toUpperCase()));
}
```

This captures the already narrowed string rather than repeatedly reading mutable external state.

## Runtime Boundaries to Validate

- `JSON.parse`
- Fetch response bodies
- local/session storage
- IndexedDB records
- URL parameters
- form data
- `postMessage` and worker messages
- WebSocket/event payloads
- environment/configuration values
- third-party library callbacks with weak types

TypeScript does not make any of these trustworthy by annotation.

## Schema Libraries

A schema library is valuable when shapes are nested, reused, versioned, or need detailed errors. Keep strict behavior: avoid coercion and implicit defaulting unless the business rule explicitly requires transformation.

```typescript
import { z } from "zod";

const CourseSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
}).strict();

const course = CourseSchema.parse(externalValue);
```

## Beginner to Expert Checklist

- beginner: `typeof`, equality, null checks
- developer: discriminated unions, `in`, `instanceof`, predicates
- senior: parsers, assertion functions, exhaustive state modeling
- expert: control-flow invalidation, cross-realm behavior, schema versioning, trust boundaries

## Final Rule

Use compile-time types inside the trusted application. Use runtime validation whenever data crosses into that trusted area.
