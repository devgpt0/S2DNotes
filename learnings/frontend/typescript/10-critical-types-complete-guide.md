# 10 - Critical TypeScript Types: Complete Beginner-to-Expert Guide

## The Main Rule

TypeScript types describe JavaScript values during development. They do not change runtime values and they disappear from emitted JavaScript.

```typescript
const course: string = "TypeScript";
console.log(typeof course);
// Console output: string
// The runtime sees a JavaScript string, not a TypeScript type object.
```

## Type Map

| Need | Type to start with |
|---|---|
| text | `string` |
| ordinary number | `number` |
| very large integer | `bigint` |
| true/false | `boolean` |
| unique symbol key | `symbol` |
| missing value | `undefined` |
| intentional empty value | `null` |
| list of one element type | `T[]` or `Array<T>` |
| fixed positions | tuple |
| known object shape | object type or interface |
| one of several types | union `A | B` |
| combined requirements | intersection `A & B` |
| external unchecked value | `unknown` |
| function returns nothing useful | `void` |
| state that cannot occur | `never` |

## Primitive Types

### `string`

```typescript
const title: string = "TypeScript Foundations";
const lessonCount = 12;
console.log(`${title}: ${lessonCount} lessons`);
// Console output: TypeScript Foundations: 12 lessons
```

Use lowercase `string`, not wrapper type `String`.

### `number`

```typescript
const price: number = 499.5;
const quantity: number = 2;
console.log(price * quantity);
// Console output: 999
```

`number` includes floating-point values, `NaN`, and infinities. A type alone cannot promise a positive, finite, safe integer.

```typescript
const requirePositiveInteger = (value: number): number => {
  if (!Number.isSafeInteger(value) || value <= 0) {
    throw new RangeError("value must be a positive safe integer");
  }
  return value;
};
```

### `bigint`

```typescript
const veryLargeCount: bigint = 9_007_199_254_740_993n;
console.log(veryLargeCount + 1n);
// Console output: 9007199254740994n
```

Do not mix `number` and `bigint` arithmetic. JSON does not serialize `bigint` without an explicit representation policy.

### `boolean`

```typescript
const published: boolean = false;
console.log(published ? "Visible" : "Draft");
// Console output: Draft
```

A boolean is good for one independent yes/no fact. Several related modes often need a literal union or discriminated union instead of multiple booleans.

### `symbol` and `unique symbol`

```typescript
const internalId: unique symbol = Symbol("internalId");
const course = { [internalId]: 42, title: "TypeScript" };
console.log(course.title, course[internalId]);
// Console output: TypeScript 42
```

Symbols create collision-resistant property keys. They are not private security boundaries.

## Literal Types

A literal type allows one exact value:

```typescript
type Theme = "light" | "dark" | "system";
const theme: Theme = "dark";
console.log(theme);
// Console output: dark
```

Literal unions are excellent for finite application states because invalid spellings fail at compile time.

## Type Inference and Widening

```typescript
const fixed = "draft"; // type is "draft"
let changing = "draft"; // type widens to string
changing = "published";
console.log(fixed, changing);
// Console output: draft published
```

`const` preserves a literal when the binding cannot change. Object properties remain mutable unless you ask for readonly literal inference:

```typescript
const config = {
  method: "GET",
  retries: 3,
} as const;
// config.method has type "GET" and is readonly.
```

`as const` changes compile-time mutability and literal inference. It does not freeze the object at runtime.

## `null` and `undefined`

With `strictNullChecks`, absence must be modeled explicitly:

```typescript
const findTitle = (id: string): string | undefined => {
  return id === "ts" ? "TypeScript" : undefined;
};

const title = findTitle("missing");
console.log(title ?? "Not found");
// Console output: Not found
```

- `undefined`: commonly missing, omitted, or not yet provided
- `null`: explicit empty value chosen by an API or domain

Use one consistent domain convention. Do not add both unless each has a different meaning.

## Arrays

