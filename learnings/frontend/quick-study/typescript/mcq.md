# TypeScript interview MCQs with explanations

Answer each question before reading the explanation.

## 1. When do TypeScript types primarily exist?

- A. At runtime
- B. During compilation and type checking
- C. While the database runs
- D. During browser painting

**Answer: B — During type checking.** Types are erased when TypeScript becomes JavaScript, so they cannot enforce runtime behavior by themselves.

## 2. Which compiler option enables the main strict checks?

- A. `fast`
- B. `strict`
- C. `safeRuntime`
- D. `typed`

**Answer: B — `strict`.** It enables a family of checks that catch unsafe null handling, implicit `any`, and other common type mistakes.

## 3. What does `any` do?

- A. Validates unknown data
- B. Disables useful type checking for that value
- C. Creates a generic
- D. Makes a value immutable

**Answer: B — It opts out of type safety.** Operations on `any` are trusted without proof, and that unsafety can spread through otherwise typed code.

## 4. Why is `unknown` preferred for untrusted input?

- A. It accepts no values
- B. It requires narrowing before use
- C. It always represents a string
- D. It validates JSON automatically

**Answer: B — It forces proof before use.** Any value can enter `unknown`, but code must check its runtime shape before performing type-specific operations.

## 5. Which check safely narrows `unknown` to `string`?

- A. `value as string`
- B. `typeof value === "string"`
- C. `String(value)`
- D. `value!`

**Answer: B — A `typeof` check.** It supplies runtime evidence. An assertion merely instructs the compiler, while `String(value)` converts rather than validates.

## 6. What does `email?: string` mean?

- A. Email is always present
- B. The property may be absent
- C. The property is private
- D. The property must be null

**Answer: B — It is optional.** Reading it may produce `undefined`, so code must handle absence before using string methods.

## 7. What does `readonly` provide?

- A. Deep runtime freezing
- B. Compile-time reassignment protection through that type
- C. Encryption
- D. Serialization

**Answer: B — Compile-time protection.** It does not freeze the value at runtime and is shallow unless nested values are also typed as readonly.

## 8. What does a union type represent?

- A. Every member type simultaneously
- B. One of several possible types
- C. No possible type
- D. Only a class hierarchy

**Answer: B — One of several types.** For example, `string | number` accepts either type, and code must narrow before using operations unique to one member.

## 9. What makes a discriminated union easy to narrow?

- A. A shared property with distinct literal values
- B. The same class name
- C. A type assertion
- D. Making every property optional

**Answer: A — A literal discriminant.** Checking a field such as `status: "success" | "error"` tells TypeScript exactly which member is present.

## 10. What does `never` represent?

- A. Any possible value
- B. A value that cannot occur
- C. Null only
- D. A missing annotation

**Answer: B — An impossible value.** It appears in functions that never return and is useful for proving that every union member was handled.

## 11. What is a generic mainly used for?

- A. Removing types
- B. Preserving relationships between types
- C. Runtime reflection
- D. Styling components

**Answer: B — Expressing type relationships.** A generic can state that a function returns the same item type accepted by its input without losing specificity.

## 12. What does `T extends { id: string }` mean?

- A. `T` must be a subclass
- B. `T` must contain a string `id`
- C. `T` returns an ID
- D. `T` must be exactly that object

**Answer: B — It constrains `T`.** Structural typing allows additional properties, but every valid `T` must provide the required string ID.

## 13. What does `Partial<T>` do?

- A. Removes half the properties
- B. Makes every property optional
- C. Makes every property nullable
- D. Makes every property readonly

**Answer: B — All properties become optional.** It is useful for patch-like shapes, but does not recursively change nested object properties.

## 14. What does `Pick<T, K>` do?

- A. Keeps selected properties `K`
- B. Removes selected properties `K`
- C. Selects array items at runtime
- D. Validates runtime keys

**Answer: A — It keeps selected properties.** The resulting type contains only the chosen keys from `T`; no runtime object transformation occurs.

## 15. What does `Omit<T, K>` do?

- A. Requires `K`
- B. Removes properties `K` from the type
- C. Makes `K` private
- D. Renames `K`

