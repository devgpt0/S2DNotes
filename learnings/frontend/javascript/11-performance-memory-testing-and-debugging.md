# 11 - JavaScript Performance, Memory, Testing, and Debugging

## Main Thread and Long Tasks

JavaScript, style, layout, and paint often share the main thread. Long synchronous work delays input and rendering.

```javascript
const started = performance.now();
const result = Array.from({ length: 100_000 }, (_, index) => index).reduce((a, b) => a + b, 0);
console.log(result, performance.now() >= started);
// Console output: 4999950000 true
```

Profile before optimizing. Move truly heavy pure computation to a worker or split work when it improves responsiveness.

## Rendering Work

- batch DOM reads then writes
- use CSS classes for visual states
- debounce expensive input-driven queries
- throttle high-frequency visual work with animation frames when appropriate
- virtualize very long lists
- avoid large DOM and repeated forced layout

## Memory Leaks

Common causes: unremoved listeners, timers, detached DOM retained by closures, unbounded caches, subscriptions, and unresolved application lifecycles.

```javascript
const controller = new AbortController();
window.addEventListener("resize", handleResize, { signal: controller.signal });
controller.abort();
console.log(controller.signal.aborted);
// Console output: true; the signal-bound listener is removed.
```

## Testing Levels

- unit: pure functions and state rules
- component/DOM: rendered behavior and accessibility
- integration: modules with real/test infrastructure
- end-to-end: critical journeys in a real browser
- visual regression: intentional appearance changes
- performance/accessibility: budgets and audits plus human testing

```javascript
import { test, expect } from "vitest";
test("adds prices", () => {
  expect([10, 20].reduce((a, b) => a + b, 0)).toBe(30);
});
// Test output: passes with total 30.
```

## Debugging Workflow

1. Reproduce reliably.
2. Read console error and complete stack.
3. Reduce to the smallest failing input.
4. Use breakpoints/watch values, not many permanent logs.
5. Inspect Network request/response/timing.
6. Confirm DOM and computed CSS.
7. Write a failing test.
8. Fix root cause and verify related cases.

## Performance Metrics

Measure Core Web Vitals, JavaScript bundle/parse/execute cost, long tasks, memory, API latency, cache behavior, and user journeys on representative mobile hardware.
