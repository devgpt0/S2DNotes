# 09 - TypeScript Practical Activities and Interview Answers

## Activity: Typed Course Search

Build a page that fetches courses, validates the runtime response, renders results, supports loading/error/empty states, and cancels obsolete searches.

Requirements:

- strict tsconfig
- no `any`, type assertions only after proven boundary logic
- discriminated union for UI state
- runtime validator for API data
- typed DOM elements/events
- AbortController cancellation
- unit tests for validation and state transitions

### Example State

```typescript
type SearchState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; courses: readonly Course[] }
  | { status: "error"; message: string };

const state: SearchState = { status: "loading" };
console.log(state.status);
// Console output: loading
```

## Activity: Generic Table

Create a generic table function/component whose columns use `keyof` relationships, renders empty state, and remains accessible. Avoid rendering arbitrary values without a formatter.

## Interview Questions with Answers

### 1. TypeScript vs JavaScript?

TypeScript is JavaScript plus compile-time type syntax/checking. Types are erased; runtime executes JavaScript.

### 2. `any` vs `unknown`?

`any` disables checking. `unknown` accepts any value but requires narrowing before use, making it appropriate for untrusted boundaries.

### 3. Interface vs type alias?

Both describe object shapes. Interfaces support declaration merging and extension; type aliases also express unions, tuples, mapped/conditional types, and primitives.

### 4. Union vs intersection?

Union means one of several types. Intersection requires all combined type requirements.

### 5. What is narrowing?

Control-flow evidence such as `typeof`, `instanceof`, discriminants, property checks, or a type predicate reduces a broader type to a more specific one.

### 6. What is a generic?

A type parameter that preserves relationships between inputs and outputs while keeping reusable code type safe.

### 7. What is structural typing?

Compatibility depends on required members rather than explicit declared type names.

### 8. Does `as Course` validate JSON?

No. It is compile-time trust. Runtime data must be checked with explicit validation or a schema library.

### 9. `private` vs `#private`?

TypeScript `private` restricts through type checking. JavaScript `#private` is enforced by the runtime language.

### 10. Why use `satisfies`?

It checks that an expression conforms to a type while retaining useful narrow inference instead of replacing the expression's type with a broad annotation.

### 11. What is `never` used for?

It represents impossible values and supports exhaustive union checks so adding a new case causes a compile error until handled.

### 12. How do you migrate safely?

Convert incrementally, type boundaries first, keep strictness moving upward, validate runtime data, prevent new unsafe code in CI, and remove temporary assertions/settings.
