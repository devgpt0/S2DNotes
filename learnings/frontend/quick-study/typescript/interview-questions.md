# TypeScript: 10 most-asked interview questions

## 1. What is TypeScript, and does it run in the browser?

TypeScript is JavaScript plus static type analysis and type syntax. It is compiled/transpiled to JavaScript before normal execution. Its types are erased and therefore do not validate runtime data.

## 2. What is the difference between `any` and `unknown`?

`any` opts out of checking and spreads unsafety. `unknown` can hold any value but must be narrowed before use. Use `unknown` at untrusted boundaries and validate it.

## 3. `type` versus `interface`?

Both describe object shapes. Interfaces support declaration merging and natural extension; type aliases also represent unions, tuples, primitives, mapped types, and conditional types. Neither validates runtime objects; choose a consistent convention.

## 4. What is type narrowing?

Narrowing uses runtime evidence—`typeof`, `instanceof`, equality, property checks, discriminants, or a type predicate—to reduce a broad type to a safe specific type within a control-flow branch.

## 5. What is a discriminated union?

It is a union whose members share a literal field such as `status`. Switching on that field gives precise member data, prevents impossible combinations, and supports exhaustive checking with `never`.

## 6. What are generics?

Generics parameterize types while preserving relationships, such as “the output item has the input array’s item type.” Constraints specify capabilities the generic must have. A generic should express a real relationship, not replace a concrete type needlessly.

## 7. What do `keyof` and `T[K]` do?

`keyof T` forms a union of known property keys. `T[K]` looks up the value type at key `K`. Together they enable APIs such as a getter that accepts only valid keys and returns the correct property type.

## 8. Type assertion versus type guard?

An assertion tells the compiler to trust the programmer and generates no check. A guard performs a runtime check that TypeScript understands. Prefer guards or schema validation for external data; use assertions only when safety is already proven.

## 9. What are mapped and conditional types?

Mapped types transform properties by iterating keys; utilities such as `Partial` use them. Conditional types select a type based on assignability and may use `infer`. They are powerful but should not obscure simple application code.

## 10. Which strict options matter in production?

Start with `strict`. Consider `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, and project-appropriate module/target settings. Run the type checker in CI and never silence errors merely to make a build pass.
