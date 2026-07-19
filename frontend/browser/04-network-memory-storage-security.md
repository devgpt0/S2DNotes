# 04 - Network, Memory, Storage, and Security Diagnosis

## Network Diagnosis

### Read the Waterfall Left to Right

The waterfall answers:

- when was a request discovered?
- did it wait in a queue?
- did it create or reuse a connection?
- how long did the server take to start responding?
- how long did content download?
- which earlier request or script initiated it?

A late-starting request can be more important than a slowly downloading one.

### Cache Headers

Important response headers include:

- `Cache-Control`
- `ETag`
- `Last-Modified`
- `Vary`
- `Age`

Hashed static assets can usually use long-lived immutable caching. HTML and API data need policies matching how they change and who may see them.

Never cache private user data in a shared cache without a proven safe policy.

### Request Priority and Preloading

Preload is powerful and easy to misuse:

```html
<link rel="preload" href="/fonts/course.woff2" as="font" type="font/woff2" crossorigin>
```

The URL, credentials mode, `as`, and type must match the later request or the browser may fetch twice. Preload only resources required for the current view.

### Service Workers

In Application > Service Workers:

- verify which worker controls the page
- inspect update and activation state
- test bypassing the worker
- inspect Cache Storage entries
- verify offline and stale-data behavior

“It works after unregistering the service worker” is evidence that fetch or update logic needs investigation, not a production fix.

## Memory in Simple Words

JavaScript objects remain in memory while something reachable still refers to them. Garbage collection can reclaim unreachable objects.

A memory leak is retained memory the application no longer needs.

Common causes:

- listeners not removed
- timers not cleared
- caches that grow without a bound
- detached DOM nodes still referenced
- closures retaining large objects
- subscriptions not cancelled

## Memory Diagnostic Workflow

1. Open a stable page and let startup settle.
2. Perform the suspected action several times.
3. Return to the original state each time.
4. Observe memory counters in Performance.
5. Take heap snapshots before and after repeated cycles.
6. Compare retained objects and paths to GC roots.
7. Fix the ownership or cleanup rule.
8. repeat the same cycle and compare again.

Heap size naturally moves. One high number is not proof of a leak.

## Lifecycle-Safe Listener Pattern

```javascript
export function mountSearch(form, onSearch) {
  if (!(form instanceof HTMLFormElement)) throw new TypeError("form is required");
  if (typeof onSearch !== "function") throw new TypeError("onSearch must be a function");

  const controller = new AbortController();
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const query = new FormData(form).get("query");
    if (typeof query !== "string") throw new TypeError("query field is missing");
    onSearch(query);
  }, { signal: controller.signal });

  return () => controller.abort();
}
```

The owner receives one cleanup function that releases every listener using the signal.

## Bounded Cache Pattern

```javascript
class ResultCache {
  #values = new Map();
  constructor(limit = 100) {
    if (!Number.isSafeInteger(limit) || limit <= 0) throw new RangeError("limit must be positive");
    this.limit = limit;
  }
  get(key) { return this.#values.get(key); }
  set(key, value) {
    if (this.#values.has(key)) this.#values.delete(key);
    this.#values.set(key, value);
    if (this.#values.size > this.limit) {
      const oldest = this.#values.keys().next().value;
      if (oldest === undefined) throw new Error("cache eviction key is missing");
      this.#values.delete(oldest);
    }
  }
}
```

The policy is simple least-recently-inserted/updated behavior. Use a proven cache when requirements include size weighting, expiry, concurrency, or persistence.

## Storage Diagnosis

Application panel areas include:

- local and session storage
- IndexedDB
- cookies
- Cache Storage
- service workers
- storage usage

Treat every stored value as untrusted when reading it back. Users, extensions, old versions, and partial migrations can change it.

Do not store authentication secrets in local storage. JavaScript-readable storage is exposed to successful XSS.

## Cookie Checks

Inspect:

- `Secure`
- `HttpOnly`
- `SameSite`
- domain and path scope
- expiry
- partitioning behavior where relevant

Client JavaScript cannot inspect `HttpOnly` cookies by design.

## Security and Issues Panels

Use Security to inspect connection security and certificate information. Use Issues to find browser-detected problems such as cookie, mixed-content, CORS, or deprecation concerns.

DevTools warnings are not a complete security review.

## CORS in Plain Language

CORS is a browser rule controlling whether frontend JavaScript may read a cross-origin response.

It is not authentication and does not stop non-browser clients from sending requests.

Fix CORS on the server or gateway that owns response policy. Do not use `mode: "no-cors"` to “fix” an API response; it produces an opaque response JavaScript cannot read.

## Content Security Policy

CSP limits which resources and scripts the page may run. It reduces the impact of some injection bugs but does not replace output safety and validation.

Use report-only deployment to understand violations, then enforce a policy based on nonces or hashes where appropriate. Avoid weakening the policy with broad unsafe sources merely to silence errors.

## Useful Chrome Internal Pages

Open these manually and share exports carefully because they may contain sensitive environment data:

- `chrome://net-export` for a detailed network log
- `chrome://webrtc-internals` for WebRTC sessions
- `chrome://gpu` for graphics feature status
- `chrome://serviceworker-internals` only when available and appropriate; prefer DevTools for normal work

Chrome internal pages are diagnostic implementation tools and can change between versions.

## Final Safety Rule

Before sharing screenshots, HAR files, cURL commands, heap snapshots, or net logs, remove tokens, cookies, authorization headers, query secrets, personal data, and private host names.
