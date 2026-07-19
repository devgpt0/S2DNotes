# 02 - A Repeatable Chrome DevTools Diagnostic Workflow

## The Goal

DevTools contains many panels. Diagnosis becomes easier when you follow the same order instead of clicking randomly.

```text
Define -> Reproduce -> Preserve evidence -> Narrow the layer -> Prove the cause -> Verify the fix
```

## Step 1: Define the Problem Precisely

Weak report:

> The page is slow.

Useful report:

> On a 4x CPU slowdown and Fast 4G, clicking “Show courses” takes about 900 ms before the first row appears. It reproduces after a clean reload in Chrome stable with extensions disabled.

Record:

- exact URL and environment
- viewport, zoom, input method, and theme
- signed-in or data state
- network and CPU conditions
- expected behavior
- actual behavior
- repeatable steps

## Step 2: Reproduce Cleanly

1. Use a clean profile or Incognito when extensions may interfere.
2. Open DevTools before the action.
3. In Network, enable Preserve log if navigation is involved.
4. Disable cache only when testing an uncached load; the checkbox applies while DevTools is open.
5. Repeat at least three times and note variation.

Do not assume Incognito means “no cache” for every diagnostic situation. Set the condition you intend to test.

## Step 3: Check the Console

Look for the first relevant error, not the largest number of follow-on errors.

Useful Console tools:

```javascript
console.table(data);
console.time("course-render");
renderCourses();
console.timeEnd("course-render");
```

Use temporary measurement locally. Remove noisy production logging and never log secrets or personal data.

Enable Pause on exceptions in Sources when a caught exception hides the original failing line.

## Step 4: Inspect the DOM and CSS

Use Elements when the problem is visual, semantic, responsive, or state-related.

Check:

- is the expected element present?
- is the content correct?
- which CSS rule is crossed out, inherited, or overridden?
- what is the computed size, display, position, overflow, and z-index?
- does a parent create a containing block, clipping area, or stacking context?
- does the Accessibility pane show the expected role and name?

Useful interactions:

- force `:hover`, `:focus`, `:focus-visible`, or `:disabled`
- edit a declaration live to test one hypothesis
- inspect Grid and Flex overlays
- use the Layout pane for grids and container queries

A successful live edit is evidence, not the final source fix. Change the real stylesheet and retest.

## Step 5: Inspect Network Requests

Filter by Fetch/XHR, JS, CSS, Img, Font, or a URL fragment.

For a failed or slow request, check:

- URL and method
- status code
- request payload and headers
- response headers and body
- Initiator: what caused the request
- Timing: queueing, connection, request, and waiting phases
- Size: transferred vs decoded resource size
- cache source

Common conclusions:

| Evidence | Likely area |
|---|---|
| long server wait | backend, database, upstream service, or edge path |
| many sequential requests | client request waterfall or API design |
| large decoded image | image sizing/format/content pipeline |
| request blocked by CORS | server response policy and request shape |
| memory cache or disk cache | browser cache reuse |
| service worker source | service-worker fetch/cache logic |

Copy as cURL only after removing cookies, authorization headers, tokens, and sensitive payloads before sharing it.

## Step 6: Debug JavaScript in Sources

Use a breakpoint close to the incorrect state.

Then inspect:

- Scope: local, closure, and global values
- Call Stack: how execution reached this line
- Watch: important expressions
- Event Listener Breakpoints: who handles click, input, timer, or network events
- XHR/fetch breakpoints: which code starts a matching request

Conditional breakpoint example:

```javascript
course.id === "course-42"
```

Logpoints can observe a value without editing source, but avoid heavy logging in a hot loop.

## Step 7: Choose the Correct Performance Tool

- slow load or interaction: Performance panel
- slow request: Network timing and server telemetry
- growing memory: Memory panel and Performance memory counters
- unused JavaScript/CSS: Coverage
- layout/paint suspicion: Rendering panel
- broad lab audit: Lighthouse
- real-user regression: field telemetry and Chrome UX Report where available

Lighthouse suggestions are leads, not proof of the root cause.

## Step 8: Form One Testable Hypothesis

Example:

> A 280 ms click delay is caused by synchronous filtering and DOM creation of 10,000 rows on the main thread.

Evidence needed:

- click event in the Performance trace
- long JavaScript task before the next paint
- call tree points to filtering/rendering functions
- reducing row count removes the delay

## Step 9: Change One Thing and Compare

Capture a before trace. Make one change. Capture an after trace under the same conditions.

Compare:

- user-visible timing
- main-thread work
- request count and bytes
- layout shifts
- memory after repeated actions
- correctness and accessibility

An improvement that breaks keyboard focus or stale-data handling is not complete.

## Useful Rendering Panel Checks

Open the Command Menu with `Ctrl+Shift+P`, type “Show Rendering,” then try:

- Paint flashing
- Layout Shift Regions
- FPS meter
- Scrolling performance issues
- emulated CSS media features

Turn overlays off after the test so they do not confuse later recordings.

## Diagnostic Handoff Template

```text
Problem:
Environment:
Steps:
Expected:
Actual:
Evidence:
Root cause:
Change:
Before/after measurement:
Remaining risk:
```

## Quick Check

If a button appears but cannot be clicked, do not immediately change `z-index`. Inspect the element under the pointer, stacking contexts, overlays, `pointer-events`, disabled/inert state, and event listeners. The evidence tells you which layer owns the bug.
