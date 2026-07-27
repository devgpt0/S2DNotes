# JavaScript: beginner-to-expert essential notes

JavaScript is the language that changes a page and handles data. It is dynamically typed: a variable can hold values of different types, so write clear checks at boundaries.

## 1. Values, variables, equality, and coercion

Use `const` by default. Use `let` only when the binding changes. Do not use `var` in new code: it is function-scoped and hoisted in surprising ways.

```js
const user = { name: "Asha" };
let count = 0;
count += 1;
```

Primitive values: `string`, `number`, `bigint`, `boolean`, `undefined`, `symbol`, `null`. Objects, arrays, and functions are reference values.

Use strict equality: `===` and `!==`. Loose equality (`==`) converts types, e.g. `0 == false` is true; avoid it.

`null` intentionally means “no value”; `undefined` usually means “not assigned/not found.” `typeof null` is historically `"object"`, so test it with `value === null`.

Falsy values are `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, and `NaN`; all other values, including `[]` and `{}`, are truthy. `??` uses its right side only for `null`/`undefined`; `||` uses it for any falsy value.

```js
const quantity = inputQuantity ?? 1;
const city = user.address?.city;
```

`Number.isNaN(value)` checks the special invalid number safely. Explicit conversion (`Number(text)`, `String(value)`) is clearer than accidental coercion.

## 2. Control flow, objects, arrays, Map, and Set

```js
const person = { name: "Asha", city: "Pune" };
const { name } = person;
const updated = { ...person, city: "Delhi" };

const numbers = [1, 2, 3];
const doubled = numbers.map((number) => number * 2);
const even = numbers.filter((number) => number % 2 === 0);
const total = numbers.reduce((sum, number) => sum + number, 0);
```

- Spread creates a shallow copy. Nested objects are still shared.
- `map` transforms every item and returns a new array.
- `filter` keeps matching items and returns a new array.
- `find` returns the first match (or `undefined`); `some` checks if any match; `every` checks all.
- `forEach` is for side effects and returns `undefined`.
- `sort()` mutates and sorts as strings by default. For numbers use `items.toSorted((a, b) => a - b)` or `[...items].sort(...)`.

Use early returns to keep branches shallow. `for...of` iterates iterable values; `for...in` iterates enumerable property keys and is rarely right for arrays.

`Map` stores key/value pairs with keys of any type. `Set` stores unique values. They are often clearer than plain objects for dynamic collections.

```js
const visits = new Map([["home", 2]]);
visits.set("about", 1);
const uniqueTags = [...new Set(["js", "css", "js"])];
```

`JSON.stringify` serializes supported JavaScript data; `JSON.parse` reads JSON. JSON cannot represent functions, `undefined`, `BigInt`, cycles, or Map/Set directly.

## 3. Functions, scope, closures, and `this`

Functions are values: pass them, return them, and store them.

```js
function createCounter() {
  let count = 0;
  return () => ++count;
}

const nextCount = createCounter();
nextCount(); // 1
```

A **closure** is a function that remembers variables from where it was created. It powers private state, callbacks, and event handlers.

`let` and `const` are block-scoped. JavaScript hoists declarations, but `let`/`const` cannot be read before initialization (the temporal dead zone).

`this` depends on how a normal function is called. Arrow functions do not create their own `this`; they capture the surrounding one. Do not use an arrow for an object method that needs dynamic `this`.

```js
const user = {
  name: "Asha",
  greet() { return this.name; },
};
```

Function declarations are callable before their source line. Function expressions are not usable until their variable initializes. `call`, `apply`, and `bind` control `this`; `bind` returns a new function.

## 4. Prototypes, classes, and modules

Objects inherit through a prototype chain. Property lookup checks the object, then its prototype, until `null`. JavaScript `class` is clearer syntax over this prototype system.

```js
class Account {
  #balance = 0;

  deposit(amount) {
    if (amount <= 0) throw new RangeError("Amount must be positive");
    this.#balance += amount;
  }

