# 06 - Browser Storage: Complete Selection and Lifecycle Guide

## Storage Is an Ownership Decision

Before choosing an API, answer:

1. Who owns the source of truth: browser, URL, or server?
2. How long should the value live?
3. Which tabs, windows, devices, or users should see it?
4. Is the value sensitive?
5. How large can it become?
6. Does it need queries or transactions?
7. Must it work offline?
8. Can the browser evict it?
9. How will schema versions migrate?
10. What happens when reading or writing fails?

Storage choice comes after these answers.

## Quick Selection Table

| Need | Suitable starting place | Avoid |
|---|---|---|
| current component interaction | React/local memory | persistent storage |
| complex shared client workflow | Redux memory | localStorage as live state bus |
| shareable filter/page/sort | URL search parameters | hidden Redux-only state |
| short one-tab draft | sessionStorage | cookie |
| small non-sensitive preference | localStorage | storing secrets |
| authenticated session identifier | secure HttpOnly cookie controlled by server | JavaScript-readable token storage by default |
| offline structured records | IndexedDB | localStorage |
| cached HTTP responses/assets | Cache Storage | using it as a general object database |
| large browser-owned files/blobs | OPFS after support/product analysis | base64 in localStorage |
| user-selected external file | File System Access API with permission/fallback | assuming permanent permission |
| cross-device source of truth | server database/API | browser-only storage |

## 1. Memory State

Examples: variables, React state, Redux store, in-memory query cache.

```javascript
let selectedCourseId = null;
selectedCourseId = "typescript";
console.log(selectedCourseId);
// Output: typescript
```

### Lifetime

Normally until reload, navigation, tab close, or process loss.

### Suitable Use Cases

- current UI state
- unsaved values that do not need recovery
- derived/cached data that can be fetched again
- sensitive values that should not be written to persistent browser storage, while still recognizing XSS can read live JavaScript memory

### Suitable Stage

Best default during prototype and production. Start in memory; add persistence only after a real survival requirement appears.

## 2. URL State

Path, query string, and fragment can represent navigation state.

```javascript
const url = new URL(location.href);
url.searchParams.set("topic", "typescript");
url.searchParams.set("page", "2");
history.replaceState(null, "", url);
console.log(url.search);
// Output: ?topic=typescript&page=2
```

### Lifetime and Scope

Survives reload, copy/paste, bookmarks, and browser history according to navigation updates.

### Suitable Use Cases

- search query
- filters
- sorting
- pagination
- selected tab with navigation meaning
- resource ID

### Do Not Store

Secrets, tokens, personal data, large payloads, or internal implementation state. URLs reach history, logs, analytics, referrers, screenshots, and shared links.

### Suitable Stage

Use from the first production version when state must be shareable or navigable. Adding URL ownership late often requires refactoring duplicate local/Redux state.

## 3. Cookies

Cookies are small key/value data automatically sent with matching HTTP requests according to domain, path, security, SameSite, and expiry rules.

Server response example:

```http
Set-Cookie: session=opaque-id; Path=/; Secure; HttpOnly; SameSite=Lax
```

### Important Attributes

- `Secure`: send only over HTTPS
- `HttpOnly`: JavaScript cannot read the cookie
- `SameSite`: controls cross-site sending behavior
- `Domain` and `Path`: request scope
- `Max-Age` or `Expires`: persistent lifetime; without them it is a session cookie

### Suitable Use Cases

- opaque server session identifier
- CSRF token pattern when designed by the server/security architecture
- very small server-needed preference when request overhead is acceptable

### Limitations

- small, commonly around 4 KB per cookie with browser/domain limits
- sent on matching requests, adding bandwidth
- requires CSRF design for cookie-authenticated state-changing requests
- partitioning and privacy rules affect cross-site use

### Suitable Stage

Use for production authentication only as part of a complete HTTPS, session, CSRF, expiry, rotation, and logout design. Do not invent authentication storage during a frontend-only prototype.

