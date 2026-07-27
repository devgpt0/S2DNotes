# TypeScript: 3 commonly asked coding questions

Strict, executable source files are in [`examples/src`](examples/src/).

```powershell
cd frontend/quick-study/typescript/examples
npm.cmd install
npm.cmd run check
npm.cmd run examples
```

Results appear in the terminal. Use `npm.cmd run example:1`, `example:2`, or `example:3` to run one example.

For a complete strict TypeScript project with visible browser results, follow [the runnable example guide](./examples/README.md).

## 1. Implement a type-safe property getter

**Question:** Accept only keys that exist on the object and infer the exact property type.

```ts
function getProperty<T extends object, K extends keyof T>(object: T, key: K): T[K] {
  return object[key];
}

const user = { id: "u1", age: 28 };
const id = getProperty(user, "id");   // string
const age = getProperty(user, "age"); // number
// getProperty(user, "email");        // compile error
```

## 2. Model and exhaustively handle request state

**Question:** Prevent impossible state combinations and make adding an unhandled state a compile error.

```ts
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string };

function describe<T>(state: RequestState<T>): string {
  switch (state.status) {
    case "idle": return "Ready";
    case "loading": return "Loading";
    case "success": return `Loaded: ${JSON.stringify(state.data)}`;
    case "error": return state.message;
    default: return assertNever(state);
  }
}

function assertNever(value: never): never {
  throw new Error(`Unhandled state: ${JSON.stringify(value)}`);
}
```

## 3. Validate unknown API data

**Question:** Safely narrow unknown JSON to a `User`; do not use a type assertion.

```ts
type User = { id: string; name: string };

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) return false;
  return "id" in value
    && typeof value.id === "string"
    && "name" in value
    && typeof value.name === "string";
}

function parseUser(value: unknown): User {
  if (!isUser(value)) throw new TypeError("Invalid user response");
  return value;
}

console.log(parseUser({ id: "u1", name: "Asha" }));
```
