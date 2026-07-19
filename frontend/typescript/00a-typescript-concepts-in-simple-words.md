# TypeScript Concepts in Simple Words

## The One-Sentence Idea

TypeScript checks JavaScript relationships before the code runs, then removes its type syntax.

```text
.ts source -> type checker + transpiler/bundler -> JavaScript -> browser
# Result: types prevent many development mistakes but do not exist to validate runtime data.
```

## Key Ideas

- inference: compiler works out an obvious type
- annotation: developer explicitly states a type
- union: value may be one of several types
- narrowing: runtime evidence reduces a union
- generic: preserves type relationships in reusable code
- structural typing: compatible shape matters, not declared name
- unknown: value accepted but unusable until checked
- never: impossible value, useful for exhaustive checks

```typescript
type LoadState = { status: "loading" } | { status: "success"; value: string };
function message(state: LoadState): string {
  return state.status === "success" ? state.value : "Loading";
}
console.log(message({ status: "success", value: "Ready" }));
// Console output: Ready
```

## Compile-Time vs Runtime

```typescript
const data = JSON.parse('{"id":7}') as { id: number };
console.log(data.id);
// Console output: 7
// Warning: "as" trusted the programmer; it did not validate JSON.
```

Use a runtime schema/check at every untrusted boundary.

## Beginner Rule

Use simple types first. Add generics/mapped/conditional types only when they express a real relationship better than duplicated concrete types.
