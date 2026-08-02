# Backend System Design Questions

These solved answers progress from common building blocks to modern senior
platform designs. Use the [interview framework](../00-interview-answer-framework.md)
before reading a solution.

## Stage 1 - Core services

1. [URL shortener](01-url-shortener.md) - Easy
2. [Distributed rate limiter](02-distributed-rate-limiter.md) - Medium
3. [Notification service](03-notification-service.md) - Medium

## Stage 2 - Product systems

4. [Chat and messaging](04-chat-system.md) - Hard
5. [Personalized news feed](05-news-feed.md) - Hard
6. [Cloud file storage and sync](06-cloud-file-storage.md) - Hard
7. [Video streaming platform](07-video-streaming.md) - Hard
8. [Payment and ledger system](08-payment-ledger.md) - Hard
9. [E-commerce inventory and orders](09-inventory-and-orders.md) - Hard
10. [Search autocomplete](10-search-autocomplete.md) - Medium

## Stage 3 - Distributed infrastructure

11. [Distributed job scheduler](11-job-scheduler.md) - Hard
12. [Metrics and log ingestion](12-observability-pipeline.md) - Hard
13. [Ride-sharing location and dispatch](13-ride-sharing-location.md) - Hard
14. [Large-scale web crawler](14-web-crawler.md) - Hard
15. [High-contention ticket booking](15-ticket-booking.md) - Hard
16. [Webhook delivery platform](16-webhook-delivery-platform.md) - Medium
17. [Feature flag and dynamic configuration service](17-feature-flag-service.md) - Medium

## Stage 4 - Current senior platform themes

18. [A/B experimentation platform](18-experimentation-platform.md) - Hard
19. [Multi-region active-active service](19-multi-region-active-active.md) - Hard
20. [Real-time leaderboard](20-realtime-leaderboard.md) - Medium
21. [Distributed cache service](21-distributed-cache.md) - Hard
22. [API gateway and service platform](22-api-gateway-platform.md) - Hard
23. [Tamper-evident audit log](23-audit-log-platform.md) - Hard
24. [Live comments and reactions](24-live-comments-and-reactions.md) - Medium
25. [Large data export and reporting](25-data-export-and-reporting.md) - Medium

## Practice method

```text
hide solution -> clarify for 5 minutes -> estimate -> draw -> deep-dive
              -> explain failures/security -> compare with model answer
```

The strongest backend answers identify the data invariant, ownership boundary,
retry behavior, and first bottleneck before naming products.
