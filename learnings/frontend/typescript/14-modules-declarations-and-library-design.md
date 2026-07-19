# 14 - Modules, Declaration Files, and Library Design

## What Is a Module?

A file with a top-level `import` or `export` is a module. Its declarations do not automatically become global.

```typescript
// price.ts
export const formatPrice = (amount: number): string => `₹${amount.toFixed(2)}`;
```

```typescript
// app.ts
import { formatPrice } from "./price.js";
console.log(formatPrice(499));
// Console output: ₹499.00
```

The correct import extension and emitted path depend on the runtime and `moduleResolution` mode. Follow the rules of your chosen Node, bundler, or library environment.

## Named and Default Exports

Named exports make the imported name explicit and support several exports:

```typescript
type Course = Readonly<{ id: string; title: string }>;

export const parseCourse = (value: unknown): Course => {
  if (typeof value !== "object" || value === null
    || !("id" in value) || typeof value.id !== "string"
    || !("title" in value) || typeof value.title !== "string") {
    throw new TypeError("invalid course");
  }
  return { id: value.id, title: value.title };
};
export type { Course };
```

A default export allows the caller to choose any local name:

```typescript
const CoursePage = () => null;
export default CoursePage;
```

Use a consistent repository policy. Named exports are often easier for refactoring and discovery; framework conventions may deliberately use defaults.

## Type-Only Imports and Exports

```typescript
import type { Course } from "./course.js";
import { parseCourse } from "./course.js";

export type { Course };
export { parseCourse };
```

Type-only imports disappear from runtime JavaScript. With `verbatimModuleSyntax`, the source must state this intent accurately.

## Avoid Barrel Cycles

A barrel re-exports from one index:

```typescript
// index.ts
export { parseCourse } from "./parse-course.js";
export type { Course } from "./course.js";
```

Barrels can simplify a stable public package surface. Internal barrels can also hide circular dependencies, increase loaded modules, and make ownership unclear.

Prefer direct feature imports internally unless a public boundary has a demonstrated reason.

## Runtime Cycles vs Type Cycles

Two modules importing each other's runtime values can observe partially initialized bindings.

Break cycles by:

- moving a shared contract into a lower-level module
- passing a dependency into a function
- separating types from runtime initialization
- changing ownership, not merely switching import syntax

`import type` removes a runtime edge only when the dependency is genuinely type-only.

## Declaration Files

A `.d.ts` file describes types for JavaScript that exists elsewhere. It emits no runtime implementation.

```typescript
// course-client.d.ts
export type Course = Readonly<{ id: string; title: string }>;
export declare const loadCourse: (id: string) => Promise<Course>;
```

The package must still provide a real JavaScript `loadCourse` function. Writing `declare` does not create it.

## Typing a Local Untyped Module

```typescript
// legacy-parser.d.ts
declare module "legacy-parser" {
  export type ParsedCourse = Readonly<{ id: string; title: string }>;
  export const parseCourse: (text: string) => ParsedCourse;
}
```

This is a promise made by your declaration. Verify it against runtime behavior and add boundary tests. A wrong declaration is a compiler-approved lie.

## Global Declarations

```typescript
// environment.d.ts
export {};

declare global {
  interface Window {
    courseAppVersion: string;
  }
}
```

`export {}` keeps the file a module while `declare global` intentionally adds a global type.

Use globals only for real platform or host-provided values. Prefer imports for application dependencies.

## Declaration Merging

Interfaces with the same name can merge:

```typescript
interface CourseMetadata {
  title: string;
}

interface CourseMetadata {
  lessons: number;
}

const metadata: CourseMetadata = { title: "TypeScript", lessons: 14 };
console.log(metadata.lessons);
// Console output: 14
```

Merging is useful for intentional library augmentation. It can be confusing for closed application-domain models, where a type alias may better communicate one owned shape.

## Module Augmentation

```typescript
import "express-session";

declare module "express-session" {
  interface SessionData {
    userId: string;
  }
}
```

Augmentation changes TypeScript's view of an existing module. It does not initialize `userId` at runtime. Your authentication flow must still establish and validate it.

## ESM and CommonJS

Modern projects should choose an explicit module strategy.

Important inputs include:

- package `"type"`
- file extensions
- `module`
- `moduleResolution`
- runtime version
- bundler behavior
- dependency export maps

Do not enable interoperability flags blindly. Test the emitted JavaScript and actual runtime import behavior.

## Package Export Maps

A library can expose only supported entry points:

```json
{
  "name": "@example/course-kit",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./testing": {
      "types": "./dist/testing.d.ts",
      "import": "./dist/testing.js"
    }
  }
}
```

Export maps prevent consumers from depending on internal files. Changing an exported type can be a breaking change even when runtime JavaScript is unchanged.

## Library Compiler Configuration

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "dist",
    "rootDir": "src",
    "verbatimModuleSyntax": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedIndexedAccess": true
  },
  "include": ["src"]
}
```

This is a library example, not a universal application config. A bundler application often uses `moduleResolution: "Bundler"` and `noEmit`.

## Public Type Design

Good public types:

- expose domain concepts, not internal implementation types
- use readonly inputs where mutation is unnecessary
- model errors and async results deliberately
- avoid leaking a framework type through every consumer
- keep generic parameters meaningful and ordered consistently
- document runtime validation separately from compile-time types

## Compatibility Traps

Potential breaking changes include:

- making an optional property required
- removing a union member consumers handle
- adding a union member to an API consumers exhaustively switch over
- narrowing accepted callback parameters
- changing generic defaults or order
- changing ESM/CommonJS export behavior
- moving or removing declaration entry points

Use type-level consumer tests for important library contracts.

## Project References

Large repositories can use project references for build boundaries and incremental checking. Add them only when packages have real dependency boundaries; they increase configuration and output ownership.

## Testing Declarations

Test both runtime and types:

```typescript
import { expectTypeOf, test } from "vitest";
import { loadCourse } from "./course-client.js";

test("loadCourse exposes a Course promise", () => {
  expectTypeOf(loadCourse("ts")).toEqualTypeOf<Promise<Course>>();
});
```

A type test does not prove network or parsing behavior. Pair it with runtime tests.

## Beginner to Expert Path

- beginner: named exports, imports, type-only imports
- developer: module boundaries, cycles, aliases, `.d.ts`
- senior: package exports, public compatibility, augmentations
- expert: ESM/CJS interop, declaration emission, multi-package builds, consumer type tests

## Final Rule

Types and modules are public contracts. Keep the runtime implementation, emitted JavaScript, declaration files, and package export map aligned.
