# 04 - TypeScript Functions and Generics

## Function Type

```typescript
type Operation = (left: number, right: number) => number;
const add: Operation = (left, right) => left + right;
console.log(add(20, 22));
// Console output: 42
```

## Optional, Default, and Rest Parameters

```typescript
const greet = (name = "Guest", ...titles: string[]): string => {
  return `Hello ${titles.join(" ")} ${name}`.replaceAll("  ", " ");
};
console.log(greet("Asha", "Dr."));
// Console output: Hello Dr. Asha
```

Optional parameters come after required parameters unless using an options object.

## Generics Preserve Relationships

```typescript
const first = <T>(values: readonly T[]): T | undefined => {
  return values[0];
};
console.log(first([10, 20]));
console.log(first(["HTML", "CSS"]));
// Console output:
// 10
// HTML
```

The same input element type becomes the output type. A generic should express a useful relationship, not replace a concrete type unnecessarily.

## Generic Constraint

```typescript
const getId = <T extends { id: string }>(value: T): string => {
  return value.id;
};
console.log(getId({ id: "course-1", title: "HTML" }));
// Console output: course-1
```

## `keyof` Relationship

```typescript
const get = <T extends object, K extends keyof T>(value: T, key: K): T[K] => {
  return value[key];
};
console.log(get({ name: "Asha", age: 25 }, "name"));
// Console output: Asha
```

## Overloads

Use overloads when call signatures produce meaningfully different related types. Prefer a union when behavior and return shape are the same.

```typescript
type Length = {
  (value: string): number;
  (value: readonly unknown[]): number;
};
const length: Length = (value: string | readonly unknown[]): number => value.length;
console.log(length("Java"), length([1, 2]));
// Console output: 4 2
```

The implementation signature is not directly callable and must safely cover every overload.
