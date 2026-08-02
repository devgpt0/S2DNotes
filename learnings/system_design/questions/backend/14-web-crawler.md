# Design a Large-Scale Web Crawler

> **Difficulty:** Hard  
> **Main focus:** URL frontier, politeness, deduplication

## Interview prompt

Design a crawler that discovers and fetches pages at large scale without harming websites.

## 1. Clarify the scope

**What I would say first:** The URL frontier must schedule by host, respect robots and politeness, and deduplicate both URLs and content.

### Functional requirements

- Discover URLs, fetch allowed pages, parse links, and store content or metadata.
- Respect robots.txt, per-host rate limits, and crawl priority.
- Avoid URL loops and duplicate content.
- Retry transient failures and recrawl changed pages.

### Out of scope for the first version

- Search ranking and serving are downstream systems.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume billions of known URLs and millions of fetches per minute.
- Network and external host behavior dominate; one host must never monopolize workers.
- The frontier is much larger than memory and requires durable partitioning.

## 3. API and data model

### Main contracts

- POST /internal/seeds {urls, priority}
- Frontier lease: claim(hostPartition, limit) -> URLs with lease expiry
- Fetch result event: {url, status, contentHash, discoveredUrls, nextFetchAt}

### Important data

- URLRecord(canonical_url_hash, canonical_url, host, state, priority, next_fetch_at)
- HostPolicy(host, robots_version, next_allowed_at, crawl_delay, failure_score)
- Content(content_hash, object_ref, mime_type, fetched_at)

## 4. High-level design

```text
seeds/discovered links -> canonicalize/deduplicate -> durable URL frontier
                                                        |
                                               host-aware scheduler
                                                        |
                                                    fetch workers
                                                        |
                       robots cache <- policy check <- response -> parser
                                                        |
                                      content store + new URL stream
```

## 5. Critical request flow

1. Canonicalize a URL, reject unsupported schemes, and deduplicate its hash.
2. Place it into a host-partitioned frontier with priority and next fetch time.
3. Scheduler leases URLs only when host policy permits another request.
4. Fetcher resolves safely, downloads within size/time limits, and records status.
5. Parser stores content metadata and emits normalized discovered links.

## 6. Deep dive

- Separate host queues from a global ready-host queue to enforce politeness.
- Bloom filters reduce repeated database checks but false positives require acceptable policy.
- Content hashes detect mirrors and duplicate bodies after fetch.
- Recrawl frequency adapts to historical change rate and importance.

## 7. Scaling, failures, and observability

- Leases expire so crashed-worker URLs return to the frontier.
- Exponential backoff and host circuit breakers protect failing sites.
- Bound redirects, DNS results, response size, and parser resource use.
- Monitor fetch success, frontier age, duplicate rate, robots failures, and per-host request rate.

## 8. Security and privacy

- Defend against SSRF: block private networks, revalidate redirects and DNS, and isolate fetchers.
- Sandbox parsers and treat every page as hostile input.
- Identify the crawler honestly and support owner opt-out.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Exact global deduplication | Accurate but expensive at web scale. |
| Bloom filter front gate | Memory-efficient with false positives. |
| Fast recrawl | Fresher data but greater cost and site load. |
| Adaptive recrawl | Efficient but needs historical signals. |

## 10. 60-second interview summary

A durable frontier is partitioned by host, and a ready-host scheduler enforces robots and politeness before leasing URLs. Fetchers are isolated against hostile content and SSRF, while URL and content deduplication control repeated work.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you test recovery from a dependency timeout?
- Which metric best reflects the user's experience?

