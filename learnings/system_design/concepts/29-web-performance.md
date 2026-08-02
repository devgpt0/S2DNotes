# Web Performance and Delivery

## Idea

Web performance is the user's wait to see useful content and interact, not one
bundle-size number.

## Classroom board

```text
navigation -> DNS/TLS -> HTML -> critical CSS/content -> LCP
user input -> main-thread work -> next paint -> INP
layout movement -> CLS
```

## Design steps

1. Set route/device Core Web Vital budgets.
2. Cache/compress assets and split by route/feature.
3. Prioritize critical content; lazy-load below-fold media/code.
4. Reduce main-thread work and virtualize large lists.
5. Measure real users, not laboratory scores alone.

## When to use it

Every frontend design should discuss delivery, rendering, network resilience,
accessibility, and low-end devices.

## Trade-offs and mistakes

Prefetching improves navigation but spends bandwidth. Avoid eager loading,
unoptimized images, hydration of static UI, unstable layout dimensions, and
optimization without field measurement.