## 4. `sessionStorage`

Synchronous string storage scoped to one origin and one top-level browsing context/page session.

```javascript
const DRAFT_KEY = "course-draft.v1";
sessionStorage.setItem(DRAFT_KEY, JSON.stringify({ title: "TypeScript" }));

const text = sessionStorage.getItem(DRAFT_KEY);
if (text === null) throw new Error("draft is missing");
const value = JSON.parse(text);
if (typeof value !== "object" || value === null || typeof value.title !== "string") {
  throw new TypeError("stored draft is invalid");
}
console.log(value.title);
// Output: TypeScript
```

### Lifetime and Scope

Normally survives reload in that tab and ends when the tab/page session ends. A new tab gets a separate session storage area, with browser-defined opener initialization details.

### Suitable Use Cases

- temporary non-sensitive one-tab draft
- one-tab wizard checkpoint
- temporary redirect/navigation context that should not become a URL

### Limitations

- synchronous main-thread API
- strings only
- small quota
- no cross-device or reliable crash-survival promise
- JavaScript-readable and exposed to XSS

### Suitable Stage

Useful in prototypes and production for small one-tab recovery. Add schema validation/versioning before production.

## 5. `localStorage`

Synchronous string storage scoped by origin and intended to persist across browser sessions.

```javascript
const THEME_KEY = "preferences.theme.v1";
const saveTheme = (theme) => {
  if (theme !== "light" && theme !== "dark") throw new TypeError("invalid theme");
  localStorage.setItem(THEME_KEY, theme);
};

const loadTheme = () => {
  const value = localStorage.getItem(THEME_KEY);
  if (value === null) return undefined;
  if (value !== "light" && value !== "dark") throw new TypeError("stored theme is invalid");
  return value;
};
```

### Suitable Use Cases

- small non-sensitive theme/density preference
- small versioned feature preference
- a prototype cache where synchronous cost and data loss are acceptable

### Poor Use Cases

- authentication tokens by default
- large lists/blobs
- high-frequency writes
- multi-record queries
- transactional data
- authoritative business data
- complete Redux stores

### Limitations

- synchronous and can block the main thread
- strings only
- quota/security errors can throw
- may be cleared or restricted
- XSS can read it
- schema becomes stale across releases

### Suitable Stage

Fine for quick prototypes. For production, keep data tiny, validate on every read, version keys/schema, handle failures, and define a reset/migration policy.

## 6. IndexedDB

IndexedDB is an asynchronous transactional database for structured browser data.

### Suitable Use Cases

- offline-first records
- many structured objects
- indexed queries
- transactional updates
- larger client caches
- queued offline mutations with a carefully designed sync protocol

### First Example

```javascript
const openDatabase = () => new Promise((resolve, reject) => {
  const request = indexedDB.open("course-app", 1);
  request.addEventListener("upgradeneeded", () => {
    const database = request.result;
    const store = database.createObjectStore("courses", { keyPath: "id" });
    store.createIndex("by-title", "title");
  });
  request.addEventListener("success", () => resolve(request.result));
  request.addEventListener("error", () => reject(request.error));
});
```

Production code should wrap request/transaction completion carefully or use a maintained small IndexedDB library. Opening a database is only the first step.

### Transactions

All related reads/writes should occur within the correct transaction. A request succeeding does not alone mean the entire transaction committed.

### Schema Versions

Database version upgrades run in `upgradeneeded`. Migrations must handle users jumping across released versions and must not perform network-dependent work inside the upgrade transaction.

### Suitable Stage

Use when product requirements include offline structured data or size/query needs beyond Web Storage. Do not introduce it only because an app reached “production.”

## 7. Cache Storage

Cache Storage stores `Request`/`Response` pairs and is commonly used by service workers.