  get balance() { return this.#balance; }
}
```

Prefer composition for sharing behavior. Private fields beginning with `#` are enforced at runtime.

ES modules have explicit dependencies:

```js
export function add(a, b) { return a + b; }
// another file: import { add } from "./math.js";
```

Named exports make dependencies easy to find. Modules are strict mode, have their own scope, and load once.

## 5. Async JavaScript and event loop

JavaScript runs synchronous code on one call stack. Browser APIs handle timers/network work. Completed work queues callbacks:

```text
call stack finishes
        ↓
drain all microtasks (Promise callbacks)
        ↓
run one task (timer/input) → browser may render → repeat
```

- **Microtasks**: promise handlers and `queueMicrotask`; run after current code, before the next task.
- **Tasks**: timers, input, and many browser events.

```js
console.log("start");
Promise.resolve().then(() => console.log("promise"));
setTimeout(() => console.log("timer"), 0);
console.log("end");
// start, end, promise, timer
```

`async` functions always return a Promise. `await` pauses only that async function; it does not block the whole page.

```js
async function loadUser(id) {
  const response = await fetch(`/api/users/${encodeURIComponent(id)}`);
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json();
}
```

`fetch` rejects for network failures, not HTTP 404/500, so check `response.ok`. Run independent requests together with `Promise.all`; it rejects if one fails. Use `Promise.allSettled` when every result matters.

Use `AbortController` to cancel obsolete fetches. Do not use `array.forEach(async ...)` when you need to wait; use `for...of` for sequential work or `Promise.all(items.map(...))` for parallel work.

## 6. DOM and events

```js
const button = document.querySelector("#save");
if (!button) throw new Error("Save button not found");

button.addEventListener("click", (event) => {
  event.preventDefault();
});
```

Events travel down (capture), reach target, then travel up (**bubble**). Event delegation puts one listener on a parent and checks `event.target`, useful for dynamic lists. `preventDefault()` stops the browser’s default action; `stopPropagation()` stops event travel and should be rare.

Avoid putting untrusted strings in `innerHTML`; use `textContent` or safe DOM APIs to prevent XSS.

Delegation example:

```js
list.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-id]");
  if (!button || !list.contains(button)) return;
  removeItem(button.dataset.id);
});
```

## 7. Errors, debugging, and cleanup

Throw an appropriate `Error`, `TypeError`, or `RangeError` when a function cannot meet its contract. Catch an error only when you can recover, add useful context, or clean up; otherwise let it propagate. `finally` always runs.

Use DevTools breakpoints, the console, Network panel, and Performance panel. Remove event listeners, observers, intervals, and subscriptions when their owner is destroyed to prevent leaks.

## 8. Browser storage and security

- `localStorage`: persistent string key/value data, synchronous, available to same-origin scripts.
- `sessionStorage`: like local storage but scoped to a browser tab/session.
- Cookies: small values sent with matching HTTP requests; authentication cookies should use `HttpOnly`, `Secure`, and suitable `SameSite` attributes.
- IndexedDB: asynchronous structured client-side database.

Do not store secrets in browser code or local storage. Prevent XSS by treating all external text as untrusted, avoiding unsafe HTML insertion, and using a Content Security Policy. Prevent prototype pollution by validating keys before merging untrusted objects.

## 9. Performance mental model

Measure first. Avoid blocking the main thread with long tasks; split heavy work or use a Web Worker. Batch DOM reads/writes, debounce noisy input such as search, and throttle continuous events such as scroll. Use memoization only for repeated expensive pure work.

## 10. Common interview pitfalls

- Shallow copy mistaken for a deep copy.
- Losing `this` by passing a method as a callback.
- Promise errors not awaited or returned.
- `sort()` mutating the original array.
- Floating-point surprises such as `0.1 + 0.2 !== 0.3`.
- Closures keeping large objects alive longer than needed.

## Interview checklist

Know `var`/`let`/`const`, primitive vs reference values, `===`, scope/hoisting/closure, arrow vs normal functions, `this`, array methods, promises/async-await/event loop, fetch error handling, and event bubbling/delegation.
