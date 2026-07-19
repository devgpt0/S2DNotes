# 06 - Event Loop, Promises, Async/Await, Fetch, and Cancellation

## Synchronous First

JavaScript runs one call stack per agent. Browser APIs can complete work later and queue callbacks/jobs.

```javascript
console.log("A");
setTimeout(() => console.log("timer"), 0);
Promise.resolve().then(() => console.log("promise"));
console.log("B");
// Console output:
// A
// B
// promise
// timer
```

Promise reactions (microtasks) run after the current stack and before the next timer task.

## Promise States

A Promise is pending, fulfilled, or rejected.

```javascript
const promise = Promise.resolve(42);
promise.then(value => console.log(value));
// Console output: 42
```

Returning a promise from `then` chains it. Throwing rejects the chain.

## Async/Await

```javascript
const answer = async () => {
  const value = await Promise.resolve(42);
  return value;
};
console.log(await answer());
// Module console output: 42
```

An async function always returns a Promise. `await` pauses that async function, not the whole browser.

## Sequential vs Parallel

```javascript
const [user, courses] = await Promise.all([
  Promise.resolve("Asha"),
  Promise.resolve(["HTML", "CSS"]),
]);
console.log(user, courses);
// Module console output: Asha ["HTML", "CSS"]
```

Start independent operations together. Use `allSettled` when every outcome is needed; `race`/`any` have different success/failure rules.

## Fetch

```javascript
const response = await fetch("/api/courses", { headers: { Accept: "application/json" } });
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const courses = await response.json();
console.log(Array.isArray(courses));
// Console output on a valid array response: true
```

Fetch rejects on network failure, not ordinary HTTP 404/500, so check `response.ok`. Validate response data.

## Cancellation and Timeout

```javascript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 3000);
try {
  const response = await fetch("/api/courses", { signal: controller.signal });
  console.log(response.status);
} finally {
  clearTimeout(timeout);
}
// Console output: HTTP status if completed within 3 seconds; otherwise fetch rejects with an abort error.
```

## Common Mistakes

- forgetting `await` and using a Promise as data
- `await` inside a loop when work is independent
- unhandled rejection
- no deadline/cancellation
- retrying unsafe requests
- updating UI after a component/page state is obsolete