```javascript
const cache = await caches.open("course-static-v1");
await cache.addAll(["/", "/styles.css", "/app.js"]);
const response = await cache.match("/styles.css");
console.log(response?.status);
// Output: 200 when cached successfully.
```

### Suitable Use Cases

- app shell/static assets
- explicitly cacheable HTTP responses
- offline fallback responses
- stale-while-revalidate or cache-first strategies with versioning

### Poor Use Cases

- arbitrary domain object querying
- secrets/private responses without a proven policy
- replacing HTTP cache automatically
- indefinite accumulation without cleanup

### Suitable Stage

Add when PWA/offline/repeat-load requirements justify a service-worker caching strategy. A basic website does not need a service worker merely to be production-ready.

## 8. Origin Private File System (OPFS)

OPFS provides origin-private file storage optimized for file-like workloads.

```javascript
const root = await navigator.storage.getDirectory();
const handle = await root.getFileHandle("course-export.json", { create: true });
const writable = await handle.createWritable();
await writable.write(JSON.stringify({ id: "ts", title: "TypeScript" }));
await writable.close();

const file = await handle.getFile();
console.log(file.size);
// Output: stored byte size.
```

### Suitable Use Cases

- large files/blobs owned by the web app
- local editors
- media processing
- SQLite/WASM-style file workloads
- high-performance file access in a worker where supported

### Limitations

- origin-private, not a user-visible normal file by default
- browser support and quota policy must be tested
- requires application indexing/metadata design
- still subject to data clearing/eviction policies

### Suitable Stage

Use in advanced offline/file-heavy products after IndexedDB vs OPFS workload analysis and support testing. It is unnecessary for ordinary preferences or small JSON records.

## 9. File System Access API

This API lets the user choose files or directories and grants a handle according to browser permission behavior.

```javascript
const [handle] = await window.showOpenFilePicker({
  types: [{ description: "JSON", accept: { "application/json": [".json"] } }],
});
const file = await handle.getFile();
console.log(file.name);
```

Use for explicit user-owned files, not silent application persistence. Provide fallbacks for unsupported browsers and never assume permission remains forever.

## 10. Server Storage

A server database is required when data must be authoritative, shared across devices/users, protected by authorization, audited, backed up, or processed by trusted services.

Browser storage can support offline/cache behavior but should not become the only copy of important business data.

## Storage Quota and Eviction

```javascript
const estimate = await navigator.storage.estimate();
console.log({ usage: estimate.usage, quota: estimate.quota });
```

Quota varies by browser, device, free space, engagement, storage type, and private mode. Never hardcode one universal capacity.

Request persistent storage when data loss would materially harm an offline product:

```javascript
const persisted = await navigator.storage.persist();
console.log(persisted);
// Output: true or false according to browser policy.
```

Persistence is a request, not a guarantee of backup. Users can still clear site data.

## Cross-Tab Updates

The `storage` event observes localStorage changes from another same-origin document:

```javascript
window.addEventListener("storage", (event) => {
  if (event.key === THEME_KEY) console.log(event.newValue);
});
```

Use `BroadcastChannel` for explicit cross-context messages:

```javascript
const channel = new BroadcastChannel("course-events");
channel.addEventListener("message", (event) => console.log(event.data));
channel.postMessage({ type: "course-updated", id: "ts" });
const dispose = () => channel.close();
```

BroadcastChannel is communication, not storage. Validate messages and close the channel.

## Privacy, Partitioning, and Private Browsing

Storage access can be partitioned or restricted in third-party contexts. Private browsing may use temporary quotas/lifetimes. Users and enterprise policies can clear or block storage.

Design first-party applications without depending on unrestricted cross-site storage. Feature-detect and provide a clear degraded experience.

## Inspect Storage in Chrome DevTools

Open DevTools > Application.

### Storage Overview

Use the Storage section to inspect usage and clear site data. Clear only the origin you intend to test; removing service workers, caches, cookies, and databases can log you out and delete offline work.

