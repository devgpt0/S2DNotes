# TypeScript Concepts in Simple Words

Read this after JavaScript fundamentals and before the detailed TypeScript chapters.

## What TypeScript Adds

TypeScript checks relationships in your source code before the browser runs it.

```typescript
const title: string = "TypeScript";
const lessons: number = 14;
console.log(`${title}: ${lessons}`);
// Output: TypeScript: 14
```

This invalid assignment fails during type checking:

```typescript
// const lessons: number = "fourteen";
```

## The Browser Still Runs JavaScript

Types disappear from emitted code.

TypeScript:

```typescript
const doubleNumber = (value: number): number => value * 2;
```

JavaScript output:

```javascript
const doubleNumber = (value) => value * 2;
```

Types improve development confidence. They do not exist as runtime validators.

## Inference

TypeScript often understands a type without an annotation:

```typescript
const course = "TypeScript"; // inferred string literal
const lessons = 14;          // inferred number literal
```

Annotate public boundaries, parameters, return contracts, and places where the intended type is wider or clearer than the initial value.

## Function Types

```typescript
const calculateTotal = (price: number, quantity: number): number => {
  return price * quantity;
};
console.log(calculateTotal(499, 2));
// Output: 998
```

TypeScript checks both arguments and the result.

## Object Types

```typescript
type Course = Readonly<{
  id: string;
  title: string;
  lessons: number;
}>;

const course: Course = {
  id: "ts",
  title: "TypeScript",
  lessons: 14,
};
console.log(course.title);
// Output: TypeScript
```

The type says which properties exist and what values they contain.

## Union Types

A union allows one of several types:

```typescript
const formatId = (id: string | number): string => {
  return typeof id === "number" ? id.toString(10) : id.toUpperCase();
};
console.log(formatId("course"), formatId(42));
// Output: COURSE 42
```

Code narrows the union before using type-specific operations.

## Literal Types

```typescript
type Status = "draft" | "published";
const status: Status = "draft";
console.log(status);
// Output: draft
```

Invalid status spellings fail type checking.

## Arrays and Tuples

```typescript
const titles: string[] = ["HTML", "CSS"];
const point: readonly [number, number] = [10, 20];
console.log(titles[0], point[1]);
// Output: HTML 20
```

An array has one repeating element type. A tuple gives meaning to fixed positions.

## `unknown` vs `any`

- `unknown`: value is not trusted yet; check it first
- `any`: stop type checking; avoid it

```typescript
const printUppercase = (value: unknown): void => {
  if (typeof value !== "string") throw new TypeError("string required");
  console.log(value.toUpperCase());
};
printUppercase("typescript");
// Output: TYPESCRIPT
```

## Runtime Validation

This annotation does not validate JSON:

```typescript
// const course = JSON.parse(text) as Course;
```

Parse into `unknown`, inspect the actual value, then return a trusted type:

```typescript
const isCourse = (value: unknown): value is Course => {
  return typeof value === "object"
    && value !== null
    && "id" in value
    && typeof value.id === "string"
    && "title" in value
    && typeof value.title === "string"
    && "lessons" in value
    && typeof value.lessons === "number";
};
```

## Discriminated Unions

```typescript
type LoadState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; course: Course }
  | { status: "error"; message: string };
```

Each state contains only valid data. This is safer than several unrelated optional fields and booleans.

## Generics

Generics preserve relationships:

```typescript
const first = <T>(values: readonly T[]): T | undefined => values[0];
console.log(first([10, 20]), first(["HTML", "CSS"]));
// Output: 10 HTML
```

The result type follows the array element type.

## Strict Mode

Strict mode catches missing null checks, implicit `any`, unsafe function relationships, and other mistakes.

Start strict. Do not weaken the compiler to make invalid code pass.

## TypeScript Cannot Prove Everything

It cannot automatically prove:

- API JSON is valid
- a user is authorized
- a number is positive
- a string is safe HTML
- storage contains the current schema
- a network request succeeds
- code is fast or accessible

Those require runtime checks, server controls, testing, and measurement.

## Beginner to Expert Path

1. inference, annotations, primitives, arrays, objects
2. unions, literals, narrowing, nullability
3. functions, generics, classes, modules
4. runtime parsers, DOM, Fetch, configuration
5. mapped/conditional types, variance, declarations, public API design

## Final Rule

Use types to represent valid application values. Validate every external value before trusting it as one of those types.
