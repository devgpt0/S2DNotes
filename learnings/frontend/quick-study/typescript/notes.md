# TypeScript: beginner-to-expert essential notes

TypeScript adds static type checking to JavaScript. It catches mistakes **while you write/build code**; types are removed at runtime. It cannot validate JSON from an API by itself.

Use strict mode:

```json
{ "compilerOptions": { "strict": true } }
```

## 1. Inference and annotations

TypeScript usually infers a type from a value. Add an annotation at public boundaries, complex shapes, and function returns when it improves clarity.

```ts
const total = 42;              // inferred as number
let label: string = "Total";

function add(left: number, right: number): number {
  return left + right;
}
```

Avoid `any`: it turns type checking off. Prefer `unknown` for data whose shape is not yet trusted. You must narrow `unknown` before using it.

```ts
function readMessage(value: unknown): string {
  if (typeof value !== "string") throw new Error("Expected a string");
  return value;
}
```

## 2. Object types, optional fields, tuples, and arrays

```ts
type User = {
  id: string;
  name: string;
  email?: string;
  readonly createdAt: Date;
};

const users: User[] = [];
```

`?` means the property may be absent, so `user.email` is `string | undefined`. Check it before string operations. `readonly` prevents reassignment through this type; it is not runtime immutability.

Use `type` for aliases, unions, and mapped/conditional types. Use `interface` mainly for object shapes that must be extended or declaration-merged. For most application code, choose one convention and stay consistent.

A tuple has a fixed position-based shape: `type Point = readonly [x: number, y: number]`. Use it only when positions are genuinely meaningful; named object fields are clearer for larger data.

## 3. Unions, literals, narrowing, and `never`

A union says a value can be one of several types. TypeScript narrows it after a safe runtime check.

```ts
type Status = "idle" | "loading" | "success" | "error";

function describe(value: string | number): string {
  return typeof value === "string" ? value.toUpperCase() : value.toFixed(2);
}
```

Use a discriminated union when variants have different data:

```ts
type Result =
  | { kind: "success"; data: string }
  | { kind: "error"; message: string };

function render(result: Result): string {
  switch (result.kind) {
    case "success": return result.data;
    case "error": return result.message;
  }
}
```

`never` means a value cannot exist, such as a function that always throws. It also makes exhaustive switches safe:

```ts
function assertNever(value: never): never {
  throw new Error(`Unhandled value: ${String(value)}`);
}
```

Call it in `default` after adding all known variants.

## 4. Functions, generics, and utility types

```ts
function first<T>(items: readonly T[]): T | undefined {
  return items[0];
}

const firstName = first(["Asha", "Ben"]); // string | undefined
```

A generic lets input and output keep their relationship. Do not use `any` where a generic is needed.

Constraints state what a generic needs:

```ts
function getId<T extends { id: string }>(value: T): string {
  return value.id;
}
```

Common utility types:

| Type | Meaning |
|---|---|
| `Partial<T>` | all properties optional |
| `Required<T>` | all required |
| `Pick<T, K>` | keep selected properties |
| `Omit<T, K>` | remove selected properties |
| `Record<K, V>` | object with keys `K` and values `V` |
| `Readonly<T>` | properties readonly |
| `ReturnType<F>` | a function return type |

Overloads describe a small set of call signatures. Prefer a union parameter when behavior and return type do not change. Avoid a generic that appears only once—it does not express a relationship.

## 5. `keyof`, indexed access, mapped, and conditional types

```ts
function getProperty<T extends object, K extends keyof T>(object: T, key: K): T[K] {
  return object[key];
}

type UserId = User["id"];
type Nullable<T> = { [K in keyof T]: T[K] | null };
type ElementType<T> = T extends readonly (infer Item)[] ? Item : never;
```

- `keyof T` creates a union of known property names.
- `T[K]` looks up the type of a property.
- Mapped types transform each property.
- Conditional types choose a type and can use `infer` to capture part of it.

These tools are valuable for reusable libraries and derived domain types. Do not make ordinary application code harder to read just to show type-level cleverness.

## 6. Classes, modules, and declarations

```ts
class UserService {
  constructor(private readonly baseUrl: string) {}

  async find(id: string): Promise<User> {
    const response = await fetch(`${this.baseUrl}/${encodeURIComponent(id)}`);
    if (!response.ok) throw new Error(`Request failed: ${response.status}`);
    const value: unknown = await response.json();
    if (!isUser(value)) throw new TypeError("Invalid user response");
    return value;
  }
}
```

Visibility modifiers are TypeScript checks; JavaScript `#privateField` provides runtime privacy. Prefer plain functions and objects unless a class owns state and behavior naturally.

Use `import type { User } from "./user.js"` for type-only dependencies when appropriate. Avoid namespaces in modern module-based applications. Declaration files (`.d.ts`) describe JavaScript types; they contain no implementation.

## 7. Runtime boundaries and everyday pitfalls

Types do not validate API responses. Parse and validate untrusted data at runtime (with explicit checks or a schema library), then return a typed value.

```ts
function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null
    && "id" in value && typeof value.id === "string"
    && "name" in value && typeof value.name === "string";
}
```

Prefer `as const` for immutable literal data and narrow values:

```ts
const roles = ["admin", "member"] as const;
type Role = (typeof roles)[number];
```

A type assertion (`value as User`) tells the compiler to trust you; it does not check anything. Use it only when you have already proved the value’s shape.

`enum` works, but a string-literal union is often simpler, has no runtime output, and is easier to compose.

Use `satisfies` to check a value without widening away useful literal information:

```ts
const routes = {
  home: "/",
  profile: "/profile",
} satisfies Record<string, `/${string}`>;
```

## 8. Compiler options and production discipline

Important settings include `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, and `noImplicitOverride`. Choose module/target settings that match the actual runtime and build tool. Keep type checking in CI; transpilation alone may not check types.

```text
untrusted JSON → unknown → runtime validation → trusted domain type
```

Do not weaken errors with `any`, broad assertions, non-null assertions (`!`), or suppression comments. Model missing data explicitly and fail at the boundary when external data is invalid.

## 9. Common mistakes

- Believing types exist at runtime.
- Using `any` for convenience.
- Writing `as User` instead of validating data.
- Returning `T` from a generic without having a real `T` value.
- Confusing optional (`value?: T`) with required-but-possibly-undefined (`value: T | undefined`).
- Forgetting that `readonly` and `Readonly<T>` are shallow compile-time checks.

## Interview checklist

Explain inference vs annotations, `any` vs `unknown`, `type` vs `interface`, optional fields, unions/narrowing/discriminated unions, `never`, generics/constraints, utility types, assertions, and compile-time types vs runtime validation.
