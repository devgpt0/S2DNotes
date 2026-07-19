# JavaScript Expert Tips, Tricks, and Browser Patterns

## Language Discipline

- Use `const` by default and `let` only for intentional reassignment.
- Prefer strict equality and explicit conversion at boundaries.
- Model absence deliberately; do not mix null, undefined, empty string, and zero without a contract.
- Use optional chaining only for legitimately optional paths, not to hide corrupt required data.
- Keep functions small, pure where possible, and explicit about side effects.
- Avoid parameter mutation and shared mutable module state.
- Prefer discriminated state objects over several booleans that can form impossible combinations.
- Use Map/Set when their key/uniqueness semantics fit better than plain objects/arrays.

## Async Expert Habits

- Start independent promises together; await them together.
- Put a deadline/cancellation signal on network and long-lived async work.
- Check `response.ok`, content type, size, and runtime schema.
- Distinguish network failure, timeout, HTTP failure, invalid data, and cancellation.
- Never retry non-idempotent work without an idempotency contract.
- Avoid floating promises; every rejection needs an owner.
- Do not use `forEach(async ...)` when completion matters; use `for...of` or `Promise.all` intentionally.
- Prevent stale responses from overwriting newer UI state.
- Clean up timers, listeners, observers, workers, sockets, and subscriptions.

## DOM and Rendering

- Use `textContent` for untrusted text and safe DOM construction for structure.
- Prefer event delegation for repeated/dynamic children.
- Batch layout reads before writes.
- Use classes/data/state rather than many direct style mutations.
- Keep DOM order semantic and focus movement intentional.
- Use AbortSignal-bound listeners for easy lifecycle cleanup.
- Use Intersection/Resize/Mutation observers instead of polling where appropriate.
- Move CPU-heavy pure work to a Worker only after profiling.

## Performance

- Optimize shipped/parsed/executed code before micro-syntax.
- Split by real route/interaction boundaries, not every component.
- Measure long tasks, INP, memory, rendering, and network on mid/low mobile hardware.
- Debounce request-like input work; throttle visual work to suitable cadence.
- Virtualize only genuinely large visible collections.
- Bound caches and remove retained closures/listeners.
- Avoid JSON stringify/parse as a general deep-clone strategy.
- Prefer algorithm/data-structure improvement over tiny loop tricks.

## Security

- Treat URL, DOM, storage, message, worker, API, and third-party data as untrusted.
- Never use `eval`, `new Function`, or string-to-script behavior.
- Validate URL schemes/hosts before navigation or fetch.
- Avoid prototype-pollution-prone deep merges.
- Keep tokens/secrets out of JavaScript-readable storage when secure HttpOnly sessions fit.
- Use CSP, Trusted Types where appropriate, and contextual output encoding.
- Third-party scripts receive powerful page access; minimize and govern them.

## Module and API Design

- Export the smallest stable API.
- Keep domain logic independent from DOM/network/storage adapters.
- Inject time, randomness, clients, and storage for deterministic tests.
- Avoid circular imports and side effects during module evaluation.
- Use named errors/results for expected failure categories.
- Document ownership: who creates, starts, cancels, and disposes a resource.

## Debugging Tricks

- Preserve logs in Network/Console only when navigation is involved.
- Use conditional DOM/XHR/fetch breakpoints.
- Inspect async stack traces and request initiators.
- Use Performance marks/measures for application-specific timings.
- Take heap snapshots and compare retained paths, not total allocation alone.
- Reproduce with cache disabled and CPU/network throttling.
- Write the failing test before refactoring the fix.

## Interview Traps Experts Explain

Hoisting/TDZ, closure in loops, `this` call site, microtask vs task order, shallow copy, equality/coercion, mutation vs reassignment, fetch HTTP behavior, module live bindings, prototype chain, event propagation, memory leaks, and race/cancellation behavior.

## Expert Code Snippets Used in Production

### Latest-Request-Wins Fetch

```javascript
let currentController;
async function search(query) {
  currentController?.abort();
  currentController = new AbortController();
  const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`, { signal: currentController.signal });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  console.log(data);
}
// Behavior: starting a newer search aborts the previous request so stale results cannot overwrite current UI.
```

### Disposable Event Lifecycle

```javascript
const lifecycle = new AbortController();
window.addEventListener("resize", handleResize, { signal: lifecycle.signal, passive: true });
button.addEventListener("click", handleClick, { signal: lifecycle.signal });
lifecycle.abort();
console.log(lifecycle.signal.aborted);
// Console output: true; both listeners are removed through one lifecycle signal.
```

### Runtime Boundary Parser

```javascript
function parseCourse(value) {
  if (typeof value !== "object" || value === null) throw new TypeError("course must be an object");
  if (typeof value.id !== "string" || typeof value.title !== "string") throw new TypeError("invalid course fields");
  return Object.freeze({ id: value.id, title: value.title });
}
console.log(parseCourse({ id: "html", title: "HTML" }));
// Console output: {id: "html", title: "HTML"} (console formatting varies).
```

### Batch DOM Read and Write

```javascript
const widths = cards.map(card => card.getBoundingClientRect().width);
requestAnimationFrame(() => cards.forEach((card, index) => card.style.setProperty("--measured-width", `${widths[index]}px`)));
console.log(widths.length);
// Console output: number of measured cards; reads occur before deferred writes to reduce layout thrashing.
```

### Bounded Memoization

```javascript
function memoizeOne(fn) {
  let hasValue = false, previousArgument, previousResult;
  return argument => {
    if (hasValue && Object.is(argument, previousArgument)) return previousResult;
    hasValue = true; previousArgument = argument; previousResult = fn(argument);
    return previousResult;
  };
}
const square = memoizeOne(value => value * value);
console.log(square(4), square(4));
// Console output: 16 16; cache remains bounded to one argument/result.
```
