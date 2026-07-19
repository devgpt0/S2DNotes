# TypeScript - Beginner to Expert Roadmap

Code convention: standalone functions use typed arrow variables by default, such as `const total = (price: number): number => price;`. Real class/object methods and language cases that cannot use arrows remain explicit exceptions.

TypeScript adds compile-time type checking to JavaScript. Its types are removed when code is compiled; the browser runs JavaScript.

These notes use modern TypeScript in strict mode. The examples require features such as `satisfies`, `NoInfer`, and `const` type parameters; keep the repository compiler current and verify its release notes during upgrades. Learn JavaScript first.

## Phase 1 - Build a Correct Foundation

1. [TypeScript concepts in simple words](00a-typescript-concepts-in-simple-words.md)
2. [Setup, inference, annotations, and strict mode](01-setup-inference-annotations-and-strict-mode.md)
3. [Critical TypeScript types - complete guide](10-critical-types-complete-guide.md)
4. [Unions, literals, narrowing, unknown, and never](02-unions-literals-narrowing-unknown-and-never.md)
5. [Object types, interfaces, aliases, and structural typing](03-object-types-interfaces-aliases-and-structural-typing.md)
6. [Functions and generics](04-functions-and-generics.md)

## Phase 2 - Write Application TypeScript

7. [Classes, modules, and declarations](05-classes-modules-and-declarations.md)
8. [Keyof, indexed access, utility, mapped, and conditional types](06-advanced-type-tools.md)
9. [DOM, Fetch, async code, and runtime validation](07-dom-fetch-async-and-runtime-validation.md)
10. [Configuration, builds, libraries, testing, and migration](08-configuration-builds-testing-and-migration.md)
11. [Practical activities and interview answers](09-typescript-practical-and-interview-answers.md)

## Phase 3 - Senior and Expert Type Design

12. [Narrowing, type guards, and runtime trust](11-narrowing-type-guards-and-runtime-trust.md)
13. [Generics, inference, and variance](12-generics-inference-and-variance.md)
14. [Mapped, conditional, template, and recursive types](13-advanced-type-transformations.md)
15. [Modules, declaration files, and library design](14-modules-declarations-and-library-design.md)
16. [Expert TypeScript tips and type-design patterns](98-typescript-expert-tips.md)
17. [Complete typed expense tracker project](99-typescript-60-minute-project.md)

## Core Rule

TypeScript proves relationships at compile time. It does not validate JSON, user input, environment variables, or browser storage at runtime.
