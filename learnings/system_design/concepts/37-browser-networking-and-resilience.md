# Browser Networking and API Resilience

## Idea

Browser requests run on unreliable networks and race with user navigation.
Frontend data layers must cancel obsolete work, deduplicate requests, bound
retries, and prevent stale responses from replacing newer state.

## Visual model

```text
user action -> request key -> cache/deduplicate -> AbortController
            -> timeout/retry policy -> validated response -> current-view check
```

## Design steps

1. Define a stable cache/request key from endpoint and relevant parameters.
2. Cancel work when its view/unmounted intent is obsolete.
3. Deduplicate in-flight reads and bound concurrency.
4. Retry only transient idempotent requests with backoff and jitter.
5. Validate response shape at the trust boundary.
6. Use cursor pagination and guard against out-of-order responses.

## When to use it

Every data-heavy frontend needs request lifecycle management. Centralize common
behavior in a small HTTP/query layer rather than repeating it in components.

## Trade-offs

Automatic retries hide brief failures but can waste mobile bandwidth and amplify
outages. Longer client caches improve navigation speed but need invalidation.

## Failure states to design

- Offline versus server rejection versus timeout.
- Partial page failure while other regions remain useful.
- Expired authentication with one coordinated refresh attempt.
- User retry that does not duplicate a mutation.

## Common mistakes

- Retrying every `4xx` response.
- Letting an old search response overwrite a newer query.
- Infinite-scroll requests without cancellation/concurrency bounds.
- Treating TypeScript types as runtime response validation.