```typescript
const titles: string[] = ["HTML", "CSS"];
const lengths: number[] = titles.map((title) => title.length);
console.log(lengths);
// Console output: [4, 3]
```

`string[]` and `Array<string>` mean the same array element type.

Use `readonly` when a function should not mutate the caller's array:

```typescript
const totalLength = (values: readonly string[]): number => {
  return values.reduce((total, value) => total + value.length, 0);
};

console.log(totalLength(["TS", "JavaScript"]));
// Console output: 12
```

Readonly is compile-time protection through that reference. It does not deep-freeze runtime data.

## Tuples

A tuple has known positions:

```typescript
type Coordinates = readonly [x: number, y: number];
const point: Coordinates = [10, 20];
const [x, y] = point;
console.log(x, y);
// Console output: 10 20
```

Use tuples when positions have stable meaning. Use an object when named fields are clearer or the shape will evolve.

Optional and rest tuple elements are possible:

```typescript
type LogEntry = readonly [message: string, code?: number];
type Path = readonly [first: string, ...remaining: string[]];
```

## Object Types

```typescript
type Course = {
  readonly id: string;
  title: string;
  description?: string;
};

const course: Course = { id: "ts", title: "TypeScript" };
course.title = "Advanced TypeScript";
console.log(course.title);
// Console output: Advanced TypeScript
// course.id cannot be assigned through this type.
```

An optional property means the property may be absent. With `exactOptionalPropertyTypes`, absent and explicitly `undefined` are not automatically treated as identical.

## `object`, `{}`, and `Object`

These are commonly misunderstood:

- `object`: any non-primitive value
- `{}`: any non-nullish value, including numbers and strings
- `Object`: broad boxed-object interface; rarely the right application type

Prefer a precise property type or `Record<PropertyKey, unknown>` for a dictionary-like object.

```typescript
const printKeys = (value: object): void => {
  console.log(Object.keys(value));
};
printKeys({ title: "TypeScript" });
// Console output: ["title"]
```

## Index Signatures and `Record`

```typescript
type ScoreByLearner = Record<string, number>;
const scores: ScoreByLearner = { Asha: 90, Ravi: 85 };
console.log(scores.Asha);
// Console output: 90
```

With `noUncheckedIndexedAccess`, an unknown key returns `number | undefined`:

```typescript
const score = scores["Unknown"];
console.log(score ?? "No score");
// Console output: No score
```

Use `Map` when keys are not only strings/symbols, insertion order and size APIs matter, or entries change frequently.

## Function Types

```typescript
type Formatter = (value: number) => string;
const formatPrice: Formatter = (value) => `₹${value.toFixed(2)}`;
console.log(formatPrice(499));
// Console output: ₹499.00
```

Function types can describe properties and callbacks:

```typescript
type CourseActions = {
  save: (title: string) => Promise<void>;
  remove: (id: string) => void;
};
```

## `void`

`void` means the caller should not use a return value:

```typescript
const announce = (message: string): void => {
  console.log(message);
};
announce("Saved");
// Console output: Saved
```

A callback typed to return `void` may accept a function that returns something, but that result is ignored. `void` does not mean the runtime function is forbidden from returning.

## `never`

`never` represents a value that cannot occur.

```typescript
const fail = (message: string): never => {
  throw new Error(message);
};
```

It is also used for exhaustive checks:

```typescript
type Status = "draft" | "published";
const statusLabel = (status: Status): string => {
  switch (status) {
    case "draft": return "Draft";
    case "published": return "Published";
    default: return status satisfies never;
  }
};

console.log(statusLabel("published"));
// Console output: Published
```

## `unknown`

`unknown` means a value exists but its type is not yet trusted.

```typescript
const printValue = (value: unknown): void => {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
    return;
  }
  console.log("Not a string");
};

printValue("typescript");
// Console output: TYPESCRIPT
```

Use `unknown` for parsed JSON, caught errors, message payloads, and other external data.

## `any`

`any` turns off useful checking and spreads through expressions:

