# 02 - Unions, Literals, Narrowing, Unknown, and Never

## Union Types

```typescript
function formatId(id: string | number): string {
  return typeof id === "number" ? id.toFixed(0) : id.toUpperCase();
}
console.log(formatId(42), formatId("ord-7"));
// Console output: 42 ORD-7
```

Narrowing proves which union member is present before member-specific operations.

## Literal Types

```typescript
type Theme = "light" | "dark";
function applyTheme(theme: Theme): string { return `theme-${theme}`; }
console.log(applyTheme("dark"));
// Console output: theme-dark
// Other strings fail type checking.
```

## Discriminated Union

```typescript
type Result =
  | { status: "success"; value: string }
  | { status: "error"; message: string };

function describe(result: Result): string {
  return result.status === "success" ? result.value : result.message;
}
console.log(describe({ status: "success", value: "ready" }));
// Console output: ready
```

This is safer than several optional properties that allow impossible combinations.

## `unknown`

```typescript
function isString(value: unknown): value is string {
  return typeof value === "string";
}
const value: unknown = "TypeScript";
if (isString(value)) console.log(value.toUpperCase());
// Console output: TYPESCRIPT
```

## Exhaustiveness and `never`

```typescript
type Shape = { kind: "circle"; radius: number } | { kind: "square"; side: number };
function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "square": return shape.side ** 2;
    default: return shape satisfies never;
  }
}
console.log(area({ kind: "square", side: 4 }));
// Console output: 16
```

Adding a new shape makes the exhaustive check fail until handled.

## Type Assertion Warning

`value as Type` tells the compiler to trust you; it performs no runtime check. Prefer narrowing or validation. Double assertions through `unknown` are a strong warning that the design is unsafe.