**Answer: B — It removes selected properties.** Like other utility types, it only changes the compile-time view, not a runtime object.

## 16. What does `Record<K, V>` describe?

- A. A tuple
- B. An object whose keys are `K` and values are `V`
- C. A database row only
- D. A class instance only

**Answer: B — A key/value object type.** For example, `Record<Role, Permission[]>` requires an array of permissions for every Role key.

## 17. What does `keyof T` produce?

- A. A runtime array of keys
- B. A union of known property keys
- C. An object's values
- D. A Boolean

**Answer: B — A key union.** If `T` has `id` and `name`, `keyof T` is typically `"id" | "name"`; it creates no runtime array.

## 18. What does `T[K]` represent in a type position?

- A. Runtime access only
- B. The property type of `T` at key `K`
- C. A generic array
- D. A mapped loop

**Answer: B — Indexed access type.** It lets one type derive the exact value type associated with another type's key.

## 19. What does a mapped type do?

- A. Runs `Array.map`
- B. Transforms properties of a type
- C. Maps HTTP routes
- D. Validates JSON

**Answer: B — It transforms a type's properties.** It iterates over keys at compile time and can change modifiers or value types.

## 20. Which keyword captures part of a type inside a conditional type?

- A. `await`
- B. `infer`
- C. `yield`
- D. `implements`

**Answer: B — `infer`.** It introduces a type variable from the structure being matched, such as extracting an array's element type.

## 21. What does `as const` usually do?

- A. Runs runtime validation
- B. Narrows literal values and makes properties or items readonly
- C. Converts a value to JSON
- D. Creates a runtime constant

**Answer: B — It preserves narrow literals.** An array such as `["admin", "member"] as const` retains those exact values instead of widening to `string[]`.

## 22. What does `satisfies` do?

- A. Checks compatibility while preserving useful inference
- B. Performs an unsafe cast
- C. Validates at runtime
- D. Extends a class

**Answer: A — It checks without replacing the inferred type.** This catches shape errors while retaining literal keys and values for later type-safe use.

## 23. What does `value as User` do at runtime?

- A. Fully validates the value
- B. Nothing
- C. Converts the value
- D. Throws when the value is wrong

**Answer: B — Nothing.** A type assertion is removed from emitted JavaScript. External values still require runtime validation.

## 24. Which type is usually simplest for a small fixed set of strings?

- A. Namespace
- B. String-literal union
- C. Abstract class
- D. Decorator

**Answer: B — A string-literal union.** It is composable, readable, and adds no generated runtime object, unlike many enum configurations.

## 25. Which declaration supports declaration merging?

- A. Type alias
- B. Interface
- C. Tuple
- D. Conditional type

**Answer: B — Interface.** Multiple compatible declarations with the same interface name merge, a feature useful for library and platform augmentation.

## 26. What does `import type` import?

- A. Runtime side effects
- B. A type-only binding
- C. JSON data
- D. CSS

**Answer: B — Type-only information.** It communicates that the import is erased and prevents it from being treated as a runtime dependency.

## 27. What is a `.d.ts` file?

- A. JavaScript implementation
- B. Type declarations
- C. Test data
- D. A source map

**Answer: B — A declaration file.** It describes the public types of JavaScript code or ambient APIs but contains no executable implementation.

## 28. Can TypeScript alone prove that an API response matches a type?

- A. Yes
- B. No; runtime validation is required
- C. Only when using `as`
- D. Only when using an interface

**Answer: B — Runtime validation is required.** Network data is runtime input and can violate declared expectations regardless of compile-time types.

## 29. What does `noUncheckedIndexedAccess` help expose?

- A. Possibly missing indexed values
- B. Slow loops
- C. Private fields
- D. Circular modules

**Answer: A — Missing indexed values.** An array or dictionary lookup gains `undefined` because the requested key or index may not exist.

## 30. What is the best replacement for an unjustified non-null assertion (`!`)?

- A. Another assertion
- B. An explicit check or accurate model of absence
- C. `any`
- D. Disabling strict mode

**Answer: B — Check or model the value.** Proving presence produces safer runtime behavior; `!` only hides the compiler warning and can leave a crash.
