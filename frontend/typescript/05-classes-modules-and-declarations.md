# 05 - TypeScript Classes, Modules, and Declarations

## Class

```typescript
class Counter {
  #value = 0;
  increment(): void { this.#value += 1; }
  get value(): number { return this.#value; }
}
const counter = new Counter();
counter.increment();
console.log(counter.value);
// Console output: 1
```

JavaScript `#private` is runtime-private. TypeScript `private` is primarily compile-time private and emits ordinary JavaScript properties depending on target.

## Parameter Properties

```typescript
class CourseService {
  constructor(private readonly endpoint: URL) {}
  describe(): string { return this.endpoint.href; }
}
console.log(new CourseService(new URL("https://example.com/api/")).describe());
// Console output: https://example.com/api/
```

## Implements

```typescript
interface Printable { print(): string }
class Receipt implements Printable {
  constructor(readonly total: number) {}
  print(): string { return `Total: ${this.total}`; }
}
console.log(new Receipt(500).print());
// Console output: Total: 500
```

`implements` checks the instance shape; it does not copy implementation.

## Modules

```typescript
// price.ts
export const addTax = (price: number): number => price * 1.18;

// app.ts
import { addTax } from "./price.js";
console.log(addTax(100));
// Console output: 118
```

Import specifiers must match the selected module/bundler/runtime behavior. Modern Node-style TypeScript may intentionally use `.js` in source imports for emitted files.

## Type-Only Import

```typescript
import type { Course } from "./course.js";
const value: Course = { id: "html", title: "HTML" };
console.log(value.title);
// Console output: HTML; type-only import is removed from emitted JavaScript.
```

## Declaration Files

`.d.ts` files describe JavaScript types without implementation. Prefer official/bundled types; use `@types/*` when a library publishes community declarations. Do not write a broad `declare module "*"` that hides missing types.
