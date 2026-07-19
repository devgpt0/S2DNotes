# 14 - Web Concurrency, Streams, Workers, and Realtime APIs

## JavaScript Concurrency Mental Model

Browser JavaScript normally runs one task at a time on an agent's call stack. Browser services perform work such as networking and timers, then schedule callbacks.

```javascript
console.log("script start");
setTimeout(() => console.log("timer task"), 0);
queueMicrotask(() => console.log("microtask"));
console.log("script end");
// Output:
// script start
// script end
// microtask
// timer task
```

Microtasks run after the current task finishes and before the browser takes the next task. An endless microtask chain can delay rendering just like one long task.

## Rendering Opportunity

A simplified loop is:

```text
run one task -> drain microtasks -> browser may render -> next task
```

The browser may skip rendering when nothing changed or scheduling conditions differ. Do not depend on a paint after every task.

## `requestAnimationFrame`

Use it for visual work that should run before a frame:

```javascript
const box = document.querySelector("#box");
if (!(box instanceof HTMLElement)) throw new Error("box is missing");

requestAnimationFrame(() => {
  box.style.transform = "translateX(100px)";
});
```

It is not a general background scheduler. Callbacks pause or throttle in hidden tabs.

## `requestIdleCallback`

Idle callbacks can run low-priority optional work when the browser has idle time, but support and timing are not universal. Never put required correctness, saving, or user feedback only in an idle callback.

## Promises Do Not Create Threads

```javascript
const calculate = async () => {
  let total = 0;
  for (let index = 0; index < 100_000_000; index += 1) total += index;
  return total;
};
```

Marking CPU-heavy work `async` does not move it off the main thread. The loop still blocks until it reaches an actual asynchronous boundary.

## Independent vs Dependent Async Work

Independent requests can start together:

```javascript
const loadDashboard = async () => {
  const [profileResponse, coursesResponse] = await Promise.all([
    fetch("/api/profile"),
    fetch("/api/courses"),
  ]);
  if (!profileResponse.ok || !coursesResponse.ok) {
    throw new Error("dashboard request failed");
  }
  return Promise.all([profileResponse.json(), coursesResponse.json()]);
};
```

Dependent work must remain ordered. Do not parallelize a request that requires an ID from an earlier response.

## Cancellation with `AbortController`

```javascript
const loadCourses = async (signal) => {
  const response = await fetch("/api/courses", { signal });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
};

const controller = new AbortController();
const promise = loadCourses(controller.signal);
controller.abort("view closed");

try {
  await promise;
} catch (error) {
  if (error instanceof DOMException && error.name === "AbortError") {
    console.log("Request cancelled");
  } else {
    throw error;
  }
}
// Output: Request cancelled
```

Cancellation is part of the operation contract. The server may still receive or process a request, so abort is not transaction rollback.

## Timeouts

Where supported by the compatibility policy:

```javascript
const response = await fetch("/api/courses", {
  signal: AbortSignal.timeout(5_000),
});
```

Otherwise combine a controller and timer, clearing the timer in `finally`.

## Fetch Response Streams

Large responses can be processed incrementally:

```javascript
const response = await fetch("/api/report.txt");
if (!response.ok || response.body === null) {
  throw new Error(`report unavailable: HTTP ${response.status}`);
}

const reader = response.body
  .pipeThrough(new TextDecoderStream())
  .getReader();

let text = "";
try {
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    text += value;
  }
} finally {
  reader.releaseLock();
}
console.log(text.length);
// Output: number of decoded characters.
```

Incremental processing helps memory and progressive UI only when the data format and application can consume partial chunks safely.

## Backpressure in Streams

Web Streams communicate how quickly consumers can accept data. A `ReadableStream`, `WritableStream`, or `TransformStream` can avoid producing an unlimited in-memory queue.

```javascript
const uppercase = new TransformStream({
  transform(chunk, controller) {
    controller.enqueue(String(chunk).toUpperCase());
  },
});
```

Transform callbacks use method syntax because the stream strategy object calls them as methods; no lexical `this` is needed, but this is the platform's expected object shape.

## Web Workers

Use a Worker for measured CPU-heavy JavaScript that does not need direct DOM access.

```javascript
// worker.js
self.addEventListener("message", (event) => {
  const values = event.data;
  if (!Array.isArray(values) || !values.every(Number.isFinite)) {
    throw new TypeError("worker expects finite numbers");
  }
  const total = values.reduce((sum, value) => sum + value, 0);
  self.postMessage(total);
});
```

```javascript
// app.js
const worker = new Worker(new URL("./worker.js", import.meta.url), { type: "module" });
worker.addEventListener("message", (event) => console.log(event.data));
worker.postMessage([10, 20, 30]);
// Console output: 60
```

Messages are cloned unless transferable objects are used. Validate worker messages; they are runtime data.

Terminate workers when their owner is removed:

```javascript
const dispose = () => worker.terminate();
```

## Transferable Objects

Large `ArrayBuffer` data can be transferred without copying:

```javascript
const buffer = new ArrayBuffer(1_024);
worker.postMessage(buffer, [buffer]);
console.log(buffer.byteLength);
// Output: 0 because ownership moved to the worker.
```

Transfer means the sender can no longer use that buffer.

## Shared Workers and Shared Memory

SharedWorker can serve multiple same-origin browsing contexts, but lifecycle and support need careful testing.

`SharedArrayBuffer` and `Atomics` enable shared memory and require cross-origin isolation/security headers. They are low-level tools for specialized workloads, not ordinary state management.

## Server-Sent Events

SSE is server-to-browser text event streaming over HTTP:

```javascript
const events = new EventSource("/api/course-events");
events.addEventListener("course-updated", (event) => {
  console.log(JSON.parse(event.data));
});
events.addEventListener("error", () => console.log("event stream interrupted"));

const dispose = () => events.close();
```

Use it for one-way live updates when automatic reconnection and HTTP infrastructure are a good fit. Validate every message.

## WebSocket

WebSocket provides full-duplex messages:

```javascript
const socket = new WebSocket("wss://example.com/courses");
socket.addEventListener("open", () => socket.send(JSON.stringify({ type: "subscribe" })));
socket.addEventListener("message", (event) => console.log(event.data));
socket.addEventListener("close", () => console.log("socket closed"));
```

Production design must define authentication, reconnect backoff, heartbeats, message validation, ordering, duplicate handling, backpressure, and cleanup.

## Choose the Right Tool

| Need | Start with |
|---|---|
| ordinary request/response | Fetch |
| incremental response body | Fetch + ReadableStream |
| CPU work away from UI | Worker |
| one-way server updates | SSE |
| two-way live messaging | WebSocket |
| visual frame update | requestAnimationFrame |
| optional idle work | requestIdleCallback with fallback/policy |

## Expert Rules

- async syntax does not create parallel CPU execution
- every async resource needs cancellation and ownership
- retries require idempotency, bounds, and backoff
- streams need error, cancellation, and backpressure handling
- workers trade main-thread time for messaging, cloning, memory, and complexity
- realtime transports need protocol design, not only connection code

## Final Rule

Choose concurrency from the workload and lifecycle. Measure main-thread blocking before adding a Worker, and define cleanup before opening a long-lived resource.
