# CDNs and Edge Delivery

## Idea

A CDN caches and serves content near users. Edge functions can perform small
location-near work such as redirects, authentication checks, or personalization.

## Visual model

```text
user -> nearest edge --hit--> response
                     --miss--> origin -> edge cache -> response
```

## Design steps

1. Give immutable assets content-hashed URLs and long cache lifetimes.
2. Define cache keys including only required headers/query dimensions.
3. Set `Cache-Control`, revalidation, and purge/version strategy.
4. Protect origin with shielding, rate limits, and signed URLs/cookies.
5. Measure hit ratio, origin load, edge errors, and regional latency.

## When to use it

Use for static assets, images/video segments, downloads, and safe cacheable API
responses. Use signed access for private media.

## Trade-offs

Personalized cache keys reduce hit rate. Purges can be slow or expensive;
versioned immutable URLs are simpler. Edge compute has runtime and data limits.

## Common mistakes

- Caching private responses under a shared key.
- Serving stale HTML referencing removed assets.
- Query-string cache fragmentation.
- Assuming CDN means the origin needs no capacity or protection.
