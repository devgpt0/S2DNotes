# Web Performance and Delivery

## Idea

Web performance is the full path from navigation to useful interaction. Control
network transfer, server response, render-blocking resources, JavaScript work,
images/fonts, layout stability, and long tasks.

## Visual model

```text
DNS/TLS -> TTFB -> HTML -> critical CSS/content -> LCP
JS parse/execute + event work -> INP
late size changes -> CLS
```

## Design steps

1. Set route/device performance budgets and Core Web Vitals targets.
2. Serve cacheable assets from a CDN with content hashes and long TTLs.
3. Prioritize the LCP resource; lazy-load only below-the-fold work.
4. Split code and defer third parties/non-critical hydration.
5. Reserve media/ad dimensions and optimize fonts.
6. Use workers/virtualization for CPU-heavy or very large UI work.
7. Measure lab and real-user data by route, device, region, and release.

## When to use each technique

- Preload only truly critical resources.
- Prefetch likely future navigation at low priority.
- Virtualize large lists when DOM size is the bottleneck.
- Use a service worker only with explicit cache/version/offline behavior.

## Trade-offs

Aggressive caching improves latency but risks stale HTML/API data. Code splitting
shrinks initial bundles but too many chunks add request/waterfall overhead.

## Common mistakes

- Optimizing bundle bytes while ignoring main-thread execution.
- Lazy-loading the LCP image.
- Measuring only a powerful developer laptop.
- Shipping unbounded third-party scripts without budgets or isolation.