```typescript
let unsafe: any = "text";
unsafe.missing.deep.call(); // TypeScript allows this; runtime fails.
```

Avoid `any` in application code. At an unavoidable legacy boundary, keep it local, convert to `unknown`, validate, and return a trusted type.

## Union Types

```typescript
const formatId = (id: string | number): string => {
  return typeof id === "number" ? id.toString(10) : id.toUpperCase();
};
console.log(formatId(42), formatId("course"));
// Console output: 42 COURSE
```

A union means the value is one member at runtime. You may use only operations safe for the currently narrowed member.

## Intersection Types

```typescript
type Identified = { id: string };
type Timestamped = { createdAt: Date };
type Entity = Identified & Timestamped;

const entity: Entity = { id: "course-1", createdAt: new Date("2026-01-01T00:00:00Z") };
console.log(entity.id, entity.createdAt.getUTCFullYear());
// Console output: course-1 2026
```

An intersection must satisfy every member. Intersecting incompatible properties can produce `never`, so do not use intersections as arbitrary “merge” tools.

## Discriminated Unions

```typescript
type LoadState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; courses: readonly Course[] }
  | { status: "error"; message: string };
```

Each state carries only the data valid for that state. This prevents impossible combinations such as `loading: true` together with a success value and error message.

## Enums vs Literal Unions

Literal unions create no extra runtime object:

```typescript
const ROLES = ["admin", "learner"] as const;
type Role = (typeof ROLES)[number];
```

String enums create a runtime object:

```typescript
enum RoleEnum {
  Admin = "admin",
  Learner = "learner",
}
console.log(RoleEnum.Admin);
// Console output: admin
```

Prefer literal unions for most application state. Use an enum when its runtime namespace and interoperability are deliberate requirements. Avoid numeric enums for external data because unexpected numbers can be confusing and protocol contracts deserve explicit validation.

## Built-In Generic Types

```typescript
const createdAt: Date = new Date("2026-07-19T00:00:00Z");
const scores: Map<string, number> = new Map([["Asha", 90]]);
const tags: Set<string> = new Set(["typescript"]);
const titlePromise: Promise<string> = Promise.resolve("TypeScript");

console.log(createdAt.getUTCFullYear(), scores.get("Asha"), tags.has("typescript"), await titlePromise);
// Module console output: 2026 90 true TypeScript
```

Types describe API values, but serialization changes them. JSON turns `Date` into text and does not directly preserve Map, Set, or bigint.

## `readonly`, `Readonly<T>`, and Deep Mutability

```typescript
type Settings = Readonly<{
  theme: "light" | "dark";
  shortcuts: string[];
}>;
```

The top-level properties cannot be reassigned, but `shortcuts` is still a mutable array. Use `readonly string[]` when nested mutation should also be prevented through the type.

Readonly is an ownership tool, not runtime freezing and not automatically recursive.

## Type Aliases vs Interfaces

Both can describe object shapes:

```typescript
interface Learner {
  readonly id: string;
  name: string;
}

type CourseId = string;
type Enrollment = { learnerId: string; courseId: CourseId };
```

Use an interface when declaration merging or an extendable object contract is intentional. Use a type alias for unions, intersections, primitives, tuples, mapped types, and closed domain shapes. Consistency matters more than ideology.

## Type Assertions

```typescript
const value: unknown = { id: 42 };
// const course = value as Course; // changes compiler belief, performs no validation.
```

An assertion is not conversion and not validation. Prefer narrowing, a parser, or a schema library at runtime boundaries.

## Beginner to Expert Checklist

- beginner: primitives, arrays, objects, function types
- developer: unions, literals, nullability, readonly, unknown
- senior: discriminated unions, precise dictionaries, serialization contracts
- expert: inference/widening, impossible intersections, declaration merging, variance, and public API compatibility

## Final Decision Rule

Choose the smallest type that represents every valid value and excludes invalid states. Then validate external runtime data before allowing it into that trusted type.
