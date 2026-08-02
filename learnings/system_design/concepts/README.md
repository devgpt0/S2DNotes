# System Design Concepts

Read these notes in order. The path starts with the shared foundations, then
moves through backend, frontend, and AI-engineering systems.

Each note explains the idea, visual model, design steps, pattern clues,
trade-offs, failure cases, and common mistakes where they apply.

## Stage 1 - Design the right problem

1. [A repeatable interview framework](01-interview-framework.md)
2. [Functional and non-functional requirements](02-requirements-and-scope.md)
3. [Capacity estimation](03-capacity-estimation.md)
4. [API contracts](04-api-contracts.md)
5. [Data modeling and access patterns](05-data-modeling.md)

## Stage 2 - Core distributed building blocks

6. [Network protocols](06-network-protocols.md)
7. [Latency, throughput, and availability](07-latency-throughput-availability.md)
8. [Horizontal scaling and load balancing](08-scaling-and-load-balancing.md)
9. [Caching](09-caching.md)
10. [CDNs and edge delivery](10-cdn-and-edge.md)
11. [Choosing a database](11-database-selection.md)
12. [Indexes and query design](12-indexes-and-queries.md)
13. [Transactions and isolation](13-transactions-and-isolation.md)
14. [Consistency and CAP](14-consistency-and-cap.md)
15. [Replication](15-replication.md)
16. [Sharding and consistent hashing](16-sharding-and-consistent-hashing.md)
17. [Queues and streams](17-queues-and-streams.md)
18. [Events, outbox, and idempotency](18-events-outbox-idempotency.md)
19. [Timeouts, retries, circuit breakers, and backpressure](19-resilience-patterns.md)
20. [Rate limiting](20-rate-limiting.md)
21. [Real-time communication](21-real-time-communication.md)
22. [Object storage and media pipelines](22-object-storage-and-media.md)
23. [Search systems](23-search-systems.md)
24. [Observability and SLOs](24-observability-and-slos.md)
25. [Security and privacy](25-security-and-privacy.md)
26. [Multi-tenancy](26-multi-tenancy.md)

## Stage 3 - Advanced backend and operations

27. [Service discovery and configuration](27-service-discovery-and-configuration.md)
28. [Consensus, leaders, and distributed locks](28-consensus-leaders-and-locks.md)
29. [Disaster recovery and multi-region systems](29-disaster-recovery-and-multi-region.md)
30. [Workflows and schedulers](30-workflows-and-schedulers.md)
31. [Schema evolution and data migrations](31-schema-evolution-and-migrations.md)
32. [Service boundaries, gateways, and communication](32-service-boundaries-and-gateways.md)
33. [Cost and capacity engineering](33-cost-and-capacity-engineering.md)

## Stage 4 - Frontend systems

34. [Frontend architecture and rendering](34-frontend-architecture-and-rendering.md)
35. [Client state, server state, and offline sync](35-frontend-state-and-offline.md)
36. [Web performance and delivery](36-web-performance.md)
37. [Browser networking and resilience](37-browser-networking-and-resilience.md)
38. [Frontend observability and safe releases](38-frontend-observability-and-releases.md)
39. [Design systems, accessibility, and internationalization](39-design-systems-accessibility-i18n.md)
40. [Micro-frontends and team boundaries](40-micro-frontends-and-team-boundaries.md)
41. [Client security and browser trust boundaries](41-client-security-and-trust.md)
42. [Real-time collaboration and conflict handling](42-realtime-collaboration-and-conflicts.md)

## Stage 5 - AI-engineering systems

43. [AI system lifecycle and data](43-ai-lifecycle-and-data.md)
44. [Embeddings and vector search](44-embeddings-and-vector-search.md)
45. [Retrieval-augmented generation](45-rag.md)
46. [LLM serving](46-llm-serving.md)
47. [AI evaluation and observability](47-ai-evaluation-and-observability.md)
48. [Agent and tool orchestration](48-ai-agents.md)
49. [AI safety, privacy, and governance](49-ai-safety-privacy-governance.md)
50. [Feature stores and ML data pipelines](50-feature-stores-and-ml-data-pipelines.md)
51. [Training, fine-tuning, and model registries](51-training-fine-tuning-and-model-registry.md)
52. [Inference optimization and GPU scheduling](52-inference-optimization-and-gpu-scheduling.md)
53. [Prompt, context, and memory management](53-prompt-context-and-memory-management.md)
54. [Multimodal and real-time AI](54-multimodal-and-realtime-ai.md)
55. [Recommendation and ranking systems](55-recommendation-and-ranking-systems.md)
56. [AI experimentation and online learning](56-ai-experimentation-and-online-learning.md)
57. [LLM security and threat modeling](57-llm-security-and-threat-modeling.md)
58. [Human-in-the-loop systems and AI incidents](58-human-in-the-loop-and-ai-incidents.md)
59. [AI cost and FinOps](59-ai-cost-and-finops.md)

## Visual map

```text
product requirements and scale
           |
           +-> backend APIs -> cache / database / search / storage
           |                      |
           |                      +-> queues / streams / workflows
           |
           +-> browser or app -> CDN -> rendering / state / offline sync
           |                              |
           |                              +-> performance / releases / security
           |
           +-> AI request -> data / retrieval / tools -> model serving
                                          |
                                          +-> evaluation / safety / human review

every path: security, observability, reliability, recovery, and cost
```
