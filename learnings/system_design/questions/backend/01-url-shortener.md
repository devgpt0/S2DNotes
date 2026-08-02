# Design a URL Shortener

> **Difficulty:** Easy  
> **Main focus:** key generation, redirects, caching

## Interview prompt

Design a service that creates short links and redirects visitors to the original URL.

## 1. Clarify the scope

**What I would say first:** I will optimize for a read-heavy redirect path. Link creation must be durable; analytics may be asynchronous.

### Functional requirements

- Create a short link for a valid HTTP or HTTPS URL.
- Redirect by short code with low latency.
- Support optional custom aliases, expiration, and link deletion.
- Count visits without slowing the redirect.

### Out of scope for the first version

- Malware crawling and a full analytics dashboard are secondary deep dives.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume 10 million new links per day and 100 million redirects per day.
- A seven-character base-62 code provides more than 3.5 trillion combinations.
- At roughly 500 bytes per link, one year is about 1.8 TB before replicas and indexes.
- Redirect traffic is bursty and much larger than creation traffic, so cache the read path.

## 3. API and data model

### Main contracts

- POST /v1/links {targetUrl, customAlias?, expiresAt?} with Idempotency-Key
- GET /{code} -> 302 Location: targetUrl
- DELETE /v1/links/{code}

### Important data

- Link(code primary key, target_url, owner_id, created_at, expires_at, status)
- VisitEvent(code, timestamp, country, referrer) in an asynchronous analytics stream

## 4. High-level design

```text
creator -> API gateway -> Link service -> primary link store
                              |              |
                              |              +-> cache invalidate
                              +-> ID generator

visitor -> CDN/edge -> Redirect service -> cache -> link store
                         |
                         +-> visit event queue -> analytics workers
```

## 5. Critical request flow

1. Validate the scheme and length; reject unsafe or malformed URLs.
2. Reserve a custom alias atomically, or obtain a unique numeric ID and base-62 encode it.
3. Write the link record before returning the short URL.
4. On redirect, check edge/cache first, then the link store.
5. Return 302 for mutable links; publish a best-effort visit event asynchronously.

## 6. Deep dive

- Use a database uniqueness constraint as the final defense against code collision.
- A range-based ID allocator avoids a central call for every link; random codes also work with collision retries.
- Cache popular codes with expiry shorter than the link's expiry. Negative-cache missing codes briefly.
- Partition by a hash of code so redirects distribute evenly.

## 7. Scaling, failures, and observability

- If analytics is down, redirects continue and events queue until retention limits are reached.
- If cache is down, protect the database with rate limits and load shedding.
- Use tombstones or short negative-cache TTLs so deletion becomes visible quickly.
- Replicate the link store across zones and define a regional recovery objective.

## 8. Security and privacy

- Authenticate management operations; redirects remain public.
- Block dangerous schemes, rate-limit creation, and integrate abuse scanning.
- Do not expose private analytics across owners; encrypt stored targets and audit deletion.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Sequential IDs | Compact and collision-free, but traffic volume is easier to infer. |
| Random codes | Harder to enumerate, but creation needs collision handling. |
| 301 redirect | Better caching, but difficult to change or revoke. |
| 302 redirect | More control and analytics, with slightly more origin traffic. |

## 10. 60-second interview summary

I use a durable code-to-URL store, cache the read-heavy redirect path, generate unique base-62 codes, and keep analytics asynchronous. The redirect remains available when analytics fails, while deletion and abuse controls are explicit.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- What happens when the main dependency times out after completing its work?
- Which metric best reflects the user's experience?

