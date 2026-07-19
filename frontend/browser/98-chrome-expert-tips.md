# 98 - Chrome Expert Tools and Production Checklist

## Expert Mindset

- reproduce the user's condition before interpreting a trace
- separate network, server, main thread, GPU, memory, and third-party work
- prefer removing work over scheduling tricks
- compare the same interaction and environment
- sanitize raw evidence before sharing it
- use field telemetry to confirm production impact

## Fast Panel Selection

| Question | Start here |
|---|---|
| Why did this CSS lose? | Elements > Styles and Computed |
| What is covering the button? | Elements, stacking contexts, event listeners |
| Who started this request? | Network > Initiator |
| Why is the click slow? | Performance interaction trace |
| Why does memory grow? | Memory snapshots and retaining paths |
| Is a service worker involved? | Application > Service Workers and Cache Storage |
| Which code is unused in this flow? | Coverage |
| Is the connection secure? | Security and Issues |
| Is graphics acceleration available? | `chrome://gpu` |

## Ignore Third-Party Noise Carefully

Performance supports ignore-listing scripts. Use it to make call trees readable, but keep a second view that includes third-party work. A tag, chat widget, or analytics script still consumes the user's CPU.

## Network Request Blocking

Use request blocking to test a hypothesis such as: “Does this third-party script cause the delay?”

Blocking is an experiment, not a shipping fix. Confirm product and dependency behavior before removing a resource.

## Local Overrides

Overrides can replace a response locally to test a CSS or JavaScript change against a remote environment.

- never confuse a local override with deployed code
- document every overridden file
- clear overrides after the experiment
- reproduce the result from the real source/build before closing the issue

## Performance Monitor

Open the Command Menu and show Performance Monitor for a live view of CPU, DOM nodes, listeners, layout, and memory while repeating an action.

Use it to spot a trend, then use a trace or heap snapshot to prove the cause.

## Coverage

Coverage reports CSS and JavaScript used during the recorded flow.

Limitations:

- one flow does not represent the whole product
- lazy features correctly appear unused before activation
- dynamic selectors and error states may not execute
- removing code requires source and product knowledge

Use coverage as a question generator, not an automatic deletion list.

## PerformanceObserver Snippets

Observe long tasks in a supported Chromium environment:

```javascript
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log("Long task", entry.startTime, entry.duration);
  }
});
observer.observe({ type: "longtask", buffered: true });
// Call observer.disconnect() when the diagnostic owner is removed.
```

Observe diagnostic layout shifts without recent input:

```javascript
let cumulativeShift = 0;
const shiftObserver = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!("hadRecentInput" in entry) || entry.hadRecentInput) continue;
    if (!("value" in entry) || typeof entry.value !== "number") continue;
    cumulativeShift += entry.value;
    console.log("Diagnostic layout shift total", cumulativeShift);
  }
});
shiftObserver.observe({ type: "layout-shift", buffered: true });
```

Production Core Web Vitals calculation has session and attribution rules. Use a maintained web-vitals implementation instead of treating these learning snippets as a complete analytics pipeline.

## React and Framework Diagnosis

Use framework tools and Chrome together:

1. framework profiler identifies component work
2. Chrome Performance shows main-thread and browser rendering cost
3. Network shows data and chunk timing
4. field data shows whether real users experience the problem

A component render is not automatically a performance problem. Measure its time and resulting work.

## Layout and Rendering Tips

- use `content-visibility: auto` only after testing find-in-page, focus, printing, and intrinsic-size behavior
- animate transforms and opacity when they match the visual requirement
- do not add `will-change` globally
- use containment only when the component truly isolates work
- avoid reading geometry immediately after writes in repeated loops
- test zoom, text enlargement, RTL, dark mode, reduced motion, and forced colors

## Network and Loading Tips

- make critical resources discoverable in initial HTML
- avoid request waterfalls created by client-only discovery
- use responsive images with dimensions
- cache hashed static assets for a long time
- keep HTML/API policies aligned with freshness and privacy
- preconnect or preload only measured important origins/resources
- remove unused third parties before micro-optimizing first-party code

## Memory Tips

- every listener, timer, observer, worker, and subscription needs an owner and cleanup rule
- cache size and lifetime must be bounded
- avoid retaining DOM nodes in module-level structures
- compare heap snapshots using retaining paths, not object count alone
- repeat the exact action cycle when verifying a leak fix

## Chrome Task Manager

Open Chrome Task Manager with `Shift+Esc` to compare tab/process CPU, memory, and network use. It helps identify which tab or extension is expensive; DevTools then explains why.

## Production Performance Checklist

- real-user LCP, INP, and CLS tracked at a named percentile
- representative lab profiles documented
- before/after traces attached to material optimizations
- route budgets for JavaScript, images, fonts, and requests
- long tasks and third-party cost reviewed
- images have responsive sources and dimensions
- critical resources are discovered early
- caches match versioning, privacy, and freshness needs
- loading, error, empty, offline, and retry states tested
- memory stable after repeated navigation or action cycles
- keyboard, screen reader, zoom, reduced motion, and contrast verified
- traces, HARs, screenshots, and exports sanitized before sharing

## Final Rule

A strong diagnostic statement connects symptom to evidence:

> The save interaction is delayed because a 240 ms synchronous transformation runs on the main thread before the next paint. Moving that pure transformation to a worker reduced the measured delay under the same 4x CPU profile, while validation and error behavior remained unchanged.

That statement names the symptom, cause, evidence, change, environment, and correctness check.