### Local and Session Storage

- expand Local Storage or Session Storage
- select the origin
- inspect key/value strings
- edit a value to test strict runtime validation
- delete one key and verify the application handles absence

Do not paste secrets into screenshots or bug reports.

### IndexedDB

- inspect database version, object stores, indexes, and rows
- refresh the view after application transactions
- test upgrades using a clean profile and data from each supported old version
- use the Console or application code for transaction behavior; the table view alone does not prove atomicity

### Cache Storage and Service Workers

- inspect cache names and Request/Response entries
- verify which service worker controls the page
- test offline behavior and update activation
- use “Bypass for network” only as a diagnostic comparison
- remove old versioned caches during service-worker activation according to policy

### Cookies

Inspect domain, path, expiry, size, `HttpOnly`, `Secure`, `SameSite`, and partitioning fields. Use Network request/response headers to understand why a cookie was set or sent.

JavaScript cannot read `HttpOnly` cookies; DevTools can show them to the developer.

### Quota

Compare DevTools storage usage with `navigator.storage.estimate()`. Values can be approximate and change with browser policy.

### Test Matrix

For every persisted feature, test:

1. first visit with empty storage
2. valid current data
3. missing optional data
4. malformed JSON or wrong types
5. old supported schema
6. unsupported schema
7. quota/security write failure
8. reload and new tab
9. logout/user switch
10. storage cleared while the app is open
11. private browsing/restricted policy
12. offline and reconnection when applicable

## Security Rules

- XSS can read JavaScript-accessible storage
- do not treat obfuscation/encryption with a shipped client key as secret protection
- do not store passwords or private service credentials
- cookie authentication needs CSRF protection and server authorization
- validate stored data on every load
- avoid caching private responses unless policy is explicit
- clear user-specific browser data on logout/shared-device flows as required
- storage deletion is not guaranteed secure erasure from every backup/sync system

## Schema Versioning

Name or encode versions:

```javascript
const KEY = "course-draft.v2";
```

Keep validation and migration separate:

```javascript
const migrateV1ToV2 = (oldValue) => ({
  version: 2,
  title: oldValue.name,
  updatedAt: new Date().toISOString(),
});
```

Migration transforms known valid old data. Validation proves both old input and new output match their schemas.

## Suitable Choice by Product Stage

### Learning Prototype

- memory first
- URL for shareable navigation
- localStorage only for tiny convenience data
- no custom authentication storage

### Internal Beta

- define schema versions
- observe quota/failure behavior
- validate on read
- decide server source of truth
- test private mode and multiple tabs

### Production Online App

- server owns business data
- secure server-managed session cookie where applicable
- URL owns navigation state
- localStorage/sessionStorage only for narrow non-sensitive needs
- telemetry for storage failures without sensitive payloads

### Offline/PWA Product

- IndexedDB for structured data
- Cache Storage for HTTP assets/responses
- service-worker update/cache strategy
- conflict, retry, queue, migration, and eviction UX
- persistent-storage request where justified

### File-Heavy Local Application

- OPFS for app-owned file workloads
- File System Access for user-owned files
- worker processing for heavy I/O/CPU where supported
- explicit export/backup and data-loss messaging

## Final Decision Flow

```text
Does it need to survive reload?
  no -> memory
  yes -> should it be shareable/navigation state?
    yes -> URL
    no -> does the server need it on requests/auth?
      yes -> secure server-designed cookie/session
      no -> small string preference or one-tab draft?
        yes -> localStorage or sessionStorage
        no -> structured/query/offline data?
          yes -> IndexedDB
          no -> HTTP response cache?
            yes -> Cache Storage
            no -> large file workload?
              yes -> OPFS/File System Access analysis
              no -> server database or reconsider the requirement
```

## Final Rule

Use browser storage as a fallible cache or explicitly scoped local feature unless the product is intentionally offline-first. Important shared data needs a trusted server source of truth.
