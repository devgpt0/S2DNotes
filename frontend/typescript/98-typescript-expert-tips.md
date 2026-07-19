# TypeScript Expert Tips and Type-Design Patterns

## Strictness

- Enable `strict`, `noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes` early.
- Use `unknown` at untrusted boundaries and narrow/validate it.
- Treat `any`, non-null assertions, and broad type assertions as review signals.
- Run `tsc --noEmit` separately because bundlers may transpile without full type checking.
- Match module/moduleResolution/import extensions to the actual runtime or bundler.

## Type Modeling

- Model valid states with discriminated unions instead of optional-property bags.
- Use literal unions for closed choices when runtime enum objects are unnecessary.
- Keep domain IDs distinguishable with branded/opaque types only when accidental mixing is a demonstrated risk.
- Prefer readonly inputs/returns to communicate ownership, but remember it is shallow compile-time protection.
- Use `satisfies` to check a contract while preserving useful literal inference.
- Derive types from stable sources instead of duplicating API/domain definitions manually.

## Generics

- Every type parameter should express a relationship.
- Constrain generics only as much as implementation needs.
- Prefer `keyof` relationships to unsafe string property names.
- Avoid generic “configuration engines” whose errors become unreadable.
- Provide simple overloads or concrete wrappers for common public use cases.

## Public APIs

- Export small stable types and hide implementation helpers.
- Accept broader safe inputs and return precise owned outputs.
- Avoid leaking third-party library types through your domain API unless intentionally coupled.
- Use type-only imports/exports to clarify runtime graph.
- For libraries, test generated declarations from a consumer project.
- A type-level breaking change is still an API breaking change.

## Runtime Boundaries

Validate fetch responses, storage, URL params, postMessage, environment/config, forms, and third-party callbacks.
- Keep parser/validator next to boundary and convert to trusted domain type.
- Distinguish missing, null, and invalid rather than coercing silently.
- Never use `as` to “fix” a runtime schema mismatch.
- Return actionable validation issues without leaking sensitive input.

## Advanced Type Restraint

- Mapped/conditional/template-literal types are valuable when they remove real inconsistency.
- Name intermediate types and add type tests for complex transformations.
- Prevent accidental distributive conditional types by tuple-wrapping when needed.
- Watch compiler/editor performance from enormous unions and recursive types.
- Prefer code generation from authoritative schemas over heroic handwritten type transformations.

## Migration Tips

- Migrate leaf modules and boundaries incrementally.
- Prevent new `any` while reducing existing unsafe regions.
- Type tests and runtime tests solve different problems; keep both.
- Replace assertion chains with validators/type guards.
- Track strictness debt explicitly; do not leave `strict: false` permanently.

## Interview Traps

Type erasure, `any` vs unknown, union vs intersection, interface vs alias, structural typing, excess-property checks, covariance/readonly arrays, function parameter variance, generic inference, `never`, declaration merging, `satisfies`, and compile-time vs runtime validation.

## Expert Code Snippets Used in Production

### Exhaustive State Handling

```typescript
type State = { status: "idle" } | { status: "loading" } | { status: "success"; value: string } | { status: "error"; message: string };
const label = (state: State): string => {
  switch (state.status) {
    case "idle": return "Start";
    case "loading": return "Loading";
    case "success": return state.value;
    case "error": return state.message;
    default: return state satisfies never;
  }
};
console.log(label({ status: "success", value: "Ready" }));
// Console output: Ready; adding a new state fails compilation until handled.
```

### Result Type for Expected Failure

```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
const parsePositive = (value: string): Result<number, string> => {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed > 0 ? { ok: true, value: parsed } : { ok: false, error: "Expected positive number" };
};
console.log(parsePositive("5"));
// Console output: {ok: true, value: 5}
```

### Branded IDs to Prevent Mixing

```typescript
type Brand<T, Name extends string> = T & { readonly __brand: Name };
type UserId = Brand<string, "UserId">;
type CourseId = Brand<string, "CourseId">;
const userId = (value: string): UserId => value as UserId;
console.log(userId("user-1"));
// Console output: user-1; compile time prevents passing UserId where CourseId is required.
```

Use brands at validated construction boundaries; the assertion itself is not validation.

### Type-Safe Event Map

```typescript
type Events = { "course:created": { id: string }; "course:deleted": { id: string; reason: string } };
const emit = <Name extends keyof Events>(name: Name, payload: Events[Name]): void => { console.log(name, payload); };
emit("course:created", { id: "html" });
// Console output: course:created {id: "html"}; mismatched payloads fail type checking.
```

### Runtime Validator Returning Trusted Type

```typescript
type Course = Readonly<{ id: string; title: string }>;
const parseCourse = (value: unknown): Course => {
  if (typeof value !== "object" || value === null) throw new TypeError("course must be an object");
  if (!("id" in value) || typeof value.id !== "string"
    || !("title" in value) || typeof value.title !== "string") {
    throw new TypeError("invalid course fields");
  }
  return { id: value.id, title: value.title };
};
console.log(parseCourse({ id: "html", title: "HTML" }).title);
// Console output: HTML
```

## High-Use Typed Variant and Responsive-Behavior Pattern

```typescript
type Tone = "primary" | "secondary" | "danger";
const TONE_CLASSES = {
  primary: "button button--primary",
  secondary: "button button--secondary",
  danger: "button button--danger",
} satisfies Record<Tone, string>;

const buttonClass = (tone: Tone): string => {
  return TONE_CLASSES[tone];
};

const wideLayout = window.matchMedia("(min-width: 48rem)");
console.log(buttonClass("primary"), wideLayout.matches);
// Result: every finite variant is required at compile time; media-query behavior remains a boolean browser value.
```

Prefer CSS for layout. Use the typed media query only when application behavior—not merely appearance—must change.
