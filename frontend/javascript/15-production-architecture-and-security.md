# 15 - Production JavaScript Architecture and Security

## Start with Boundaries

A maintainable frontend separates:

- trusted domain values
- external runtime data
- pure calculations
- browser side effects
- UI rendering
- network/storage adapters

The goal is not to create many layers. The goal is to make ownership, failures, and data flow obvious.

## A Small Feature Shape

```text
course-search/
|-- course.js          # domain validation and pure rules
|-- course-api.js      # Fetch boundary
|-- course-view.js     # DOM creation
`-- course-search.js   # feature coordination and lifecycle
```

Create this separation when responsibilities genuinely differ. A tiny feature can stay in one file until complexity appears.

## Validate at the Boundary

```javascript
const parseCourse = (value) => {
  if (typeof value !== "object" || value === null) {
    throw new TypeError("course must be an object");
  }
  if (typeof value.id !== "string" || value.id.length === 0) {
    throw new TypeError("course id must be a non-empty string");
  }
  if (typeof value.title !== "string" || value.title.length === 0) {
    throw new TypeError("course title must be a non-empty string");
  }
  return Object.freeze({ id: value.id, title: value.title });
};
```

Do not pass arbitrary server or storage objects through the whole application.

## Pure Domain Update

```javascript
const addCourse = (courses, course) => {
  if (!Array.isArray(courses)) throw new TypeError("courses must be an array");
  if (courses.some((existing) => existing.id === course.id)) {
    throw new RangeError(`duplicate course id: ${course.id}`);
  }
  return [...courses, course];
};

const next = addCourse([], { id: "js", title: "JavaScript" });
console.log(next);
// Output: [{ id: "js", title: "JavaScript" }]
```

Pure rules are easy to test because inputs and outputs contain the behavior.

## Network Adapter

```javascript
export const loadCourses = async (signal) => {
  const response = await fetch("/api/courses", {
    headers: { Accept: "application/json" },
    signal,
  });
  if (!response.ok) throw new Error(`courses request failed: HTTP ${response.status}`);

  const value = await response.json();
  if (!Array.isArray(value)) throw new TypeError("courses response must be an array");
  return value.map(parseCourse);
};
```

The adapter owns HTTP details and converts external data into trusted domain values.

## DOM Renderer

```javascript
export const courseElement = (course) => {
  const item = document.createElement("li");
  const link = document.createElement("a");
  link.href = `/courses/${encodeURIComponent(course.id)}`;
  link.textContent = course.title;
  item.append(link);
  return item;
};
```

`textContent` treats course titles as text. Encoding the path segment prevents an ID from changing URL structure.

## Feature Lifecycle

```javascript
export const mountCourseSearch = (root) => {
  if (!(root instanceof HTMLElement)) throw new TypeError("root is required");
  const controller = new AbortController();

  void loadCourses(controller.signal).then(
    (courses) => root.replaceChildren(...courses.map(courseElement)),
    (error) => {
      if (error instanceof DOMException && error.name === "AbortError") return;
      root.textContent = "Courses could not be loaded.";
    },
  );

  return () => controller.abort();
};
```

The owner receives cleanup. Expected abort is handled; unrelated failures are not silently treated as success.

## Error Categories

Separate errors that need different action:

- validation: external data violates a contract
- authentication: user identity missing/expired
- authorization: identity lacks permission
- conflict: state changed since the user's version
- rate/capacity: retry only according to a bounded policy
- transient network: may support retry
- programmer error: should reach monitoring and fail the operation

Do not show raw exception messages or stack traces to users.

## Cross-Site Scripting

XSS happens when untrusted content becomes executable markup or code.

Prefer safe sinks:

```javascript
status.textContent = userMessage;
input.value = userValue;
```

Dangerous sinks require a proven need and policy:

- `innerHTML`
- `outerHTML`
- `insertAdjacentHTML`
- dynamic script creation
- string-to-code APIs such as `eval`
- unvalidated `javascript:` or navigation URLs

If rich HTML is a product requirement, use a maintained sanitizer with an explicit allowlist and a Content Security Policy.

## URL Safety

```javascript
const safeExternalUrl = (value, base = location.origin) => {
  const url = new URL(value, base);
  if (url.protocol !== "https:") throw new TypeError("only HTTPS links are allowed");
  return url;
};
```

Protocol policy depends on the feature. Internal navigation may also require an allowed origin/path check. Never place secrets into URLs because they can reach history, logs, referrers, and screenshots.

## Prototype Pollution

Do not recursively merge untrusted keys into ordinary objects.

```javascript
const ALLOWED_SETTINGS = new Set(["theme", "density"]);

const parseSettings = (value) => {
  if (typeof value !== "object" || value === null) throw new TypeError("invalid settings");
  const result = Object.create(null);
  for (const [key, item] of Object.entries(value)) {
    if (!ALLOWED_SETTINGS.has(key) || typeof item !== "string") {
      throw new TypeError(`invalid setting: ${key}`);
    }
    result[key] = item;
  }
  return result;
};
```

Allowlist fields instead of trying to sanitize arbitrary object graphs.

## Authentication and Authorization

- frontend code cannot keep a secret from the user
- route guards improve UX but do not enforce server authorization
- every protected server operation must authorize the authenticated identity
- `HttpOnly`, `Secure`, appropriate `SameSite` cookies reduce some token risks
- cookie sessions need CSRF design
- do not store long-lived bearer tokens in local storage as a default

## Supply Chain

- minimize dependencies
- inspect package ownership, releases, and install scripts
- use lockfiles and automated review
- remove unused packages
- treat copied registry/component code as owned source
- do not expose private registry credentials in logs or frontend builds

## Configuration and Secrets

Frontend environment variables are built into public assets unless tooling explicitly keeps them server-side.

Allowed frontend configuration includes public API base URLs or feature flags that are not authorization controls. Database passwords, private API keys, signing keys, and service credentials belong on a trusted server.

## Performance Architecture

Start with:

- less JavaScript
- fewer client-only request waterfalls
- route/feature splitting at meaningful boundaries
- stable server/cache behavior
- responsive images and fonts
- bounded lists and caches
- main-thread work measured in Chrome

Memoization is not an architecture. Cache only with explicit key, size, invalidation, error, and ownership rules.

## Testing Strategy

| Level | Proves |
|---|---|
| pure unit test | domain calculation and failure rules |
| component/DOM test | user-visible interaction and accessibility |
| boundary test | parsing and network/storage behavior |
| integration test | several real parts work together |
| end-to-end test | important user journey in a browser |
| performance test | budget under a named environment |

Test loading, success, empty, invalid, error, cancellation, retry, offline, and conflict states where relevant.

## Observability

Useful frontend telemetry may include:

- route and release version
- safe error category
- Core Web Vitals
- request duration/status category
- feature success/failure rate
- correlation/trace ID

Never log tokens, passwords, full sensitive payloads, or unnecessary personal data.

## Expert Review Questions

1. Where does untrusted data become trusted?
2. Who owns each side effect and cleanup?
3. Can invalid state be represented?
4. What happens on slow, cancelled, duplicate, stale, and failed work?
5. Is authorization enforced on the server?
6. Does the feature remain usable by keyboard and assistive technology?
7. What evidence shows performance is acceptable?
8. Which dependency or abstraction can be removed?

## Final Rule

Production architecture is clear ownership and explicit failure behavior, not the number of folders or patterns.
