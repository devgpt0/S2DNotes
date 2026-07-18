# 07 - TypeScript DOM, Fetch, Async Code, and Runtime Validation

## DOM Null Safety

```typescript
const button = document.querySelector<HTMLButtonElement>("#save");
if (!button) throw new Error("#save button is required");
button.disabled = true;
console.log(button.disabled);
// Console output: true
```

The generic narrows element type, but the result remains nullable because selectors can fail.

## Typed Events

```typescript
const input = document.querySelector<HTMLInputElement>("#email");
if (!input) throw new Error("#email is required");
input.addEventListener("input", event => {
  const target = event.currentTarget;
  console.log(target.value);
});
// Console output while typing: current email field value.
```

`currentTarget` is safer than asserting an arbitrary bubbled `target`.

## Fetch Returns Untrusted Data

```typescript
type Course = { id: string; title: string };

function isCourse(value: unknown): value is Course {
  if (typeof value !== "object" || value === null) return false;
  const item = value as Record<string, unknown>;
  return typeof item.id === "string" && typeof item.title === "string";
}

const response = await fetch("/api/course/html");
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const data: unknown = await response.json();
if (!isCourse(data)) throw new TypeError("Invalid course response");
console.log(data.title);
// Module console output on valid response: course title.
```

Writing `const data = await response.json() as Course` does not validate anything.

For large schemas, use a runtime validation library that returns typed validated data.

## Typed Error Handling

```typescript
try {
  throw new Error("failed");
} catch (error: unknown) {
  console.log(error instanceof Error ? error.message : "Unknown failure");
}
// Console output: failed
```

## Promise Types

```typescript
async function loadName(): Promise<string> {
  return "Asha";
}
console.log(await loadName());
// Module console output: Asha
```

Use `Awaited<T>` when deriving a resolved value type from nested promise-like types.
