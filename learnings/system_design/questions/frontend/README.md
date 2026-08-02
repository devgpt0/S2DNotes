# Frontend System Design Questions

Frontend system design covers browser constraints, rendering, state ownership,
network behavior, performance, resilience, accessibility, security, and
team-scale delivery.

Use the [interview framework](../00-interview-answer-framework.md), but replace
backend capacity guesses with explicit browser, device, network, and user
experience budgets where appropriate.

## Stage 1 - Product experiences

1. [Infinite social feed](01-infinite-social-feed.md) - Easy
2. [Collaborative document editor](02-collaborative-editor.md) - Hard
3. [Design system and component library](03-design-system.md) - Medium
4. [Micro-frontend platform](04-micro-frontend-platform.md) - Hard
5. [Real-time analytics dashboard](05-real-time-dashboard.md) - Medium
6. [Offline-first task application](06-offline-first-app.md) - Medium
7. [Large media gallery](07-media-gallery.md) - Easy

## Stage 2 - Current frontend interview themes

8. [AI assistant interface](08-ai-assistant-interface.md) - Hard
9. [Adaptive video streaming client](09-video-streaming-client.md) - Hard
10. [Resilient checkout frontend](10-checkout-frontend.md) - Medium
11. [Interactive map frontend](11-interactive-map.md) - Hard
12. [Dynamic form builder](12-form-builder.md) - Hard
13. [Virtualized enterprise data grid](13-virtualized-data-grid.md) - Hard
14. [Frontend observability and safe-release platform](14-frontend-observability-and-release.md) - Hard
15. [Real-time chat frontend](15-realtime-chat-frontend.md) - Medium

## What every answer must include

```text
user flow -> state ownership -> API/events -> component boundaries
          -> loading/error/offline states -> performance budgets
          -> accessibility/security -> rollout and telemetry
```

Do not reduce frontend system design to a component tree. Explain what happens
on a slow device, a flaky network, a stale response, and a bad deployment.
